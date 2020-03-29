# Importing Modules
from PyAstronomy import pyasl
import matplotlib.pyplot as plt
import math as m
import numpy as np
from scipy.interpolate import UnivariateSpline
import csv
import os
from astropy.io import fits
from decimal import Decimal

import norm as nm




# Define the path
path = "/home/slogle/Astro"

# Tell it where to look for the fits file
os.chdir(path)

# Give the file a name and define the path
fif = 'test1.fits'

# Extracting the data from the fits file
hdul = fits.open(fif)
hdul.info()
data = fits.getdata(fif)
header = fits.getheader(fif)


wavelength = np.array(data[0][0])
flux = np.array(data[0][1])
x = wavelength
y = flux
#Normalizing
norm_flux = nm.norm(flux)




#Smoothing
r=int(input("Please enter a r value: "))

alpha=(1.0)/(2.0*r+1.0)


new_flux=[]
new_wavelength=[]
j=r
k=r


while j<len(flux)-r:
  t=0
  t=sum(flux[(j-r):(j+r+1)])
  new_flux.append(alpha*t)
  j+=1

while k<len(wavelength)-r:
  t=0
  t=sum(wavelength[(k-r):(k+r+1)])
  new_wavelength.append(alpha*t)
  k+=1

new_wavelength=np.asarray(new_wavelength)
new_flux=np.asarray(new_flux)

plt.subplot(1,2,1)
plt.plot(x,y)
plt.title("Raw Wavelength vs Flux")
plt.xlabel("Wavelength (Ångstroms)")
plt.ylabel("Flux")

plt.subplot(1,2,2)
plt.plot(new_wavelength,new_flux)
plt.title("Normalized/Smoothed Wavelength vs Flux")
plt.xlabel("Wavelength (Ångstroms)")
plt.ylabel("Flux")
plt.show()


#format(new_wavelength, '.10f')
#format(new_flux, '.10f')

#Writing to Text file
L=len(new_flux)
def form_e(q):
    a = '%E' % q
    return a.split('E')[0].rstrip('0').rstrip('0').rstrip('.')+'E'+a.split('E')[1]


with open('Luke2020', 'w') as f:
    f.write("HD6268 (Flux) (Lin           npts="+str(L) +"\n")
    for i in range(0, L):
        f.write("%6s" % ("")) 
        f.write("%8s" % (form_e(new_wavelength[i])))
        f.write("%20s" % (form_e(new_flux[i])))
        f.write("\n")


