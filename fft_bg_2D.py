# Usage
# python fft_bg_2D.py 'image.fits' 'im.st.fits' 'im.bg.fits' 0.9  1.0
# see below for the meanings of the arguments


from scipy import fftpack
import numpy as np
import pyfits

import sys
total = len(sys.argv)
cmdargs = str(sys.argv)

#print ("The total numbers of args passed to the script: %d " % total)
print ("Args list: %s " % cmdargs)
print ("imf, st, bg, frac, scale")


# arguments
imf = str(sys.argv[1]) # input image file
stf = str(sys.argv[2]) # output structure file
bgf = str(sys.argv[3]) # output background file
frac  = float(sys.argv[4]) # fraction of max power spectrum, to separate hight and low spatial freq
scale = float(sys.argv[5]) # factor to scale background, usually 1.0



# FFT start_________________________________________________________________________________
im = pyfits.getdata(imf)
# fill NAN pixels with 0
mask_nan = np.isnan(im)
im[mask_nan]=0.0

cim = im.copy()		# copy for further use
hd = pyfits.getheader(imf)

# Take FFT of the image. *1.0 to make the dtype right
F1 = fftpack.fft2(cim*1.0)

# Now shift the quadrants around so that low spatial frequencies are in
# the center of the 2D fourier transformed image.
F2 = fftpack.fftshift( F1 )

# Calculate a 2D power spectrum
# for plot
ps2 = np.abs( F2 )**2
ps2 = np.log10(ps2)
# for making mask
ps1 = np.abs( F1 )**2
ps1 = np.log10(ps1)


# make the mask used to separate high- and low- spatial frequency
mask0 = ps1 <= np.max(ps1)*frac
mask1 = ps1 >  np.max(ps1)*frac

# iFFT back to image domain
high = fftpack.ifft2( F1*mask0 ).real # high spatial freq
low  = fftpack.ifft2( F1*mask1 ).real # low  spatial freq
bg = low.copy()		# background
bg *= np.median(im)/np.max(bg) # background cannot be higher than median value in original image
bg *= scale  #optional scalling factor, usually 1.0
st = im.copy()-bg	# structure

#FFT end_________________________________________________________________________________



# Write out FITS
st[mask_nan] = np.nan  # mask out where original data was NAN
st[ st<5.0 ] = np.nan  # mask out negative (or unlikely small value) pixels
# write out structure file
tmp = pyfits.PrimaryHDU(data=st, header=hd)
tmp.writeto(stf, clobber=True)
# write out background file
tmp = pyfits.PrimaryHDU(data=bg, header=hd)
tmp.writeto(bgf, clobber=True)

