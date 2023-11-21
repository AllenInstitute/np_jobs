from __future__ import annotations

from pathlib import Path
from typing import Generator, Tuple

import np_session
import np_tools
from typing_extensions import Literal

from np_jobs import PipelineSortingQueue

Q = PipelineSortingQueue()

def get_sessions_with_missing_metrics() -> Generator[Path, None, None]:
    for session in np_session.Projects.DRDG.state['ephys']:
        session = np_session.Session(session)
        if not isinstance(session, np_session.PipelineSession):
            print('skipped', session)
            continue
        if len(session.metrics_csv) < len(session.probes_inserted):
            yield session
        
def get_probes_missing_sorted_data(session: np_session.PipelineSession) -> tuple[str, ...]:
    if session.probes_inserted is None:
        raise ValueError(f'No probes inserted for {session}')
    return tuple(probe for probe in session.probes_inserted if probe not in session.probe_letter_to_metrics_csv_path.keys())
            
    
def sorted_paths() -> Generator[Path, None, None]:
    for session in np_session.Projects.DRDG.state['ephys']:
        if not isinstance(session, np_session.PipelineSession):
            print('skipped', session)
            continue
        for csv in session.metrics_csv:
            yield csv.parent
            
def paths_to_ctimes(parent: Path) -> Tuple[float, ...]:
    return tuple(p.stat().st_ctime for p in parent.iterdir())

def range_hours(parent: Path) -> float:
    ctimes = paths_to_ctimes(parent)
    return (max(ctimes) - min(ctimes)) / 3600


def add_sessions_with_sorted_data_mismatch():

    for p in sorted_paths():
        if range_hours(p) > 7:
            session = p.parent.parent.parent.name
            probe = p.parent.parent.name.split('probe')[-1][0]
            print(f'{range_hours(p):.1f} h  {session} probe{probe}')
            if session in Q:
                probe += Q[session].probes
            Q.add_or_update(session, probes=probe)


def add_sessions_with_missing_metrics():
    for session in get_sessions_with_missing_metrics():
        print(session)
        Q.add_or_update(session, probes=''.join(get_probes_missing_sorted_data(session)))
        
        
if __name__ == "__main__":
    add_sessions_with_missing_metrics()