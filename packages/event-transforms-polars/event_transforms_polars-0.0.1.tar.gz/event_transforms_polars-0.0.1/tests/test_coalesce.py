from event_transforms_polars.coalesce import coalesce_events
from datetime import datetime, timedelta

import polars as pl
from polars.testing import assert_frame_equal
from polars.exceptions import InvalidOperationError, ColumnNotFoundError

import pytest

EVENT_FRAME_SCHEMA = {'id': pl.Int32, 'group': pl.Utf8, 'start': pl.Datetime('us'), 'end': pl.Datetime('us')}

def as_date(n_secs: float) -> datetime:
    return datetime(1970, 1, 1) + timedelta(seconds=n_secs)

def test_each_single_group_cases():

    events = pl.DataFrame([
        # ..AAAA....
        # ....AAAAA.
        (1, 'A', as_date(2), as_date(5)),
        (2, 'A', as_date(4), as_date(8)),

        # ....AAA..
        # ..AAA....
        (3, 'A', as_date(14), as_date(16)),
        (4, 'A', as_date(12), as_date(14)),

        # .AAAAAA.
        # ..AAA...
        (5, 'A', as_date(22), as_date(27)),
        (6, 'A', as_date(23), as_date(25)),

        # .....AA.
        # ..AA....
        (7, 'A', as_date(35), as_date(36)),
        (8, 'A', as_date(33), as_date(34)),

        # .....AA.
        # ...AA...
        (9, 'A', as_date(45), as_date(46)),
        (10, 'A', as_date(44), as_date(45)),
    ], schema=pl.Schema({
        'id': pl.Int32, 'group': pl.Utf8, 'start': pl.Datetime('us'), 'end': pl.Datetime('us'),
    }), orient='row')

    expected = pl.DataFrame([
        (1, as_date(2), as_date(8), 1, 'A', as_date(2), as_date(5)),
        (1, as_date(2), as_date(8), 2, 'A', as_date(4), as_date(8)),

        (2, as_date(12), as_date(16), 3, 'A', as_date(14), as_date(16)),
        (2, as_date(12), as_date(16), 4, 'A', as_date(12), as_date(14)),

        (3, as_date(22), as_date(27), 5, 'A', as_date(22), as_date(27)),
        (3, as_date(22), as_date(27), 6, 'A', as_date(23), as_date(25)),

        (4, as_date(33), as_date(34), 8, 'A', as_date(33), as_date(34)),
        (5, as_date(35), as_date(36), 7, 'A', as_date(35), as_date(36)),

        (6, as_date(44), as_date(46), 9, 'A', as_date(45), as_date(46)),
        (6, as_date(44), as_date(46), 10, 'A', as_date(44), as_date(45)),
    ], schema=pl.Schema({
        'index': pl.Int32, 'start': pl.Datetime('us'), 'end': pl.Datetime('us'), 'id': pl.Int32, 'group': pl.Utf8, 'start_orig': pl.Datetime('us'), 'end_orig': pl.Datetime('us'),
    }), orient='row').sort('start_orig')

    result = coalesce_events(events, 'start', 'end').sort('start_orig')

    assert_frame_equal(result, expected, check_column_order=False)

def test_grouped_results_same_as_calculated_individually():
    
    events_df = pl.DataFrame([
        (1, 'A', as_date(2), as_date(5)),
        (2, 'A', as_date(4), as_date(8)),
        (3, 'A', as_date(14), as_date(16)),
        (4, 'A', as_date(12), as_date(14)),
        (5, 'A', as_date(22), as_date(27)),
        (6, 'A', as_date(23), as_date(25)),
        (7, 'A', as_date(35), as_date(36)),
        (8, 'A', as_date(33), as_date(34)),
        (9, 'A', as_date(45), as_date(46)),
        (10, 'A', as_date(44), as_date(45)),
        (11, 'B', as_date(15), as_date(60)),
        (12, 'B', as_date(40), as_date(65)),
        (13, 'C', as_date(20), as_date(30)),
    ], schema=pl.Schema({
        'id': pl.Int32, 'group': pl.Utf8, 'start': pl.Datetime('us'), 'end': pl.Datetime('us'),
    }), orient='row')

    result_df_using_grouping = coalesce_events(
        events_df,
        x_start='start',
        x_end='end',
        group=['group'],
    ).sort('start').drop('group')

    result_df_individually = pl.concat([
        coalesce_events(group_df.drop(['group']), 'start', 'end')
        for _, group_df in events_df.group_by('group')
    ]).sort('start')

    assert_frame_equal(result_df_individually, result_df_using_grouping)

