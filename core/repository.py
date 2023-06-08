from pathlib import Path
import json
import os

from core.notes import __BLANK_CONTENT__ as BLANK_NOTES 
from core.todo import __BLANK_CONTENT__ as BLANK_TODO
import core.visuals as Visuals
import core.errors as Errors
import core.moment as Moment

"""
REPOSITORY:

.notty/
  saves/
    <hash>/
      save-<hash>.json
      CODE...
  
  notes.json
  todo.json
  notty.meta
"""

class Repository:
    def __init__(self, path: Path | str) -> None:
        if isinstance(path, str):
            path = Path(path)
        if not path.is_dir():
            path = Path(str(path) + "//")
        
        self.path = path
        self.repo_path = Path(str(self.path) + "/.notty/")
        self.saves_path = Path(str(self.repo_path) + "/saves/")
        self.notes_path = Path(str(self.repo_path) + "/notes.json")
        self.todo_path = Path(str(self.repo_path) + "/todo.json")
        self.meta_path = Path(str(self.repo_path) + "/notty.meta")
        self.is_initialized = self.check_initialized()
    
    def initialize(self):
        with Visuals.ProcessCallback("Initialize REPO") as Callback:
            if self.is_initialized:
                raise Errors.RepositoryError("Already initialized")
            Callback.info("starting...")

            self.repo_path.mkdir(exist_ok=True)

            Callback.info("created /.notty/")

            self.saves_path.mkdir(exist_ok=True)
            Callback.info("created /saves/")

            self.notes_path.touch(exist_ok=True)
            Callback.info("created notes file")

            self.todo_path.touch(exist_ok=True)
            Callback.info("created todos file")

            self.meta_path.touch(exist_ok=True)
            Callback.info("created meta file")   

            with open(self.notes_path, "w+") as file:
                json.dump(BLANK_NOTES, file)
            Callback.info("written notes")

            with open(self.todo_path, "w+") as file:
                json.dump(BLANK_TODO, file)
            Callback.info("written todo")

            now_timestamp = Moment.generate_timestamp()
            meta_content = {
                "ingore": [],
                "date_init": now_timestamp,
                "date_edit": now_timestamp,
            }
            with open(self.meta_path, "w+") as file:
                json.dump(meta_content, file)
            Callback.info("written meta")
        
        self.is_initialized = True

    def check_initialized(self):
        if not self.repo_path.exists():
            return False
        
        return True
        
r = Repository("E:/PythonProjects/nty")
# r.initialize()
