# -*- coding=utf-8 -*-
from PIL import Image
import base64

def get_image_base64():
    path = 'C:\\tmp\\test.jpg'
    im = Image.open(path)
    size = im.height, im.width
#    if im.height > 2000:
#        size = 2000, 2000 * (im.width / im.height)
    im.thumbnail(size)
    im.save(path)

    with open(path, 'rb') as f:
        base64_data = base64.b64encode(f.read())
    return base64_data
