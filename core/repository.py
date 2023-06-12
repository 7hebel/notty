""" This module makes it easy to manage repositories. """

from dataclasses import dataclass
from typing import Any
from enum import Enum
import shutil
import random
import json
import stat
import os

from core.todo import __BLANK_CONTENT__ as BLANK_TODO
from core.hash import Hash, SHORT_LENGTH
import core.visuals as Visuals
import core.errors as Errors
import core.moment as Moment
from core.path import Path
import core.files as Files


SAVE_DATA_FILE: str = "notty.save"
REPO_STRUCTURE: dict[str, None | dict[str, Any]] = {
    "saves/": None,
    "bin/": None,
    "notes.txt": None,
    "todo.json": BLANK_TODO,
    "notty.meta": {},
    "notty.ignore": None,
}


class MetaKeys(Enum):
    """ These keys are used in notty.meta file. """
    DATE_CREATED = "date_created"
    DATE_EDITED = "date_edited"


@dataclass
class Save:
    """ Contains various information about save. """
    hash: Hash
    path: Path
    comment: str
    date_created: int


class Repository:
    """ Main Repository representation. """

    @staticmethod
    def _build_meta(meta_file_path: Path) -> None:
        """ Remove current content and write default to meta file. """
        now_timestamp = Moment.generate_timestamp()
        meta_content = {
            "date_created": now_timestamp,
            "date_edited": now_timestamp,
        }

        with open(str(meta_file_path), "w+", encoding="utf8") as file:
            json.dump(meta_content, file)

    @staticmethod
    def create(path: Path | str) -> "Repository":
        """ Create new repository in current location. """
        if isinstance(path, str):
            path = Path(path)

        src_path = path
        path = path // ".notty"

        with Visuals.ProcessCallback("Generate structure.", "Generated REPO.") as callback:
            if path.exists():
                raise Errors.RepositoryError("Already exists.")

            for parent_path in path.all_parents():
                if ".notty" in parent_path.list_dir() and (parent_path//".notty").is_dir():
                    raise Errors.RepositoryError(
                        f"There is repository in higher level directory: {parent_path}"
                    )

            for item, data in REPO_STRUCTURE.items():
                if item.endswith("/"):
                    (path // item).touch()
                    callback.success(f"created dir : {item}")
                    continue

                file = (path / item).touch()
                callback.success(f"created file: {item}")

                if data is None:
                    callback.info(f"keeping file blank: {item}")
                    continue

                with open(str(file), "w+", encoding="utf8") as file_obj:
                    json.dump(data, file_obj)
                callback.info(f"filled file: {item}")

            meta_path = path / "notty.meta"
            Repository._build_meta(meta_path)
            callback.success("filled meta")

        return Repository(src_path)


    def __init__(self, path: Path | str) -> None:
        if isinstance(path, str):
            path = Path(path)

        self.path: Path = path
        self.repo_path: Path = path // ".notty"
        self.saves_path: Path = self.repo_path // "saves"
        self.bin_path: Path = self.repo_path // "bin"

        try:
            self.is_initialized = self.check_initialized()
        except (FileNotFoundError, PermissionError, OSError, TypeError) as error:
            self.is_initialized = False
            Visuals.display_error(f"Cannot load repository: {error}")

    def _edit_meta(self, key: MetaKeys, value: Any) -> None:
        """ Edit notty.meta file's key. """

        meta_file = self.repo_path / "notty.meta"
        with open(str(meta_file), "r", encoding="utf8") as file:
            try:
                content = json.load(file)
            except json.decoder.JSONDecodeError:
                Visuals.display_warning("Meta file corrupted, rebuilt.")
                Repository._build_meta(meta_file)
                content = json.load(file)

        with open(str(meta_file), "w+", encoding="utf8") as file:
            if key not in MetaKeys:
                Visuals.display_warning(f"Modifying unknown meta key: {key}")
            content[key.value] = value
            json.dump(content, file)

    def _update_edited_date(self) -> None:
        """ Update repository's date_edited key to current timestamp. """
        self._edit_meta(MetaKeys.DATE_EDITED, Moment.generate_timestamp())

    def check_initialized(self) -> bool:
        """ Check if repository in current location is initialized. """

        if not self.repo_path.exists():
            return False

        repo_container = self.repo_path.list_dir(True)
        for item in set(REPO_STRUCTURE.keys()):
            if item.endswith("/"):
                item = item.split("/")[0]

            if item not in repo_container:
                return False
        return True

    def create_save(self, comment: str) -> None:
        """ Create new save with current code state. """

        with Visuals.ProcessCallback("Save current project's state.") as callback:
            date_created = Moment.generate_timestamp()
            callback.info("gathered meta data")

            hash_obj = Hash.generate(f"{date_created}--{comment}--{random.randint(0, 9999)}")
            callback.info(f"generated hash ({hash_obj.short})")

            save_path = self.saves_path // hash_obj.full
            save_path.touch()
            callback.success("created directory")

            meta_file = save_path / SAVE_DATA_FILE
            meta_file.touch()
            callback.success("created meta file")

            metadata = {
                "comment": comment,
                "date_created": date_created,
            }
            with open(str(meta_file), "w", encoding="utf8") as file:
                json.dump(metadata, file)
            callback.info("written metadata")

            def ignore_function(directory, contents):
                """ Create ignore_list that contains all ignored names.
                    Used in shutil.copytree as ignore parameter. """

                ignore_list = []
                for name in contents:
                    path = os.path.join(directory, name)
                    if os.path.isdir(path) and ".notty" in name:
                        ignore_list.append(name)
                    elif Files.name_in_patterns(name, self.get_ignore_patterns()):
                        ignore_list.append(name)
                return ignore_list

            shutil.copytree(
                str(self.path),
                str(save_path/""),
                ignore=ignore_function,
                dirs_exist_ok=True
            )

            callback.success("copied all")
            callback.success_message = f"Saved to: {str(hash_obj)}"
        self._update_edited_date()

    def load_save(self, hash_object: Hash) -> Save:
        """ Load all save's information and return it in new Save object. """

        save_path = self.saves_path / hash_object.full

        if not save_path.exists():
            raise Errors.SaveError("Save does not exists.")
        if not save_path.is_dir():
            raise NotADirectoryError("Path is not a directory.")

        full_hash = save_path.get_name()
        if len(full_hash) != 64:
            raise Errors.HashError(f"Invalid HASH's length: {len(full_hash)}/64")
        short_hash = full_hash[:SHORT_LENGTH]

        if SAVE_DATA_FILE in save_path.list_dir(True):
            data_file = save_path / SAVE_DATA_FILE
            with open(str(data_file), "r", encoding="utf8") as file:
                content: dict[str, Any] = json.load(file)

            comment = content.get("comment", False)
            date_created = content.get("date_created", False)

        else:
            comment = "?"
            date_created = None

        return Save(Hash(full_hash, short_hash), save_path, comment, date_created)

    def remove_save(self, save: Save) -> None:
        """ Delete save's directory. """

        save_path = self.saves_path // save.hash.full 
        os.chmod(str(save_path), stat.S_IWRITE)
        shutil.rmtree(str(save_path))
        self._update_edited_date()

    def get_all_saves(self) -> list[Save]:
        """ Return list of all saved code states in Save objects put together into one list. """
        return [self.load_save(Hash.generate_from_full(save_hash))
                for save_hash in self.saves_path.list_dir(True)]

    def find_save(self, save_hash: str) -> Save | None:
        """ Find save from hash in either short or full form and return Save
        object representing found save or None if save was not found. """

        if len(save_hash) not in (5, 64):
            Visuals.display_error(
                f"Invalid save_hash's length: (got {len(save_hash)}) expected: short=5 or full=64"
            )
            return None

        all_saves = self.get_all_saves()
        for save_obj in all_saves:
            if save_obj.hash == save_hash:
                return save_obj

        Visuals.display_error("Save with given hash not found.")
        return None

    def rollback_save(self, save_object: Save) -> None:
        """ Copy code state from given save_object to main directory. """

        if not (save_object.path/"").exists():
            raise FileNotFoundError("This save does not exists.")

        shutil.copytree(
            str(save_object.path/""),
            str(self.path/""),
            ignore=lambda _, contents: [
                name for name in contents
                if "notty" in name
            ],
            dirs_exist_ok=True
        )
        self._update_edited_date()

    def get_ignore_patterns(self) -> list[str]:
        """ Get all ignored patterns from notty.ignore. One line = one pattern. """

        with open(str(self.repo_path / "notty.ignore"), encoding="utf8") as file:
            return file.readlines()