def test_works_for_lazy_frame():
    events_df = pl.DataFrame([
        (1, 'A', as_date(2), as_date(5)),
        (2, 'A', as_date(4), as_date(8)),
        (3, 'A', as_date(14), as_date(16)),
        (4, 'A', as_date(12), as_date(14)),
        (5, 'A', as_date(22), as_date(27)),
        (6, 'A', as_date(23), as_date(25)),
        (7, 'A', as_date(35), as_date(36)),
        (8, 'A', as_date(33), as_date(34)),
        (9, 'A', as_date(45), as_date(46)),
        (10, 'A', as_date(44), as_date(45)),
        (11, 'B', as_date(15), as_date(60)),
        (12, 'B', as_date(40), as_date(65)),
        (13, 'C', as_date(20), as_date(30)),
    ], schema=pl.Schema({
        'id': pl.Int32, 'group': pl.Utf8, 'start': pl.Datetime('us'), 'end': pl.Datetime('us'),
    }), orient='row')

    result_from_lazyframe = coalesce_events(
        events_df.lazy(),
        x_start='start',
        x_end='end',
        group=['group'],
    ).sort('start').collect()

    result_from_dataframe = coalesce_events(
        events_df,
        x_start='start',
        x_end='end',
        group=['group'],
    ).sort('start')

    assert_frame_equal(result_from_dataframe, result_from_lazyframe)

def test_input_validation_handling():
    
    test_df = pl.DataFrame([
        pl.Series('DATETIME_MS', [], dtype=pl.Datetime('ms')),
        pl.Series('DATETIME_US', [], dtype=pl.Datetime('us')),
        pl.Series('DATETIME_NS', [], dtype=pl.Datetime('ns')),
        pl.Series('DATETIME_MS_UTC', [], dtype=pl.Datetime('ms', 'UTC')),
        pl.Series('DATETIME_MS_OTHER', [], dtype=pl.Datetime('ms', 'Australia/Sydney')),
        pl.Series('FLOAT32', [], dtype=pl.Float32),
        pl.Series('FLOAT64', [], dtype=pl.Float64),
        pl.Series('INT16', [], dtype=pl.Int16),
        pl.Series('INT32', [], dtype=pl.Int32),
    ])

    # Column existence
    with pytest.raises(ColumnNotFoundError):
        coalesce_events(test_df, 'XYZ', 'DATETIME_MS')
    with pytest.raises(ColumnNotFoundError):
        coalesce_events(test_df, 'DATETIME_MS', 'XYZ')
    with pytest.raises(ColumnNotFoundError):
        coalesce_events(test_df, 'DATETIME_MS', 'DATETIME_MS', ['DATETIME_MS', 'XYZ'])

    # Column type validation
    with pytest.raises(InvalidOperationError):
        coalesce_events(test_df, 'DATETIME_MS', 'DATETIME_US')
    with pytest.raises(InvalidOperationError):
        coalesce_events(test_df, 'DATETIME_MS', 'DATETIME_MS_UTC')
    with pytest.raises(InvalidOperationError):
        coalesce_events(test_df, 'DATETIME_MS_OTHER', 'DATETIME_MS_UTC')
    with pytest.raises(InvalidOperationError):
        coalesce_events(test_df, 'FLOAT32', 'FLOAT64')
    with pytest.raises(InvalidOperationError):
        coalesce_events(test_df, 'FLOAT32', 'INT32')
