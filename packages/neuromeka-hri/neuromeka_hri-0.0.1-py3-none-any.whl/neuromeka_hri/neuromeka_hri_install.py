import shutil
from pathlib import Path
import sys

def main():    
    # Copy data to user's home directory
    data_src = Path(__file__).parent / "apk_file"
    data_dst = Path.home() / "neuromeka-hri"
    if data_src.exists():
        try:
            if data_dst.exists():
                shutil.rmtree(data_dst)
            shutil.copytree(data_src, data_dst)
            print(f"Copied data to: {data_dst}")
        except PermissionError as e:
            print("Permission error: ", e)
        except Exception as e:
            print("Failed to copy data: ", e)
