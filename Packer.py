from PIL import Image
import os
import sys


source = "D:\King Assessment\Tiles\\"
dir = os.listdir(source)
images = []
sizes = []

for pic in dir:
    images.append(Image.open(source + pic).convert('RGBA'))

for img in images:
    sizes.append(img.size)
sizes = list(set(sizes))

size = (0,0)
if len(sizes) > 1:
    size = min(sizes)
else:
    size = sizes[0] 

result = Image.new('RGBA', (size[0], size[1] * len(images)), (250, 250, 250))

for img in images:
    reImg = img.resize(size, Image.BILINEAR)
    result.paste(reImg, (0, size[1] * images.index(img)))
    
result.save(source + 'result' + '.png', 'png')



    
