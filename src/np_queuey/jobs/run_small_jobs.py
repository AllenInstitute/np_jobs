import subprocess
import pathlib
import sys
import os

def main():
    subprocess.Popen(
        'huey_consumer np_queuey.hueys.dynamicrouting_behavior_session_mtrain_upload.huey',
        creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    
if __name__ == "__main__":
    main()