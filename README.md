# FTbg
Background removal using Fourier Transform


This handy python script takes a FITS image, perform Fourier transform, and separate low- and high-spatial frequency components by a user-specified cut. Both components are then inverse FT back to image domain. It can be used to remove large-scale background/foreground emission in many astrophysical applications.

Input: original FITS image
Outputs: background and structure images

If you find this script useful, please cite our paper:
[Large-scale filaments associated with Milky Way spiral arms](http://adsabs.harvard.edu/abs/2015MNRAS.450.4043W).
