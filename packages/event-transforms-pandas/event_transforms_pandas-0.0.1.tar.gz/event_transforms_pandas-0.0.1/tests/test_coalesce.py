from event_transforms_pandas.coalesce import coalesce_events
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import pandas as pd
from pandas.testing import assert_frame_equal
import pytest

# Settings for printing dataframes for debugging
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

def as_date(n_secs: float) -> datetime:
    return datetime(1970, 1, 1) + timedelta(seconds=n_secs)

def test_each_single_group_cases():

    events = pd.DataFrame([
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
    ], columns=['id', 'group', 'start', 'end'])

    expected = pd.DataFrame([
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
    ], columns=['index', 'start', 'end', 'id', 'group', 'start_orig', 'end_orig']).sort_values('id').reset_index(drop=True)
    
    result = coalesce_events(events, 'start', 'end').sort_values('id').reset_index(drop=True)[['index', 'start', 'end', 'id', 'group', 'start_orig', 'end_orig']]

    assert_frame_equal(expected, result)

def test_grouped_results_same_as_calculated_individually():

    events_df = pd.DataFrame([
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
    ], columns=['id', 'group', 'start', 'end'])

    result_df_using_grouping = coalesce_events(
        events_df,
        x_start='start',
        x_end='end',
        group='group',
    ).sort_values('id').reset_index(drop=True)

    result_df_individually = pd.concat([
        coalesce_events(
            group_df,
            x_start='start',
            x_end='end',
        )
        for _, group_df in events_df.groupby('group')
    ]).sort_values('id').reset_index(drop=True)

    assert_frame_equal(result_df_using_grouping, result_df_individually)

def test_input_validation_handling():
    test_df = pd.DataFrame(
        [
            {'DATETIME': datetime(2025, 1, 1), 'DATETIME_TZ': datetime(2025, 1, 1, tzinfo=ZoneInfo('Australia/Perth')), 'FLOAT': 1.23, 'STRING': 'A'},
        ],
    )

    # Column existence
    with pytest.raises(KeyError):
        coalesce_events(test_df, 'DATETIME', 'ABC')
    with pytest.raises(KeyError):
        coalesce_events(test_df, 'ABC', 'DATETIME')
    with pytest.raises(KeyError):
        coalesce_events(test_df, 'DATETIME', 'DATETIME', ['DATETIME', 'YZA'])
    
    # Column type validation
    with pytest.raises(TypeError):
        coalesce_events(test_df, 'FLOAT', 'DATETIME')
    with pytest.raises(TypeError):
        coalesce_events(test_df, 'DATETIME', 'DATETIME_TZ')

