import pathlib
from typing import Generator

import np_session
import np_tools

from np_jobs import PipelineQCQueue

Q = PipelineQCQueue()

def get_sessions() -> Generator[np_session.Session, None, None]:
    for session_folder in np_session.Projects.DRDG.state['ephys']:
        session = np_session.Session(session_folder)
        
        yield session

def add_sessions():
    for session in get_sessions():
        Q.add_or_update(session)

def create_qc_folder():
    """Dumps symlinks to qc.html in a single folder, for easier access"""
    root = pathlib.Path("//allen/programs/mindscope/workgroups/dynamicrouting/dynamic_gating/qc/summary_htmls")
    root.mkdir(parents=True, exist_ok=True)
    for session in get_sessions():
        np_tools.symlink(session.qc_path / 'qc.html', root / f'{session}.html' )

def delete_qc_folders():
    for session in np_session.sessions():
        for name in (
            'qc.html',
            'qc.css',
            'single_page_img_json_report.css',
            'session_meta.json',
            'specimen_meta.json',
            ):
            p = session.npexp_path / 'qc' / name
            if p.is_dir():
                for f in p.rglob('*'):
                    try:
                        f.unlink()
                    except OSError:
                        print(session, ' failed to delete ', f.name)
                        continue
                try:
                    p.unlink()
                except OSError:
                    print(session, ' failed to delete ', p.name)
                    continue
            
if __name__ == "__main__":
    # add_sessions()
    create_qc_folder()
    # delete_qc_folders()