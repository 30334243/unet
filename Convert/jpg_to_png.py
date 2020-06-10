from PIL import Image
from pathlib import Path
import os

def jpg_to_png(path_jpg, path_dir_png):
    im1 = Image.open(path_jpg)
    im1.save(os.path.join(path_dir_png, os.path.basename(Path(path_jpg).with_suffix(".png"))))