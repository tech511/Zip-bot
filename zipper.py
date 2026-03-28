import os
import zipfile
from config import ZIP_DIR, SPLIT_SIZE

def create_zip(uid):
    path = f"{ZIP_DIR}/{uid}_part1.zip"
    return zipfile.ZipFile(path, "w"), path, 1

def check_split(zip_path, part):
    if os.path.exists(zip_path) and os.path.getsize(zip_path) > SPLIT_SIZE:
        part += 1
        new_path = zip_path.replace(f"part{part-1}", f"part{part}")
        return new_path, part
    return zip_path, part
