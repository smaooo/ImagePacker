import os
from posixpath import split
import sys
import getopt
from argparse import ArgumentParser 
from typing import Tuple, List
from PIL import Image, UnidentifiedImageError
from PIL.Image import Image as ImgType

# Function for checking if images exist
def imageCheck(img: str) -> None:
    # Print the error
    print('{} does not exist!'.format(img))
    # Ask for user to either terminate the program or continue without the mentioned image
    x = input('Do you want to continue? (yes/no)').upper()
    # Ask user to input yes/no as long as none of them are given
    while x:
        # If user input yes continue program
        if x == 'YES' or x == 'Y':
            break
        # If user input no terminate program
        elif x == 'NO' or x == 'N':
            sys.exit()
        # If yes or no are not given terminate the program
        x = input('Do you want to continue?').upper()

# Process command line arguments
def commandLine(argv) -> Tuple[str]:
    # Define the neede variables
    inputPath: str = ''     # Input/Source folder path
    images: str = ''        # List of images 
    outputPath: str = ''    # Output folder path
    outputName:str = ''     # Output/result name
    same: bool = False      # Same as input directory for saving the result
    padding = None          # Padding around images

    try:
        # Get options and their arguments
        opts = getopt.getopt(argv,"hi:l:d:o:p:")[0]
        # If -h option is not given
        if '-h' not in argv:
            # And if -o option is not given
            if '-o' not in argv:
                # Print error for reminding the usage
                print('usage:   ' + __file__ + ' -o <output name>')
                # Exit the program
                sys.exit(2)

    # Handle no options error
    except getopt.GetoptError as err:
        # Remind the usage
        print('usage: {} -o <output name>'.format(__file__))
        # Print the error
        print(err)
        # Terminate the program
        sys.exit(2)
    
    # Handle the given options
    for opt, arg in opts:
        # Handle -h (help) option
        if opt == '-h':
            print('Image Packer V1')
            print()
            print('usage:')
            print()
            print(__file__ + ' -o <output name>')
            print('Will collect all of the images in the same folder as the "{}" file and save the result with <output name>.'.format(__file__))
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
            print('-p arg             : Padding around the picture in pixel (e.g. -p 0). By default it is 10 pixel.')
            sys.exit()

        # Handle -i (input/source folder path) option
        elif opt == '-i':
            # Set the inputpath variable
            inputPath = arg
            # Check if the input path exists
            if not os.path.exists(inputPath):
                # Clean up the inputpath for checking again
                inputPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), inputPath.translate({ord(i): None for i in '\/'}))
                # If input path does not exist
                if not os.path.exists(inputPath): 
                    # Print the error
                    print("The source folder does not exist!")
                    # Terminate the program
                    sys.exit(2)

        # Handle -l (list of images) option
        elif opt == '-l':
            # Convert the string format of list to an actual list
            images = list(map(str, arg.strip('[]').split(',')))
        
        # Handle -d (destination folder path) option
        elif opt == '-d':
            # If the "same" argument given
            if arg == 'same':
                # Set same variable to True to use the input source folder as output folder
                same = True
            else:
                # Set the outputPath variable
                outputPath = arg
                # If output path does not exists
                if not os.path.exists(outputPath):
                    # Print that the folder does not exist
                    print('The given folder ({}) does not exist!'.format(outputPath))
                    # Get the non existing folder name
                    folderName = outputPath.split('/')[-1] if len(outputPath.split('/')) else outputPath.split('\\')[-1]
                    # Get the path
                    path = outputPath.strip(folderName)
                    # Ask user if he wants to a folder at the given path be created
                    x = input('Do you want a folder under the name "{}" to be created in {}? (yes/no)'.format(folderName, path)).upper()
                    # Ask the question as long as user is not giving yes/no answer
                    while x:
                        # If user input yes continue program
                        if x == 'YES' or x == 'Y':
                            try:
                                # Create the folder
                                os.mkdir(outputPath)
                            except OSError as error:
                                print(error)
                            break
                        # If user input no terminate program
                        elif x == 'NO' or x == 'N':
                            sys.exit()
                        # Ask the question again
                        x = input('Do you want a folder under the name {} to be created in {}? (yes/no)'.format(folderName, path)).upper()

        # Handle -o (output name) option  
        elif opt == '-o':
            # Set output name
            outputName = arg
        # Handle -p (padding) option
        elif opt == '-p':
            # Convert the argument to float
            if arg.isnumeric():
                padding = float(arg)
            else:
                # Print out the error
                print('The given padding is not a positive number!')
                # Give an example to the user
                print('usage: {} -o <output name> -p 5'.format(__file__))
                # Terminate program
                sys.exit(2)

    # If only an image list is given
    if len(inputPath) == 0 and len(images) > 0:
        # Check each image
        for img in images:
            # Check if the current image exists in the location
            if not os.path.exists(img):
                # If no ask user for an action
                imageCheck(img)    
    
    # If both input path and an image list is given 
    elif len(inputPath) > 0 and len(images) > 0:
        # Check each image
        for img in images:
            # Check if the current imagae exists in the location
            if not os.path.exists(os.path.join(inputPath, img)):
                # If no ask user for an action
                imageCheck(img)

    # If neither input path or an image list is given
    elif len(inputPath) == 0 and len(images) == 0:
        # Set the input path same as the python script location
        inputPath = os.path.dirname(os.path.realpath(__file__))

    # If either outputpath is not given or the "same" keyword is given
    if len(outputPath) == 0 or same:
        # Set output path same as input path
        outputPath = inputPath

    return inputPath, images, outputPath, outputName, padding

