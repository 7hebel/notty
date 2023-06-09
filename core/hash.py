from dataclasses import dataclass
import hashlib

SHORT_LENGTH = 5

@dataclass
class Hash:
    full: str
    short: str

    @staticmethod
    def generate(data: str) -> "Hash":
        full_hash = hashlib.sha256(data.encode()).hexdigest()
        short_hash = full_hash[:SHORT_LENGTH]
        return Hash(full_hash, short_hash)
    
    @staticmethod
    def from_full(full_hash: str) -> "Hash":
        short_hash = full_hash[:SHORT_LENGTH]
        return Hash(full_hash, short_hash)


    def __eq__(self, value: str) -> bool:
        return str(value).strip().lower() in (self.full.lower(), self.short.lower())
    
    def __str__(self) -> str:
        return f"({self.short}) {self.full}"
