from pathlib import Path

class Repository:
    def __init__(self, path: Path | str) -> None:
        if isinstance(path, str):
            path = Path(path)
        
        self.path = path
        self.load()

    def load(self):
        pass
