from PIL import Image, ImageFilter, ExifTags
from os import listdir
from os.path import isfile, join

dWidth = 1920
dHeight = 1080
dSize = dWidth, dHeight


def resize(img):
    imgPath = join(".", "in", img)
    outPath = join(".", "out", img)
    print(f"Processing {imgPath}")
    im = Image.open(imgPath)

    orientation = 0
    for orientation in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation] == "Orientation":
            break

    exif = dict(im._getexif().items())

    if orientation in exif:
        if exif[orientation] == 3:
            im = im.transpose(Image.ROTATE_180)
        elif exif[orientation] == 6:
            im = im.transpose(Image.ROTATE_270)
        elif exif[orientation] == 8:
            im = im.transpose(Image.ROTATE_90)

    im.thumbnail(dSize, Image.ANTIALIAS)

    background = im
    if background.size[0] < dWidth:
        r = dWidth / background.size[0]
        background = background.resize((dWidth, int(background.size[1] * r)))
    if background.size[1] < dHeight:
        r = dHeight / background.size[1]
        background = background.resize((int(background.size[0] * r), dHeight))
    background = background.filter(ImageFilter.GaussianBlur(radius=25))
    l = int((background.size[0] - dWidth) / 2)
    r = int(background.size[0] - l)
    t = int((background.size[1] - dHeight) / 2)
    b = int(background.size[1] - t)
    background = background.crop((l, t, r, b))
    background.paste(
        im, (int((dWidth - im.size[0]) / 2), int((dHeight - im.size[1]) / 2))
    )
    background.save(outPath)


images = [f for f in listdir("./in") if isfile(join("./in", f))]
for img in images:
    resize(img)
