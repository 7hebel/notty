from pathlib import Path


class Repository:
    def __init__(self, path: Path | str) -> None:
        if isinstance(path, str):
            path = Path(path)
        
        self.path = path
        self.load()

    def check_metadata(self):
        pass

    def load(self):
        pass


