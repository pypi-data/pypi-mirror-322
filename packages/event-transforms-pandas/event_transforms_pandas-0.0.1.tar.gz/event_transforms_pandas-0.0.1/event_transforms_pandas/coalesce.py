import pandas as pd
import numpy as np

def coalesce_events(
    df: pd.DataFrame,
    x_start: str,
    x_end: str,
    group: str | list[str] | None = None
) -> pd.DataFrame:
    
    if type(group) == str:
        groups = [group]
    elif group is None:
        groups = []
    elif type(group) == list:
        groups = group
    
    coalesced_df = pd.concat([
        df[groups +  [x_start]].rename({x_start: 'datetime'}, axis=1).assign(flag=1),
        df[groups +  [x_end]].rename({x_end: 'datetime'}, axis=1).assign(flag=-1),
    ]).sort_values('datetime')
    coalesced_df['simul_events'] = (
        coalesced_df.groupby(groups)['flag'].cumsum()
        if len(groups) > 0
        else coalesced_df['flag'].cumsum()
    )
    coalesced_df['prev_simul_events'] = (
        coalesced_df.groupby(groups)['simul_events'].shift(1).fillna(0)
        if len(groups) > 0
        else coalesced_df['simul_events'].shift(1).fillna(0)
    )

    coalesced_df['coalesced_event_start'] = np.where((coalesced_df['simul_events'] > 0) & (coalesced_df['prev_simul_events'] == 0), 1, 0)
    coalesced_df['index'] = (
        coalesced_df.groupby(group)['coalesced_event_start'].cumsum()
        if len(groups) > 0
        else coalesced_df['coalesced_event_start'].cumsum()
    )

    coalesced_df_2 = coalesced_df.groupby(groups + ['index']).agg({
        'datetime': ['min', 'max']
    }).reset_index()
    coalesced_df_2.columns = groups + ['index', x_start, x_end]

    result = pd.merge_asof(
        df.sort_values(x_start).rename({x_start: x_start + '_orig', x_end: x_end + '_orig'}, axis=1),
        coalesced_df_2.sort_values(x_start),
        left_on=x_start + '_orig',
        right_on=x_start,
        direction='backward',
        by=groups if len(groups) > 0 else None
    )

    return result



if __name__ == '__main__':

    
    from datetime import datetime, timedelta
    from typing import NamedTuple
    
    def as_date(n_secs: float) -> datetime:
        return datetime(1970, 1, 1) + timedelta(seconds=n_secs)
    
    class Event(NamedTuple):
        id: int
        group: str
        start: str
        end: str

    events = [
        Event(1, 'A', as_date(2), as_date(5)),
        Event(2, 'A', as_date(4), as_date(8)),
        Event(3, 'A', as_date(14), as_date(16)),
        Event(4, 'A', as_date(12), as_date(14)),
        Event(5, 'A', as_date(22), as_date(27)),
        Event(6, 'A', as_date(23), as_date(25)),
        Event(7, 'A', as_date(35), as_date(36)),
        Event(8, 'A', as_date(33), as_date(34)),
        Event(9, 'A', as_date(45), as_date(46)),
        Event(10, 'A', as_date(44), as_date(45)),
        Event(11, 'B', as_date(15), as_date(60)),
        Event(12, 'B', as_date(40), as_date(65)),
        Event(13, 'C', as_date(20), as_date(30)),
    ]

    df = pd.DataFrame(events)
    group = ['group']
    x_start = 'start'
    x_end = 'end'

    result = coalesce_events(df, x_start, x_end, group)
    print(result)
    