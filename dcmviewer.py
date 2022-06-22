import matplotlib.pyplot as plt
import numpy as np
from pydicom import dcmread
import sys
import getopt

arg = sys.argv
opts,argv = getopt.getopt(arg[1:],"i:l:h:o:b:c:de")


def conversion(im):
  im = im - np.amin(im)
  n = np.amax(im)/255
  im = np.abs(im*(1/n))
  return im

display = True

arguments = np.zeros(8) #stocks an "activation number" for each arguments

try:
  #for each arguments, we activate the corresponding index in arguments[]
  #We also stock the values passed in the arguments.
  #The order of the arguments is not important
  for opt, arg in opts: 
      if opt in ['-i']:
        ds = dcmread(arg)
        arguments[0] = 1

      elif opt in ['-d']:
        arguments[1] = 1

      elif opt in ['-l']:
        l = int(arg)
        arguments[2] = 1

      elif opt in ['-h']:
        h = int(arg)
        arguments[3] = 1
          
      elif opt in ['-b']:
        arguments[4] = 1
        b = int(arg)

      elif opt in ['-c']:
        arguments[5] = 1
        c = float(arg)

      elif opt in ['-o']:
        arguments[6] = 1
        save = arg
      
      elif opt in ['-e']:
        arguments[7] = 1

  #If an argument is activated then we execute is corresponding code 
  if(arguments[0] == 1):
    im = ds.pixel_array


  if(arguments[1] == 1):
    display = False
    print("The size of the image is " + str(ds.Columns) + " * " + str(ds.Rows))
    print("The number of samples per pixel is " + str(ds.SamplesPerPixel))
    print("The number of bits per samples is " + str(ds.BitsStored))
    print("Maximum value: " + str(np.amax(im)))
    print("Minimum value: " + str(np.amin(im)))

  if(arguments[2] == 1):
    im = np.where(im < l, l, im)

  if(arguments[3] == 1):
    im = np.where(im > h, h, im)
    if(h <= l):
      print("h must be higher than l !!!")

  im = conversion(im) #For the next arguments, we need ton convert the pixel array into
                      #a classic image array (with value between 0 and 255)
                
  if(arguments[7] == 1): # Not functional
    hist, count = np.histogram(im, bins = 256)
    cdf = np.cumsum(hist)/(im.size)
    imbis = np.zeros([im.shape[0], im.shape[1]])
    for i in range(256):
      imbis = np.where(im == i, 255*cdf[i], imbis)
    im = np.around(imbis)



  if(arguments[4] == 1):
    im = im + b
    im = np.where(im < 0, 0, im)
    im = np.where(im > 255, 255, im)
    if(b < -255 or b > 255):
      print("b must be between -255 and 255 !!!")

  if(arguments[5] == 1):
    m = np.mean(im)
    im = im - m
    im = im * c
    im = im + m
    im = np.around(im)
    im = np.where(im < 0, 0, im)
    im = np.where(im > 255, 255, im)

  if(arguments[6] == 1):
    display = False
    plt.imsave(save, im, cmap = plt.cm.gray, vmin = 0, vmax = 255 )

  if(display):
    plt.figure()
    plt.imshow(im, cmap = plt.cm.gray, vmin = 0, vmax = 255)
    plt.show()

except:
  print("There's one or more arguments which are not correct")
  print("-i path/file.dcom: Specify your .dcom file (Mandatory)")
  print("-l n: Low value for windowing the image")
  print("-h n: High value for windowing the image (must be lower than the -l value)")
  print("-b n: Add n to each pixel to increase or lower the luminosity (must be between -255 and 255)")
  print("-c n: adjust the contrast by a factor n (n must be positive)")
  print("-d if you want to print the characteristics of the image instead of display the image")
  print("-o path/save.png/jpg/jpeg :if you want to save the image instead of display it")
  print("-e equalize the histogram of the image")

