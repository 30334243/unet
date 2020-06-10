from PIL import Image

def jpg_to_png(path_jpg, path_png):
    im1 = Image.open(path_jpg)
    im1.save(path_png)