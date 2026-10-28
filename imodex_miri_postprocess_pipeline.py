#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 11:18:27 2022

Pipeline for postprocessing of JWST/MIRI coronagraphic data for exoplanets and circumstellar disks observations

Last update : 25/03/2024

@author: cperrot
"""


import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits # type: ignore
import glob
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.optimize import lsq_linear
from numpy.linalg import eig
#from scipy import ndimage
#import glob, os
import math
from scipy.ndimage import generic_filter, distance_transform_edt#, gaussian_filter
import copy
import kneed


### centre corono (Baudoz et al.)
# F1065C : x0 = 120.25 / y0 = 112.03
# F1140C : x0 = 119.77 / y0 = 112.16
# F1550C : x0 = 119.71 / y0 = 113.28


#Conversion Jy to W/m2/µm
def flux_Jy_to_Wm(wl,flux) :
    return np.array(flux)/(333564095198152064*1e-6*np.array(wl)**2)

#Conversion W/m2/µm to Jy
def flux_Wm_to_Jy(wl,flux) :
    return np.array(flux)*(333564095198152064*1e-6*np.array(wl)**2)




#### Data mise en forme (loading, median, background subtraction, badpixel correction)

### function to save fits files
def save_fits(image,filename,over=True):
    hdu = fits.PrimaryHDU()
    hdu.data = image
    if over == True:
        hdu.writeto(filename,overwrite=over)
    if over == False:
        print('not saved (overwrite=False)')

#save fits with header
def save_fits_h(image,filename,header,over=True):
    hdu = fits.PrimaryHDU()
    hdu.data = image
    if header:
        hdu.header = header
    if over == True:
        hdu.writeto(filename,overwrite=over)
    if over == False:
        print('not saved (overwrite=False)')
        
        
### function to read fits cube with 2, 3 or 4 dimension - option to resize the cubes
def load_cube(path, affix, xdim=0, ydim=0, x0=120, y0=112, silent=True, **kwargs):
    liste= glob.glob(path+'*'+affix+'.fits')
    liste.sort()
    file0 = fits.open(liste[0])
    nimg = np.shape(liste)[0]
    ndim=file0[1].header['NAXIS']
    dimx=file0[1].header['NAXIS1']
    dimy=file0[1].header['NAXIS2']
    if silent:
        print('Loading of '+str(nimg)+' cubes.')
        print('Number of dimension : '+str(ndim))

    file0.close()
    
    if xdim == 0:
        xdim = dimx
        x0   = xdim//2
    if ydim == 0:
        ydim = dimy
        y0   = ydim//2
    if silent:
        print('Initial images size (px) : '+str(dimx)+' / '+str(dimy))
        print('New images size (px)     : '+str(xdim)+' / '+str(ydim))
    
    if ndim == 3:
        nframe=file0[1].header['NAXIS3']
        if silent:
            print('Number of frames : '+str(nframe))
    
    if ndim == 4:
        nframe=file0[1].header['NAXIS4']
        ngroup=file0[1].header['NAXIS3']
        if silent:
            print('Number of frames : '+str(nframe))
            print('Number of groups : '+str(ngroup))
        
    if ndim > 4:
        raise Exception("Okay, Houston, I believe we have had a problem here (ndim > 4)", ndim)

    
    if ndim == 2:
        if nimg > 1:
            cube = []
            header = []
            for i in liste:
                file = fits.open(i)
                header.append([file[0].header,file[1].header])
                cube.append(file[1].data[y0-ydim//2:y0+ydim//2,x0-xdim//2:x0+xdim//2])
                file.close()
            cube = np.array(cube)
        else:
            file = fits.open(liste[0])
            header = [file[0].header,file[1].header]
            cube = file[1].data[y0-ydim//2:y0+ydim//2,x0-xdim//2:x0+xdim//2]
            file.close
    
    if ndim == 3:
        if nimg > 1:
            cube = [] 
            header = []
            for i in liste:
                file = fits.open(i)
                header.append([file[0].header,file[1].header])
                cube.append(file[1].data[:,y0-ydim//2:y0+ydim//2,x0-xdim//2:x0+xdim//2])
                file.close()
            cube = np.array(cube)
        else:
            file = fits.open(liste[0])
            header = [file[0].header,file[1].header]
            cube = file[1].data[:,y0-ydim//2:y0+ydim//2,x0-xdim//2:x0+xdim//2]
            file.close
            
    if ndim == 4:
        if nimg > 1:
            cube = [] 
            header = []
            for i in liste:
                file = fits.open(i)
                header.append([file[0].header,file[1].header])
                cube.append(file[1].data[:,:,y0-ydim//2:y0+ydim//2,x0-xdim//2:x0+xdim//2])
                file.close()
            cube = np.array(cube)
        else:
            file = fits.open(liste[0])
            header = [file[0].header,file[1].header]
            cube = file[1].data[:,:,y0-ydim//2:y0+ydim//2,x0-xdim//2:x0+xdim//2]
            file.close

    return cube, header


#detect pixels with high/low value compare to their neighbour and put them as NaN. Sigma clipping method. 
# outdated, used instead remove_bad_pixel() from Jonas
def sigma_clip_jwst(cube, sig=3):
    print("outdated, use remove_bad_pixel() function by Jonas instead")
    return []
    ndim = len(np.shape(cube))
    ydim = np.shape(cube)[-2]
    xdim = np.shape(cube)[-1]
    if ndim == 2:
        for i in range(ydim):
            for j in range(xdim):
                if (i <= 1) or (j <= 1) or (i >= ydim-3) or (j >= xdim-3):
                    toto=0
                else:
                    med= np.nanmedian(cube[i-2:i+3,j-2:j+3])
                    std= np.nanstd(cube[i-2:i+3,j-2:j+3])
                    if (cube[i,j] >= med+sig*std) or (cube[i,j] <= med-sig*std):
                        cube[i,j] = math.nan
    elif ndim == 3:
        for k in range(np.shape(cube)[0]):
            for i in range(ydim):
                for j in range(xdim):
                    if (i <= 1) or (j <= 1) or (i >= ydim-3) or (j >= xdim-3):
                        toto=1
                    else:
                        med= np.nanmedian(cube[k,i-2:i+3,j-2:j+3])
                        std= np.nanstd(cube[k,i-2:i+3,j-2:j+3])
                        if (cube[k,i,j] >= med+sig*std) or (cube[k,i,j] <= med-sig*std):
                            cube[k,i,j] = math.nan

    return cube

# transform NaN value to lisible value. For clean and readable image only, interpolation is at your own risk !
def clean_image_nan(cube):
    ndim = len(np.shape(cube))
    ydim = np.shape(cube)[-2]
    xdim = np.shape(cube)[-1]
    if ndim == 2:
        bpmap = np.where(np.isnan(cube))
        for k in range(len(bpmap[0])):
            if (bpmap[0][k] == 0) or (bpmap[1][k] == 0) or (bpmap[0][k] == ydim-1) or (bpmap[1][k] == xdim-1):
                cube[bpmap[0][k],bpmap[1][k]] = 0.
            else:
                cube[bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])

    if ndim == 3:
        for i in range(np.shape(cube)[0]):
            bpmap = np.where(np.isnan(cube[i,:,:]))
            for k in range(len(bpmap[0])):
                if (bpmap[0][k] == 0) or (bpmap[1][k] == 0) or (bpmap[0][k] == ydim-1) or (bpmap[1][k] == xdim-1):
                    cube[i,bpmap[0][k],bpmap[1][k]] = 0.
                else:
                    cube[i,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
            
                
                
    return cube

#code de Jonas
# Comparaison avec d'autres code de sigmaclipping: c'est pour le moment le plus rapide (vectorize plus long)
def remove_bad_pixel(image_array2d:np.ndarray, threshold:float = 4, generic_filter_kernel_size:int = 5) -> np.ndarray:
    """
    Identifies bad pixels and replaces by nan values. Use `fill_nans_image` next to apply RDI or PCA.
    
    Parameters
    ----------
    image_array2d : np.ndarray
        2D array representing the image.
    threshold : float, optional
        Threshold in number of standard deviations to identify bad pixels, by default 4.
    generic_filter_kernel_size : int, optional
        Size of the filter kernel, by default 5. This represents the size of the neighborhood used to compute the mean and std (std over all pixels inside square of size x size).
    
    Returns
    -------
    np.ndarray
        Image with bad pixels replaced by NaN values.
    """
    assert threshold > 0, "Threshold must be positive!"
    assert isinstance(generic_filter_kernel_size, int) and generic_filter_kernel_size % 2 == 1, "generic_filter_kernel_size must be an odd integer!"
    
    # 1. Prepare std and mean on neighbours
    mask = np.ones((generic_filter_kernel_size, generic_filter_kernel_size))
    center = generic_filter_kernel_size // 2
    mask[center, center] = 0  # Exclude the center pixel from the calculation
    
    # 2. Compute std and mean images
    mean_image = generic_filter(
        image_array2d,
        function=lambda x: np.nanmean(x[mask.flatten().astype(bool)]),
        size=generic_filter_kernel_size,
        mode='constant',
        cval=np.nan
    )
    
    std_image = generic_filter(
        image_array2d,
        function=lambda x: np.nanstd(x[mask.flatten().astype(bool)]),
        size=generic_filter_kernel_size,
        mode='constant',
        cval=np.nan
    )
    
    # 3. Identify bad pixels
    deviation_image = (image_array2d - mean_image) / std_image  
    anomaly_mask = np.abs(deviation_image) > threshold
    image_array2d = copy.deepcopy(image_array2d)
    image_array2d[anomaly_mask] = np.nan
    return image_array2d


#code de Jonas
def fill_nans_image(image_array2d:np.ndarray, method = "nn", generic_filter_kernel_size:int = 5) -> np.ndarray:
    """
    Removes NaN values from a 2D image by applying a generic filter that replaces NaNs with the mean of surrounding pixels.
    
    Parameters
    ----------
    image_array2d : np.ndarray
        2D array representing the image with potential NaN values.
    method : Literal, optional
        Method to fill NaNs, either by taking the value of the nearest neighbor ("nn") or the mean of surrounding pixels ("nnmean"), by default "nnmean".
    generic_filter_kernel_size : int, optional
        Size of the filter kernel, by default 7. This represents the size of the neighborhood used to compute the mean (mean over all pixels inside square of size x size).
    """
    if method == "nn":
        nan_msk = np.isnan(image_array2d)
        distance, indices = distance_transform_edt(nan_msk, return_indices=True)
        image_2d_filled = copy.deepcopy(image_array2d)
        image_2d_filled[nan_msk] = image_array2d[tuple(indices[:, nan_msk])]
    if method == "nnmean":
        nan_msk = np.isnan(image_array2d)
        image_2d_filled = copy.deepcopy(image_array2d)
        image_2d_filled[nan_msk] = generic_filter(
            image_array2d,
            function=lambda x: np.nanmean(x),
            size=generic_filter_kernel_size,
            mode='constant',
            cval=np.nan
        )[nan_msk]
    assert np.isnan(image_2d_filled).sum() == 0, "There are still NaNs in the image! Increase filter kernel."
    return image_2d_filled

### function to replace NaN value by neighbour-mean value
def badpixel_corr(cube):
    ndim = len(np.shape(cube))
    ydim = np.shape(cube)[-2]
    xdim = np.shape(cube)[-1]
    if ndim == 2:
        bpmap = np.where(np.isnan(cube))
        for k in range(len(bpmap[0])):
            if bpmap[0][k] == 0:
                cube[bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[bpmap[0][k]:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
            elif bpmap[0][k] == ydim-1:
                cube[bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[bpmap[0][k]-1:bpmap[0][k]+1,bpmap[1][k]-1:bpmap[1][k]+2])
            elif bpmap[1][k] == 0:
                cube[bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]:bpmap[1][k]+2])
            elif bpmap[1][k] == xdim-1:
                cube[bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+1])
            else:
                cube[bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
    elif ndim == 3:
        for i in range(np.shape(cube)[0]):
            bpmap = np.where(np.isnan(cube[i,:,:]))
            for k in range(len(bpmap[0])):
                if bpmap[0][k] == 0:
                    cube[i,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,bpmap[0][k]:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
                elif bpmap[0][k] == ydim-1:
                    cube[i,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,bpmap[0][k]-1:bpmap[0][k]+1,bpmap[1][k]-1:bpmap[1][k]+2])
                elif bpmap[1][k] == 0:
                    cube[i,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]:bpmap[1][k]+2])
                elif bpmap[1][k] == xdim-1:
                    cube[i,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+1])
                else:
                    cube[i,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
    elif ndim ==4:
        for j in range(np.shape(cube)[1]):
            for i in range(np.shape(cube)[0]):
                bpmap = np.where(np.isnan(cube[i,j,:,:]))
                for k in range(len(bpmap[0])):
                    if bpmap[0][k] == 0:
                        cube[i,j,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,bpmap[0][k]:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
                    elif bpmap[0][k] == ydim-1:
                        cube[i,j,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,bpmap[0][k]-1:bpmap[0][k]+1,bpmap[1][k]-1:bpmap[1][k]+2])
                    elif bpmap[1][k] == 0:
                        cube[i,j,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]:bpmap[1][k]+2])
                    elif bpmap[1][k] == xdim-1:
                        cube[i,j,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+1])
                    else:
                        cube[i,j,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])

    
    elif ndim ==5:
        for l in range(np.shape(cube)[2]):
            for j in range(np.shape(cube)[1]):
                for i in range(np.shape(cube)[0]):
                    bpmap = np.where(np.isnan(cube[i,j,l,:,:]))
                    for k in range(len(bpmap[0])):
                        if bpmap[0][k] == 0:
                            cube[i,j,l,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,l,bpmap[0][k]:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])
                        elif bpmap[0][k] == ydim-1:
                            cube[i,j,l,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,l,bpmap[0][k]-1:bpmap[0][k]+1,bpmap[1][k]-1:bpmap[1][k]+2])
                        elif bpmap[1][k] == 0:
                            cube[i,j,l,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,l,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]:bpmap[1][k]+2])
                        elif bpmap[1][k] == xdim-1:
                            cube[i,j,l,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,l,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+1])
                        else:
                            cube[i,j,l,bpmap[0][k],bpmap[1][k]] = np.nanmean(cube[i,j,l,bpmap[0][k]-1:bpmap[0][k]+2,bpmap[1][k]-1:bpmap[1][k]+2])

    
    
    
    else:
        print('Cube with 1 dimension or more than 5. Nothing happened.')
        
    return cube



#### Flux scaling between target and reference using 2 method (Perrot+2023 and TA flux integration)
	

# f_scale = facteur a appliquer a la ref pour avoir le même niveau de flux que la target (see Perrot et al. 2023)



def flux_scaling_fact(cube,ref):
#    f_scale = np.sum(do_median(cube)*do_median(ref))/np.sum(do_median(ref)**2) # normalement c'est (TARGET*REF)/sigma**2 et (REF/sigma)**2
    f_scale = np.sum(cube*ref)/np.sum(ref**2) # normalement c'est (TARGET*REF)/sigma**2 et (REF/sigma)**2
    return f_scale


### Flux scaling with TA and using Gaussian fit and correlation map

def gaussian_ravel(coords, height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    xx = coords[0]
    yy = coords[1]
    width_x = float(width_x)
    width_y = float(width_y)
    return np.ravel(height*np.exp(-(((center_x-xx)/width_x)**2. + ((center_y-yy)/width_y)**2.)/2.))

def gaussian(coords, height, center_x, center_y, width_x, width_y):
    """Returns a gaussian function with the given parameters"""
    xx = coords[0]
    yy = coords[1]
    width_x = float(width_x)
    width_y = float(width_y)
    return height*np.exp(-(((center_x-xx)/width_x)**2. + ((center_y-yy)/width_y)**2.)/2.)

def correlation(ima, ima_ref):
    #correlation by Lisa
    ny = ima.shape[0]
    nx = ima.shape[1]
    aa = np.zeros((2 * ny, 2 * nx))
    bb = np.zeros((2 * ny, 2 * nx))
    aa[:ny, :nx] = np.copy(ima)
    bb[:ny, :nx] = np.copy(ima_ref)
    bb[ny:, :nx] = np.copy(ima_ref)
    bb[ny:, nx:] = np.copy(ima_ref)
    bb[:ny, nx:] = np.copy(ima_ref)

    temp = np.fft.fft2(aa) * np.conjugate(np.fft.fft2(bb))
    corr_map = np.real(np.fft.fftshift(np.fft.ifft2(temp)))
    return corr_map[int(ny/2):int(3*ny/2), int(nx/2):int(3*nx/2)]

def flux_scaling_ta(ta_roll_fld, ta_ref_fld, affix, silent=True):
    newdim=200
    roll, header = load_cube(ta_roll_fld+'/', affix, xdim=newdim, ydim=newdim, silent=silent)
    roll = clean_image_nan(roll)


    xx, yy = np.meshgrid(np.arange(newdim), np.arange(newdim))
    #TA = very broadband filter so we cant use the observed lam to estiamte the fwhm/sigma
    sigma = 1.55 #FWHM / (2 * np.sqrt(2 * np.log(2)))
    model_PSF = gaussian([xx,yy], 1., newdim/2, newdim/2, sigma, sigma)
    if silent: print('sigma model PSF: ',sigma)
    
    image = roll[0,:,:].reshape(newdim,newdim)
    image = clean_image_nan(image)

	
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
    if silent: 
        print('max: ',np.max(image),'Y: ', ypos_max, 'X: ', xpos_max,'sigma: ', sigma)
        plt.imshow(image[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none')
        plt.show()
    popt, pcov = curve_fit(gaussian_ravel, [xx, yy], np.ravel(image), p0=[np.max(image), ypos_max, xpos_max, sigma , sigma])
    stdd = np.sqrt(np.diag(pcov))
    if silent: 
        print("Roll - TA 1")
        print("Result : A = "+str(round(popt[0],1))+" / x0 = "+str(round(popt[1],2))+" / y0 = "+str(round(popt[2],2))+" / width_x = "+str(round(popt[3],2))+" / width_y = "+str(round(popt[4],2)))
        print("Stddev : A = "+str(round(stdd[0],1))+" / x0 = "+str(round(stdd[1],2))+" / y0 = "+str(round(stdd[2],2))+" / width_x = "+str(round(stdd[3],2))+" / width_y = "+str(round(stdd[4],2)))
    model_gauss = gaussian([xx, yy],popt[0],popt[1],popt[2],popt[3],popt[4])
    roll1_tot = np.sum(model_gauss)
    #print(np.shape(model_gauss))
    #print(np.sum(model_gauss[round(popt[2])-5:round(popt[2])+5,round(popt[1])-5:round(popt[1])+5]))
    #plt.matshow(roll[0,:,:].reshape(newdim,newdim),vmin=0,vmax=150,origin='lower',interpolation='none')
    #plt.matshow(model_gauss[round(popt[2])-5:round(popt[2])+5,round(popt[1])-5:round(popt[1])+5],vmin=0,vmax=190,origin='lower',interpolation='none')
    #plt.show()

    image = roll[1,:,:].reshape(newdim,newdim)
    image = clean_image_nan(image)
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
    if silent: 
        print('max: ',np.max(image),'Y: ', ypos_max, 'X: ', xpos_max,'sigma: ', sigma)
        plt.imshow(image[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none')
        plt.show()
    popt, pcov = curve_fit(gaussian_ravel, [xx, yy], np.ravel(image), p0=[np.max(image), ypos_max, xpos_max, sigma , sigma])
    stdd = np.sqrt(np.diag(pcov))
    if silent: 
        print("Roll - TA 2")
        print("Result : A = "+str(round(popt[0],1))+" / x0 = "+str(round(popt[1],2))+" / y0 = "+str(round(popt[2],2))+" / width_x = "+str(round(popt[3],2))+" / width_y = "+str(round(popt[4],2)))
        print("Stddev : A = "+str(round(stdd[0],1))+" / x0 = "+str(round(stdd[1],2))+" / y0 = "+str(round(stdd[2],2))+" / width_x = "+str(round(stdd[3],2))+" / width_y = "+str(round(stdd[4],2)))
    model_gauss = gaussian([xx, yy],popt[0],popt[1],popt[2],popt[3],popt[4])
    roll2_tot = np.sum(model_gauss)
    #plt.matshow(roll[1,:,:].reshape(newdim,newdim),vmin=0,vmax=150,origin='lower',interpolation='none')
    #plt.show()

    ref, header = load_cube(ta_ref_fld+'/', affix, xdim=newdim, ydim=newdim, silent=silent)
    ref = badpixel_corr(ref)

    image = ref[0,:,:].reshape(newdim,newdim)
    image = clean_image_nan(image)
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
    if silent: 
        print('max: ',np.max(image),'Y: ', ypos_max, 'X: ', xpos_max,'sigma: ', sigma)
        plt.imshow(image[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none')
        plt.show()
    popt, pcov = curve_fit(gaussian_ravel, [xx, yy], np.ravel(image), p0=[np.max(image), ypos_max, xpos_max, sigma , sigma])
    stdd = np.sqrt(np.diag(pcov))
    if silent: 
        print("Ref - TA 1")
        print("Result : A = "+str(round(popt[0],1))+" / x0 = "+str(round(popt[1],2))+" / y0 = "+str(round(popt[2],2))+" / width_x = "+str(round(popt[3],2))+" / width_y = "+str(round(popt[4],2)))
        print("Stddev : A = "+str(round(stdd[0],1))+" / x0 = "+str(round(stdd[1],2))+" / y0 = "+str(round(stdd[2],2))+" / width_x = "+str(round(stdd[3],2))+" / width_y = "+str(round(stdd[4],2)))
    model_gauss = gaussian([xx, yy],popt[0],popt[1],popt[2],popt[3],popt[4])
    ref1_tot = np.sum(model_gauss)
    #plt.matshow(roll[0,:,:].reshape(newdim,newdim),vmin=0,vmax=150,origin='lower',interpolation='none')
    #plt.show()

    image = ref[1,:,:].reshape(newdim,newdim)
    image = clean_image_nan(image)
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
    if silent: 
        print('max: ',np.max(image),'Y: ', ypos_max, 'X: ', xpos_max,'sigma: ', sigma)
        plt.imshow(image[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none')
        plt.show()
    popt, pcov = curve_fit(gaussian_ravel, [xx, yy], np.ravel(image), p0=[np.max(image), ypos_max, xpos_max, sigma , sigma])
    stdd = np.sqrt(np.diag(pcov))
    if silent: 
        print("Ref - TA 2")
        print("Result : A = "+str(round(popt[0],1))+" / x0 = "+str(round(popt[1],2))+" / y0 = "+str(round(popt[2],2))+" / width_x = "+str(round(popt[3],2))+" / width_y = "+str(round(popt[4],2)))
        print("Stddev : A = "+str(round(stdd[0],1))+" / x0 = "+str(round(stdd[1],2))+" / y0 = "+str(round(stdd[2],2))+" / width_x = "+str(round(stdd[3],2))+" / width_y = "+str(round(stdd[4],2)))
    model_gauss = gaussian([xx, yy],popt[0],popt[1],popt[2],popt[3],popt[4])
    ref2_tot = np.sum(model_gauss)


    f_scale = (roll1_tot+roll2_tot)/(ref1_tot+ref2_tot)
    return f_scale



### calcul le flux de la TA par Photometrie d'Ouverture centrée sur la position trouvée par auto-correlation
def flux_scaling_ta_OP(ta_roll_fld, ta_ref_fld, affix, lam, silent=True):
#, pos1=[165,176], pos2=[125,133]):
    newdim=200
    roll, header = load_cube(ta_roll_fld+'/', affix, xdim=newdim, ydim=newdim, silent=silent)
    ref, header  = load_cube(ta_ref_fld+'/', affix, xdim=newdim, ydim=newdim, silent=silent)
    roll = clean_image_nan(roll)
    ref  = clean_image_nan(ref)

    xx, yy = np.meshgrid(np.arange(newdim), np.arange(newdim))
    D=6.5
    pixscale = 0.110
    FWHM = lam/D/np.pi*180.*3600./pixscale
    sigma = 1.55 #FWHM / (2 * np.sqrt(2 * np.log(2)))
    model_PSF = gaussian([xx,yy], 1., newdim/2, newdim/2, sigma, sigma)
    print('sigma model PSF: ',sigma)
        
    ### SCIENCE
    print("Roll - TA 1")
    image = roll[0,:,:]#.reshape(newdim,newdim)	
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
    
    Y, X = np.ogrid[:newdim, :newdim]
    mask = np.sqrt((X - xpos_max+0.5)**2 + (Y-ypos_max+0.5)**2) < 1*FWHM
    roll1_tot = np.sum(image*mask)
    
    print('max img:',np.max(image),'max corr:',image[ypos_max, xpos_max], 'Y:', ypos_max, 'X:', xpos_max, 'sigma:', sigma, 'Tot:', roll1_tot)
    plt.imshow((image*mask)[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none',cmap='inferno')
    plt.show()
    
    
    print("Roll - TA 2")
    image = roll[1,:,:]
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))

    Y, X = np.ogrid[:newdim, :newdim]
    mask = np.sqrt((X - xpos_max+0.5)**2 + (Y-ypos_max+0.5)**2) < 1*FWHM
    roll2_tot = np.sum(image*mask)

    print('max img:',np.max(image),'max corr:',image[ypos_max, xpos_max], 'Y:', ypos_max, 'X:', xpos_max, 'sigma:', sigma, 'Tot:', roll2_tot)
    plt.imshow((image*mask)[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none',cmap='inferno')
    plt.show()
    

    ### REFERENCE


    print("Ref - TA 1")
    image = ref[0,:,:]
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
    
    Y, X = np.ogrid[:newdim, :newdim]
    mask = np.sqrt((X - xpos_max+0.5)**2 + (Y-ypos_max+0.5)**2) < 1*FWHM
    ref1_tot = np.sum(image*mask)

    print('max img:',np.max(image),'max corr:',image[ypos_max, xpos_max], 'Y:', ypos_max, 'X:', xpos_max, 'sigma:', sigma, 'Tot:', ref1_tot)
    plt.imshow((image*mask)[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none',cmap='inferno')
    plt.show()
    

    print("Ref - TA 2")
    image = ref[1,:,:]
    corr_map = correlation(image, model_PSF)
    ypos_max, xpos_max = np.unravel_index(np.argmax(corr_map),(newdim, newdim))
   
    Y, X = np.ogrid[:newdim, :newdim]
    mask = np.sqrt((X - xpos_max+0.5)**2 + (Y-ypos_max+0.5)**2) < 1*FWHM
    ref2_tot = np.sum(image*mask)

    print('max img:',np.max(image),'max corr:',image[ypos_max, xpos_max], 'Y:', ypos_max, 'X:', xpos_max, 'sigma:', sigma, 'Tot:', ref2_tot)
    plt.imshow((image*mask)[ypos_max-15:ypos_max+15, xpos_max-15:xpos_max+15],origin='lower',interpolation='none',cmap='inferno')
    plt.show()


    f_scale = (roll1_tot+roll2_tot)/(ref1_tot+ref2_tot)
    return f_scale






	
#### Different RDI postprocessing
#- classical RDI (target - reference)
#- RDI Linear Combination
#- RDI PCA / KLIP
#- classical ADI (target - target with different angle)

def RDI_classic(cube, ref, offset_ref = 0., f_scale = 0):
    if f_scale == 0:
        f_scale = flux_scaling_fact(cube, ref)
    ndim_ref = len(np.shape(ref))
    if ndim_ref == 2:
        res = cube - (f_scale*ref + offset_ref)
    if ndim_ref == 3:
        res = cube - (f_scale*np.nanmedian(ref,axis=0) + offset_ref)
    if ndim_ref > 3:
        raise Exception("Okay, Houston, I believe we have had a problem here (ndim ref > 3)")
    if ndim_ref <2:
        raise Exception("Okay, Houston, I believe we have had a problem here (ndim ref < 2)")
    return res



def MIRI_linear_comb(target, reference, use_minimize=False):
    
    def linear_comb(P):
        result = science - lib_reference.dot(P)
        return np.sum(result*result)

    science = target.flatten()
    lib_reference = np.column_stack([m.flatten() for m in reference])
    P0 = np.zeros(lib_reference.shape[1])  
    
    if use_minimize:
        bounds = [(0, None)] * lib_reference.shape[1]
        res = minimize(linear_comb, P0, method="L-BFGS-B",tol=1e-5, bounds=bounds) #Nelder-Mead
    else:
        res = lsq_linear(lib_reference.astype(np.float64), science.astype(np.float64), bounds=(0, np.inf))
    
    p_opti = res.x
    model_combined = (lib_reference @ p_opti).reshape(target.shape)
    residual = target - model_combined
    return residual



def MIRI_linear_comb_mask(target, reference, mask, use_minimize=False):
    def linear_comb(P):
        for i in range(nb_refs):
            result = science - lib_reference_mask.dot(P)
        return np.sum(result*result)
    
    lib_reference = np.column_stack([m.flatten() for m in reference] + [np.ones(reference[0].shape).flatten(), -np.ones(reference[0].shape).flatten()])
    
    if use_minimize:
        target_mask = np.ma.array(target, mask=mask)
        science = (target_mask).flatten()
        nb_refs = np.shape(reference)[0]
        lib_reference_mask = np.column_stack([np.ma.array(reference[i], mask=mask).flatten() for i in range(nb_refs)])
        P0 = np.zeros(lib_reference.shape[1]) 
        bounds = [(0, None)] * lib_reference_mask.shape[1]
        res = minimize(linear_comb, P0, method="Nelder-Mead",tol=1e-10, bounds=bounds) #"L-BFGS-B" #"Nelder-Mead"
    else:
        science = target[mask]
        lib_reference_mask = np.column_stack([m[mask] for m in reference] + [np.ones(reference[0].shape)[mask], -np.ones(reference[0].shape)[mask]])
        res = lsq_linear(lib_reference_mask.astype(np.float64), science.astype(np.float64), bounds=(0, np.inf), max_iter=1000, verbose=0)
    
    p_opti = res.x
    model_combined = (lib_reference @ p_opti).reshape(target.shape)
    residual = target - model_combined
    return residual




#PCA traduit de IDL à Python par Mathilde Mâlin
def sub_PCA(data_target, data_ref, center_corono, Ktrunc, dim=45, plot=False):
    nb_ref = len(data_ref)
    #OK
    
    #dim=45
    limx = [int(center_corono[0]-dim), int(center_corono[0]+dim)]
    limy = [int(center_corono[1]-dim), int(center_corono[1]+dim)]
    data_red = data_target[limx[0]:limx[1], limy[0]:limy[1]]
    data_red_ref = [data_ref[r][limx[0]:limx[1], limy[0]:limy[1]] for r in range(nb_ref)]
    
    #Ref en 2D : nb ref x nb pixels
    ref_flat = [np.ndarray.flatten(data_red_ref[r]) for r in range(nb_ref)]
    ref_mean = [np.nanmean(ref_flat[r])  for r in range(nb_ref)]
    Xref = [ref_flat[r] - ref_mean[r] for r in range(nb_ref)]
    Xref = np.array(Xref)
    #print(np.shape(Xref))
    
    #Data en 2D : nb_frame (toujours 1) x nb pixels
    data_flat = np.ndarray.flatten(data_red)
    data_mean = np.nanmean(data_flat)
    Xdata = data_flat - data_mean
    #print(np.shape(Xdata))
    
    Npix = len(Xdata)
    #nb de modes qu’on souhaite supp
    Ktrunc = int(Ktrunc)
   
    #mesure de la matrice de covariace
    V = np.dot(Xref,np.transpose(Xref))/Npix #useless ici
    cov_matrix = np.cov(Xref)
    #mesure des valeurs et vecteurs propres
    eigenvalues, eigenvectors = eig(cov_matrix)
    
    #modes de la ref
    modes = np.dot(np.transpose(eigenvectors),Xref)
    
    #Normalisation des modes ???
    normv = np.sqrt(np.sum(modes**2,1))
    modes = [modes[r,:]/normv[r] for r in range(nb_ref)]
    coef = np.dot(Xdata, np.transpose(modes[:Ktrunc-1]))
    
    #projection des modes des ref sur les coef de l’image
    X_data_projected = np.dot(np.transpose(modes[:Ktrunc-1]),coef)
    ref_reconstructed = X_data_projected + data_mean #juste data mean ??
    
    #Reshape la nouevlle ref en 2D
    h,w = np.shape(data_red)
    ref_reshape = np.reshape(ref_reconstructed, (h,w))
    if plot == True:
        fig, ax = plt.subplots(1, 3, figsize =(17,4))
        im=ax[0].imshow(ref_reshape, origin="lower", vmin=-2, vmax=6)
        ax[0].set_title("new reference")
        cbar = fig.colorbar(im,ax = ax[0], orientation = "vertical")
        cbar.set_label('DN/s', rotation=270,  labelpad = 20, fontsize=16)
        im=ax[1].imshow(data_red, origin="lower", vmin=-2, vmax=6)
        ax[1].set_title("Data")
        cbar = fig.colorbar(im,ax = ax[1], orientation = "vertical")
        cbar.set_label('DN/s', rotation=270,  labelpad = 20, fontsize=16)
        im=ax[2].imshow(data_red - ref_reshape, origin="lower", vmin=-1, vmax=6)
        ax[2].set_title("Data - new ref")
        cbar = fig.colorbar(im,ax = ax[2], orientation = "vertical")
        cbar.set_label('DN/s', rotation=270,  labelpad = 20, fontsize=16)
        plt.show()
    return data_red - ref_reshape





def apply_pca(
    science_image:np.ndarray,
    reference_images:list[np.ndarray],
    pca_masks:list[np.ndarray] = None,
    sharpness:float = 0,
    n_components:int = None
):
    """
    Applies PCA-based RDI to a science image given a list of reference images.

    Parameters
    ----------
    science_image : np.ndarray
        The science image to process.
    reference_images : list[np.ndarray]
        List of reference images to use for RDI.
    pca_masks : list[np.ndarray]
        One PCA subtraction will be performed per mask in this list. The masks should not intersect and their union should cover the full image.
    sharpness : float, optional
        An opimal k is found by the algorithm. If sharpness is 0, the optimal k will be used. Else, K = optimal_k * (1-sharpness) + len(S) * sharpness where S is the singular values array.
    n_components : int, optional
        If provided, this number of components will be used for all masks, overriding the optimal k found by the algorithm.
    """

    # ----------------- #
    # !-- Arguments --! #
    # ----------------- #

    # 1. Check references
    assert isinstance(reference_images, list), "reference_images must be a list of images (os a list of numpy arrays)!"
    assert len(reference_images) > 0, "At least one reference image must be provided!"
    assert isinstance(reference_images[0], np.ndarray), "reference_images must be a list of images (os a list of numpy arrays)!"
    assert all([img.shape == science_image.shape for img in reference_images]), "All images must have the same shape!"

    # 2. Check masks
    if pca_masks is None:
        pca_masks = [np.ones_like(science_image, dtype=bool)]
    assert isinstance(pca_masks, list), "pca_masks must be a list of masks (os a list of numpy arrays)!"
    assert isinstance(pca_masks[0], np.ndarray), "pca_masks must be a list of masks (os a list of numpy arrays)!"
    assert all([mask.shape == science_image.shape for mask in pca_masks]), "All masks must have the same shape as the images!"
    # let's sume masks as integers and check that we get ones everywhere
    sum_of_masks = np.sum(np.array(pca_masks, dtype=int), axis=0)
    assert np.all(sum_of_masks == 1), "The masks must not intersect and their union must cover the full image!"
    assert all([np.sum(mask) >= 2 * len(reference_images) for mask in pca_masks]), "Each mask must contain at least 2 times more pixels than reference images!"


    # ----------- #
    # !-- PCA --! #
    # ----------- #

    pca_model = np.zeros_like(science_image).flatten() # we will reshape at the end

    for mask in pca_masks:

        # 1. Prepare data matrix
        X = np.array([img[mask].flatten() for img in reference_images]).T  # shape (n_pixels, n_references)
        #X_mean = np.mean(X, axis=1, keepdims=True)
        X_centered = X# - X_mean  # Center the data

        # 2. Compute SVD
        U, S, VT = np.linalg.svd(X_centered, full_matrices=False)

        # 3. Find optimal number of components using the elbow method
        from kneed import KneeLocator
        knee = KneeLocator(range(len(S)), S, curve='convex', direction='decreasing')
        k = knee.knee
        if k is None:
            k = min(1, len(S) // 10) # Fallback to 10% of components if knee not found
        k = np.round(k * (1 - sharpness) + len(S) * sharpness).astype(int)
        if n_components is not None:
            k = n_components
            assert k <= len(S), f"n_components must be less than or equal to the number of reference images ({len(S)})! Got {k}."

        # 4. Project science image onto PCA basis
        y = science_image[mask].flatten()
        y_centered = y #- X_mean.flatten()
        U_k = U[:, :k]
        coefficients = U_k.T @ y_centered  # shape (k,)
        y_pca_model = U_k @ coefficients #+ X_mean.flatten()  # shape (n_pixels,)
        pca_model[mask.flatten()] = y_pca_model


    # ------------- #
    # !-- Model --! #
    # ------------- #

    pca_model = pca_model.reshape(science_image.shape)
    return science_image - pca_model