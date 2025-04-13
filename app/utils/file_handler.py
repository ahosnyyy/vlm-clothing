import tempfile
import os
from fastapi import UploadFile

def save_spooled_temp_image(upload: UploadFile) -> str:
    """Save image to a spooled temp file, then write it to disk and return path."""
    with tempfile.SpooledTemporaryFile(max_size=5_000_000, suffix=".jpg") as spooled_file:
        spooled_file.write(upload.file.read())
        spooled_file.seek(0)

        # Create a real temp file Ollama can read from
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as disk_file:
            disk_file.write(spooled_file.read())
            return disk_file.name  # Return actual file path

def remove_temp_image(path: str):
    try:
        os.remove(path)
    except OSError:
        pass
