import numpy
from numpy.fft import fft2, ifft2, fftshift, ifftshift
from scipy import misc
from scipy import ndimage
from scipy.stats.stats import pearsonr
import math
import random


def fourierSpectrum(filename):
   A = ndimage.imread(filename, flatten=True)
   misc.imresize(A,(512,512), interp='bilinear', mode=None)
   unshiftedfft = numpy.fft.fft2(A)
   shiftedfft = fftshift(unshiftedfft)
   spectrum = numpy.log10(numpy.absolute(shiftedfft) + numpy.ones(A.shape))
   misc.imsave("images/spectrum-shifted.png", spectrum)


def randomVector(secretKey, length):
   random.seed(secretKey)
   return [random.choice([0,1]) for _ in range(length)]


def applyWatermark(imageMatrix, watermarkMatrix, alpha):
   shiftedDFT = fftshift(fft2(imageMatrix))
   watermarkedDFT = shiftedDFT + alpha * watermarkMatrix
   #misc.imsave("images/watermarked-spectrum.png", scaleSpectrum(watermarkedDFT))
   watermarkedImage = ifft2(ifftshift(watermarkedDFT))
   return watermarkedImage


def makeWatermark(imageShape, radius, Key, vectorLength=50):
   watermark = numpy.zeros(imageShape)
   center = (int(imageShape[0] / 2) + 1, int(imageShape[1] / 2) + 1)

   vector = randomVector(Key, vectorLength)

   x = lambda t: center[0] + int(radius * math.cos(t * 2 * math.pi / vectorLength))
   y = lambda t: center[1] + int(radius * math.sin(t * 2 * math.pi / vectorLength))
   indices = [(x(t), y(t)) for t in range(vectorLength)]

   for i,location in enumerate(indices):
      watermark[location] = vector[i]

   return watermark


def decodeWatermark(image, secretKey):
    fourierSpectrum(image)
    Img = "images/spectrum-shifted.png"
    vector = randomVector(secretKey, 50)
    myImg = ndimage.imread(Img, flatten=True)
    newvector = []
    radius = min(myImg.shape) / 4
    center = (int(myImg.shape[0] / 2) + 1, int(myImg.shape[1] / 2) + 1)

    x = lambda t: center[0] + int(radius * math.cos(t * 2 * math.pi / 50))
    y = lambda t: center[1] + int(radius * math.sin(t * 2 * math.pi / 50))
    indices = [(x(t), y(t)) for t in range(50)]

    for i,location in enumerate(indices):
        newvector.append(myImg[location])


    if (pearsonr(vector,newvector)[0] > 0.65):
        print(pearsonr(vector,newvector)[0])
        return "Watermark Present"
    else:
        print(pearsonr(vector,newvector)[0])
        return  "No Watermark Found"


def FFT(opendir,flag):
    opendir = opendir.encode('ascii')
    # filename = opendir.encode('ascii')
    # print(filename)
    # print(opendir)
    secretKey = 57846874321257
    alpha = 100000
    if(flag):
        theImage = ndimage.imread(opendir, flatten=True)
        watermark = makeWatermark(theImage.shape, min(theImage.shape) / 4, secretKey)
        #print(watermark)
        misc.imsave("images/FFT-watermark-spectrum.png", watermark)

        watermarked = numpy.real(applyWatermark(theImage, watermark, alpha))
        misc.imsave("images/FFT-watermarked.png",watermarked)

        return "images/FFT-watermarked.png"

    else:
        return decodeWatermark(opendir,secretKey)