# Load images in a list from the given path
def loadImages(path: str, images: List[str]) -> List[ImgType]:
    
    # If only a list of images is given
    if len(images) > 0 and len(path) == 0:
        # Load images in a list
        for i in range(len(images)):
            images[i] = Image.open(images[i]).convert('RGBA')

    # If both input path and image list is given
    elif len(images) > 0 and len(path) > 0:
        # Join input path and images file name togther and load them in a list
        for i in range(len(images)):
            images[i] = Image.open(os.path.join(path, images[i])).convert('RGBA')

    # If only an input path is given
    elif len(images) == 0 and len(path) > 0:
        # Create an empty list for images
        images = []
        # List all of the files in the given input path
        dir = os.listdir(path)
        # Load each file while checking if it is an image file
        for img in dir:
            try:
                # If it is an image file add image to the list
                images.append(Image.open(os.path.join(path, img)).convert('RGBA'))

            # If it is not an image file don't add the file
            except (UnidentifiedImageError, PermissionError):
                pass
            
    # If image list is empty
    if len(images) == 0:
        # Print an error
        print('There is no image in the directory!')
        # Terminate the program
        sys.exit(2)
    
    return images

# Corect the size of each image and make them same size
def sizeCorrection(images: List[ImgType]) -> Tuple[List[ImgType],Tuple[int]]:
    
    # Create a list for different size
    sizes = []

    # Add each image size to the list
    for img in images:
        sizes.append(img.size)
    
    # Make sure there is no repetitive size in the list
    sizes = list(set(sizes))

    # Calculate the ratio for each size and add it to the ratios list
    ratios = [max(x) / min(x) for x in sizes]

    # Create a tuple for the selected size
    size = tuple()
    # If there is a difference between sizes in images
    if len(sizes) > 1:
        # Select the size with the nearest ratio to 1 (square)
        size = sizes[ratios.index(min(ratios))]

    # If all of the images are the same size don't do anything and return to main function
    else:
        return images, sizes[0]

    # If there was a difference between sizes, resize each image to the selected size
    for i in range(len(images)):
        images[i] = images[i].resize(size)

    return images, size

# Center all of the images 
def centering(images: List[ImgType], size: Tuple[int]) -> List[ImgType]:
    
    # Calculate the center point
    center = (int(size[0]/2), int(size[1]/2))

    # Center each image
    for i in range(len(images)):
        # Get the bounding box around the actual image area
        bound = images[i].getbbox()
        # Calculate the distance between min and max points in the bounding box
        distances = (int((bound[2] - bound[0])/2), int((bound[3] - bound[1])/2))
        # Create the new bounding box based on the center point of the image
        newBound = (center[0] - distances[0], center[1] - distances[1], center[0] + distances[0], center[1] + distances[1])
        # Crop the current image and save it in to a temp variable
        tmpImg = images[i].crop(images[i].getbbox())
        # Create a new blank image with the given size
        tmp = Image.new('RGBA', size)
        # Paste the temp image in the the blank image based on the given left and top points (so that is centered)
        tmp.paste(tmpImg, (newBound[0], newBound[1]))
        # Update the current image to the cenetered one
        images[i] = tmp

    return images

# Crop the empty area around the images
def cropping(images: List[ImgType], padding: float) -> List[ImgType]:
    
    # Check if the user has given a padding amount
    if padding == None:
        # If no set the padding to 10 pixel
        padding = 10
    
    # Get to smallest bounding box between all of the images
    bound = min([x.getbbox() for x in images])
    # Add the padding to the bounding box
    bound = (bound[0] - padding, bound[1] - padding, bound[2] + padding, bound[3] + padding)
    # Calculate distances between min and max points of the bounding box
    distances = (bound[2] - bound[0], bound[3] - bound[1])
    
    # Crop each image
    for i in range(len(images)):        
        # Get the current image bounding box
        tmpBound = images[i].getbbox()

        # Calculate the padding amount that should be added to each direction
        distx = abs(distances[0] - (tmpBound[2] - tmpBound[0])) /2
        disty = abs(distances[1] - (tmpBound[3] - tmpBound[1])) /2

        # Create new bounding box aound the image
        bound = (tmpBound[0] - distx, tmpBound[1] - disty, tmpBound[2] + distx, tmpBound[3] + disty)
        # Crop the image based on the new bounding box
        images[i] = images[i].crop(bound)

    return images


# Create the array of the given images
def compositor(images: List[ImgType], path: str, name: str) -> None:

    # Get the size of a single image
    size = images[0].size
    
    # Create a new black image with the size based on the number of images
    result = Image.new('RGBA', (size[0], size[1] * len(images)))

    # Add each image to the result image
    for img in images:
        # Paste current image to the result image at the given location
        result.paste(img, (0, size[1] * images.index(img)))

    # Save the result image ath the given path with the given name
    result.save(os.path.join(path,name) + '.png')
    # Alert user that the result image has been saved in the given location with the given name
    print('Output image has been saved in "{}" under the name "{}.png"!'.format(path, name))


# Main funtion
def main(argv) -> None:

    # Handle the command line arguments
    inputPath, images, outputPath, outputName, padding = commandLine(argv)
    # Load images into a list and save it to the variable
    images = loadImages(inputPath, images)
    # Correct the size of images and make them same size
    images, size = sizeCorrection(images)
    # Center images filled area
    images = centering(images, size)
    # Crop images based on the padding
    images = cropping(images, padding)
    # Combine images and create the result image
    compositor(images, outputPath, outputName)


if __name__ == "__main__":
    main(sys.argv[1:])
