# ImagePacker
ImagePacker is a command line program written in Python for creating vertical image array of the given images.

## Usage
(py/py3/python/python3) ImagePacker.py -o "output name"

Will collect all of the images in the same folder as the " file and save the result with <output name>.

  
# Options and Arguments
-i arg             : will only use images inside the given source folder (e.g. -i D:/Foo/)
  
-l arg             : List of Images paths (e.g. -l [D:/Foo/img1.png,D:/Foo/img2.png,...])
  
-i arg -l arg      : Use only the given list of images in the given source folder (e.g. -i D:/Foo/ -l [img1.png,img2.png,...]
  
-d arg             : Destination folder where you want to save the result
  
                     -d <destination path>: will save the result in the given path
                     -d same: will save the result in the same folder as the source folder
  
-o arg             : Name of the result image file
  
-p arg             : Padding around the picture in pixel (e.g. -p 0). By default it is 10 pixel.
