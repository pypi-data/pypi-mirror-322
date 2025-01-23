import polars as pl
from polars.exceptions import InvalidOperationError, ColumnNotFoundError

def coalesce_events(
    df: pl.DataFrame | pl.LazyFrame,
    x_start: str,
    x_end: str,
    group: str | list[str] | None = None,
    suffix: str = '_orig',
) -> pl.DataFrame | pl.LazyFrame:
    if type(group) == str:
        groups = [group]
    elif group is None:
        groups = []
    elif type(group) == list:
        groups = group
    
    expected_columns = [x_start, x_end] + groups
    for col in expected_columns:
        if col not in df.collect_schema():
            raise ColumnNotFoundError(f'Column {x_start} not found in DataFrame. Columns found: ' + ', '.join(f'"{x}"' for x in df.columns[:10]) + (", ..." if len(df.columns) > 10 else ""))

    x_start_type, x_end_type = df.collect_schema().get(x_start), df.collect_schema().get(x_end)
    if not x_start_type.is_temporal() and not x_start_type.is_numeric():
        raise InvalidOperationError(f'Column "{x_start}" must be a temporal or numeric type, got {x_start_type}')
    if not x_end_type.is_temporal() and not x_end_type.is_numeric():
        raise InvalidOperationError(f'Column "{x_end}" must be a temporal or numeric type, got {x_end_type}')
    if not x_start_type == x_end_type:
        raise InvalidOperationError(f'Columns "{x_start}" and "{x_end}" must have the same type, got {x_start_type} and {x_end_type}')

    # Coalesce overlapping events
    coalesced_df = pl.concat([
        df.select(groups + [pl.col(x_start).alias('DATETIME'), pl.lit(1).alias('FLAG')]),
        df.select(groups + [pl.col(x_end).alias('DATETIME'), pl.lit(-1).alias('FLAG')]),
    ]).sort('DATETIME').with_columns([
        pl.col('FLAG').cum_sum().over(groups).alias('SIMUL_EVENTS')
        if len(groups) > 0
        else pl.col('FLAG').cum_sum().alias('SIMUL_EVENTS'),
    ]).with_columns([
        pl.col('SIMUL_EVENTS').shift(1).over(groups).alias('PREV_SIMUL_EVENTS')
        if len(groups) > 0
        else pl.col('SIMUL_EVENTS').shift(1).alias('PREV_SIMUL_EVENTS'),
    ]).with_columns([
        pl.when(
            pl.col('SIMUL_EVENTS').gt(0) & pl.col('PREV_SIMUL_EVENTS').fill_null(0).eq(0)
        ).then(
            pl.lit(1)
        ).otherwise(
            pl.lit(0)
        ).alias('NEW_EVENT_FLAG'),
    ]).with_columns([
        pl.col('NEW_EVENT_FLAG').cum_sum().over(groups).alias('index')
        if len(groups) > 0
        else pl.col('NEW_EVENT_FLAG').cum_sum().alias('index'),
    ]).group_by(groups + ['index']).agg([
        pl.col('DATETIME').min().alias(x_start),
        pl.col('DATETIME').max().alias(x_end),
    ]).sort(x_start)

    return df.sort(x_start).rename({x_start: x_start + suffix, x_end: x_end + suffix}).join_asof(
        coalesced_df,
        left_on=x_start + suffix,
        right_on=x_start,
        strategy='backward',
        by=groups if len(groups) > 0 else None,
    )