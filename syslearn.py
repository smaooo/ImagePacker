import os
import sys
import getopt
from argparse import ArgumentParser 
from typing import Tuple, List
from PIL import Image, UnidentifiedImageError
from PIL.Image import Image as ImgType

def imageCheck(img: str) -> None:
    print('{} does not exist!'.format(img))
    x = input('Do you want to continue?').upper()
    while x:
        
        if x == 'YES' or x == 'Y':

            break
        
        elif x == 'NO' or x == 'N':
            sys.exit()
        x = input('Do you want to continue?').upper()

def commandLine(argv) -> Tuple[str]:
    inputPath = ''
    images = ''
    outputPath = ''
    outputName = ''
    same = False

    try:
        opts, args = getopt.getopt(argv,"hi:l:d:o:")

        if '-h' not in argv:
            if '-o' not in argv:
                print('usage:   ' + __file__ + ' -o <output name>')
                sys.exit(2)

    except getopt.GetoptError as err:
        print('usage: syslearn.py -o <output name>')
        print(err)
        sys.exit(2)
    
    for opt, arg in opts:
        
        if opt == '-h':
            print('Image Packer V1')
            print()
            print('usage:')
            print()
            print(__file__ + ' -o <output name>')
            print('Will collect all of the images in the same folder as the *.py file and save the result with <output name>.')
            print()
            print('...')
            print('Options and arguments:')
            print('''-i arg             : {} will only use images inside the given source folder (e.g. D:/Foo/)''')
            print('''-l arg             : List of Images paths (e.g. -l [D:/Foo/img1.png,D:/Foo/img2.png,...])''')
            print('''-i arg -l arg      : Use only the given list of images in the given source folder
                     (e.g. -i D:/Foo/ -l [img1.png,img2.png,...]''')
            print('''-d arg             : Destination folder where you want to save the result''')
            print()
            print('                     -d <destination path>: will save the result in the given path')
            print('                     -d same: will save the result in the same folder as the source folder')
            print()
            print('-o arg             : Name of the result image file')
            sys.exit()

        elif opt == '-i':
            inputPath = arg
            if not os.path.exists(inputPath):
                inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputPath.translate({ord(i): None for i in '\/'}))
                if not os.path.exists(inputPath): 
                    print("The source folder does not exist!")
                    sys.exit(2)

        elif opt == '-l':
            images = list(map(str, arg.strip('[]').split(',')))
        elif opt == '-d':
            if arg == 'same':
                same = True
            else:
                outputPath = arg
                if not os.path.exists(outputPath):
                    try:
                        os.mkdir(outputPath)
                    except OSError as error:
                        print(error)
        elif opt == '-o':
            outputName = arg

    if len(inputPath) == 0 and len(images) > 0:
        for img in images:
            if not os.path.exists(img):
                imageCheck(img)    

    elif len(inputPath) > 0 and len(images) > 0:
        for img in images:
            if not os.path.exists(os.path.join(inputPath, img)):
                imageCheck(img)
    elif len(inputPath) == 0 and len(images) == 0:
        inputPath = os.path.dirname(os.path.realpath(__file__))

    if len(outputPath) == 0 or same:
        outputPath = inputPath

    return inputPath, images, outputPath, outputName


def loadImages(path: str, images: List[str]) -> List[ImgType]:
    if len(images) > 0 and len(path) == 0:
        for i in range(len(images)):
            images[i] = Image.open(images[i]).convert('RGBA')

    elif len(images) > 0 and len(path) > 0:
        for i in range(len(images)):
            images[i] = Image.open(os.path.join(path, images[i])).convert('RGBA')
    elif len(images) == 0 and len(path) > 0:
        
        images = []
        dir = os.listdir(path)
        for img in dir:
            try:
                images.append(Image.open(os.path.join(path, img)).convert('RGBA'))
            except (UnidentifiedImageError, PermissionError):
                pass
    if len(images) == 0:
        print('There is no image in the directory!')
        sys.exit(2)
    
    return images


def sizeCorrection(images: List[ImgType]) -> Tuple[List[ImgType],Tuple[int]]:
    sizes = []
    for img in images:
        sizes.append(img.size)
    sizes = list(set(sizes))
    ratios = [max(x) / min(x) for x in sizes]

    size = tuple()
    if len(sizes) > 1:
        
        size = sizes[ratios.index(min(ratios))]
    else:
        size = sizes[0]

    for i in range(len(images)):
        images[i] = images[i].resize(size)
    return images, size


def centering(images: List[ImgType], size: Tuple[int]) -> List[ImgType]:
    
    center = (int(size[0]/2), int(size[1]/2))
    for i in range(len(images)):
        bound = images[i].getbbox()
        distances = (int((bound[2] - bound[0])/2), int((bound[3] - bound[1])/2))
        newBound = (center[0] - distances[0], center[1] - distances[1], center[0] + distances[0], center[1] + distances[1])
        tmpImg = images[i].crop(images[i].getbbox())
        tmp = Image.new('RGBA', size)
        tmp.paste(tmpImg, (newBound[0], newBound[1]))
        images[i] = tmp

    return images


def cropping(images: List[ImgType]) -> List[ImgType]:
    
    bound = min([x.getbbox() for x in images])
    distances = (bound[2] - bound[0], bound[3] - bound[1])
    for i in range(len(images)):        
        tmpBound = images[i].getbbox()
        distx = abs(distances[0] - (tmpBound[2] - tmpBound[0])) /2
        disty = abs(distances[1] - (tmpBound[3] - tmpBound[1])) /2

        
        images[i] = images[i].crop((tmpBound[0] - distx, tmpBound[1] - disty, tmpBound[2] + distx, tmpBound[3] + disty))

    return images


def compositor(images: List[ImgType], path: str, name: str) -> None:
    size = images[0].size
    result = Image.new('RGBA', (size[0], size[1] * len(images)))

    for img in images:
        result.paste(img, (0, size[1] * images.index(img)))
    result.save(os.path.join(path,name) + '.png')
    print('Output image has been saved in "{}" under the name "{}.png"!'.format(path, name))



def main(argv) -> None:
    inputPath, images, outputPath, outputName = commandLine(argv)
    
    images = loadImages(inputPath, images)
    
    images, size = sizeCorrection(images)
    images = centering(images, size)
    
    images = cropping(images)
    compositor(images, outputPath, outputName)


if __name__ == "__main__":
    main(sys.argv[1:])
