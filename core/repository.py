from dataclasses import dataclass
from pathlib import Path
import shutil
import random
import json
import stat
import os

from core.notes import __BLANK_CONTENT__ as BLANK_NOTES 
from core.todo import __BLANK_CONTENT__ as BLANK_TODO
from core.hash import Hash, SHORT_LENGTH
import core.visuals as Visuals
import core.errors as Errors
import core.moment as Moment
import core.files as Files

"""
REPOSITORY:

.notty/
  bin/
  saves/
    <hash>/
      save-<hash>.json
      CODE...
  
  notes.json
  todo.json
  notty.meta
"""


SAVE_DATA_FILE = "notty.save"
REPO_STRUCTURE = {
    "saves/": None,
    "bin/": None,
    "notes.json": BLANK_NOTES,
    "todo.json": BLANK_TODO,
    "notty.meta": {},
}

@dataclass
class Save:
    hash: Hash
    path: Path
    comment: str
    date_created: int
        

class Repository:

    @staticmethod
    def create(path: Path | str) -> "Repository":
        if isinstance(path, str):
            src_path = path
            path = Path(path)

        path = Path(str(path) + "/.notty/")
 

        with Visuals.ProcessCallback("Generate structure.", "Generated REPO.") as Callback:

            if path.exists():
                raise Errors.RepositoryError("Already exists.")

            for parent_path in path.parents:
                if ".notty" in os.listdir(str(parent_path)) and os.path.isdir(str(parent_path)+"/.notty"):
                    raise Errors.RepositoryError(f"There is repository in higher level directory: {parent_path}")

            for item, data in REPO_STRUCTURE.items():
                if item.endswith("/"):
                    directory = Path(str(path) + "/" + item)
                    directory.mkdir(parents=True)
                    Callback.success(f"created dir : {directory}")
                    
                else:
                    file = Path(str(path) + "/" + item)
                    file.touch()
                    Callback.success(f"created file: {file}")

                    with open(str(file), "w+") as file_obj:
                        json.dump(data, file_obj)
                    Callback.info(f"filled file: {file}")
            
            meta_file = Path(str(path) + "/" + "notty.meta")
            now_timestamp = Moment.generate_timestamp()
            meta_content = {
                "date_created": now_timestamp,
                "date_edited": now_timestamp,
            }
            with open(str(meta_file), "w+") as file:
                json.dump(meta_content, file)
            Callback.success("filled meta")

        return Repository(src_path)

    def __init__(self, path: Path | str) -> None:
        if isinstance(path, str):
            path = Path(path)
        
        self.path = path
        self.repo_path = Path(str(self.path) + "/.notty/")
        self.saves_path = self.repo_path.joinpath("saves/")

        try:
            self.is_initialized = self.check_initialized()
        except Exception as error:
            self.is_initialized = False
            Visuals.Message.error(f"Cannot load repository: {error}")

    def check_initialized(self) -> bool:
        if not self.repo_path.exists():
            return False
        
        repo_container = os.listdir(str(self.repo_path))
        for item in set(REPO_STRUCTURE.keys()):
            if item.endswith("/"):
                item = item.split("/")[0]
            
            if item not in repo_container:
                return False
            
        return True
    
    def create_save(self, comment: str):
        with Visuals.ProcessCallback("Save current project's state.") as Callback:
            date_created = Moment.generate_timestamp()
            Callback.info("gathered meta data")

            hash_obj = Hash.generate(f"{date_created}--{comment}--{random.randint(0, 9999)}")
            Callback.info(f"generated hash ({hash_obj.short})")

            save_path = Path(str(self.saves_path) + "/" + hash_obj.full)
            save_path.mkdir()
            Callback.success("created directory")

            meta_file = Path(str(save_path) + "/" + SAVE_DATA_FILE)
            meta_file.touch()
            Callback.success("created meta file")

            metadata = {
                "comment": comment,
                "date_created": date_created, 
            }
            with open(str(meta_file), "w") as file:
                json.dump(metadata, file)
            Callback.info("written metadata")

            subpaths = Files.get_paths(self.path, [SAVE_DATA_FILE], [".notty"])
            Callback.info(f"found {len(subpaths)} items")

            shutil.copytree(
                str(self.path),
                str(save_path)+"/",
                ignore=lambda directory, contents: [
                    name for name in contents
                    if os.path.isdir(os.path.join(directory, name)) and ".notty" in name
                ],
                dirs_exist_ok=True
            )

            Callback.success("copied all")
            Callback.success_message = f"Saved to: ({hash_obj.short}) {hash_obj.full}"

    def load_save(self, hash: Hash) -> Save:
        save_path = Path(str(self.saves_path) + "/" + hash.full)

        if not save_path.exists():
            raise Errors.SaveError("Save does not exists.")

        if not save_path.is_dir():
            raise NotADirectoryError("Path is not a directory.")
        
        full_hash = save_path.name

        if len(full_hash) != 64:
            raise Errors.HashError(f"Invalid HASH's length: {len(full_hash)}/64")
        
        short_hash = full_hash[:SHORT_LENGTH]

        if SAVE_DATA_FILE in os.listdir(save_path):       
            data_file = Path(str(save_path) + "/" + SAVE_DATA_FILE)
            with open(data_file, "r") as file:
                content: dict = json.load(file)

            date_created = content.get("date_created", False)
            comment = content.get("comment", False)
        else:
            date_created = None
            comment = None
        
        return Save(Hash(full_hash, short_hash), save_path, comment, date_created)

    def remove_save(self, save: Save):
        save_path = str(self.saves_path) + "/" + save.hash.full + "/"
        os.chmod(save_path, stat.S_IWRITE)
        shutil.rmtree(save_path)

    def get_all_saves(self) -> list[Save]:
        saves = []
        for save_hash in os.listdir(str(self.saves_path)):
            loaded_save = self.load_save(Hash.from_full(save_hash))
            if loaded_save != False:
                saves.append(loaded_save)
        return saves

    def find_save(self, save_hash: str) -> Save | None:
        if len(save_hash) not in (5, 64):
            Visuals.Message.error(f"Invalid save_hash's length: (got {len(save_hash)}) expected: short=5 or full=64")
            return

        all_saves = self.get_all_saves()
        for save_obj in all_saves:
            if save_obj.hash == save_hash:
                return save_obj
        else:
            Visuals.Message.error("Save with given hash not found.")
            return None

    def rollback_save(self, save_obj: Save):
        save_path = save_obj.path

        shutil.copytree(
            str(save_path)+"/",
            str(self.path),
            ignore=lambda _, contents: [
                name for name in contents
                if "notty" in name
            ],
            dirs_exist_ok=True
        )
        
