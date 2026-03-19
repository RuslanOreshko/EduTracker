from pathlib import Path
import shutil

from edutracker.core.config import settings

class LocalFileFetcher:
    def fetch(self, source_path: Path, destination_path: Path) -> Path:
        source_path = Path(source_path).resolve()
        destination_path = Path(destination_path).resolve()

        if not source_path.exists():
            raise FileNotFoundError(f"source file not found: {source_path}")

        if not source_path.is_file():
            raise ValueError(f"source path is not a file: {source_path}")
        
        destination_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(source_path, destination_path)

        return destination_path
    

def build_local_fetcher() -> LocalFileFetcher:
    return LocalFileFetcher()