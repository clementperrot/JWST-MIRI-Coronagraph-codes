#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module pour faire la calibration de stage 1 et stage 2 des données MIRI coronographe ainsi que le master background.
Auteur: Clément PERROT
Date: 2026-11-05
"""

# Basic system utilities for interacting with files
import glob, os 
from collections import defaultdict
import numpy as np
from astropy.io import fits

# for JWST calibration pipeline
import jwst
import crds
from jwst.pipeline import Detector1Pipeline
from jwst.pipeline import Image2Pipeline

# Echo pipeline version and CRDS context in use
print(f"JWST Calibration Pipeline Version: {jwst.__version__}")
print(f"Using CRDS Context: {crds.get_context_name('jwst')}")


def stage1(files, output_dir):
    """
    Applique la calibration du pipeline officiel JWST pour passer de UNCAL à RATE (stage 1) 

    Args:
        files (str): path des fichiers uncal, peut être une list de fichier
        output_dir (str): chemin d'accès pour le répertoire de sauvegarde des produits du stage 1

    Returns:
        None
    """
    det1dict = defaultdict(dict)
    det1dict['jump']['maximum_cores'] = 'half' # Turn on multi-core processing (off by default).  Choose what fraction of cores to use (quarter, half, or all)
    for f in files:
        Detector1Pipeline.call(f, output_dir=output_dir, steps=det1dict, save_results=True)


def MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref):
    """
    Create folder for output and proceed to the stage 1 data reduction

    Args:
        uncal_dir (str)                  : Path where UNCAL (Stage 0 data) observation are.                     Ex : "/home/login/data/JWST/MIRI/UNCAL/P03662/"
        rate_dir (str)                   : Path where RATE (Stage 1 data) observation are (saved).              Ex : "/home/login/data/JWST/MIRI/RATE/P03662/"
        filter_name (list[str])          : Name of filter used.                                                 Ex : ["F1140C"] / ["F1065C","F1140C"]
        num_obs_sci (list[list[str]])    : Obs number of the Science acquisition for each filters.              Ex : [["001","002"]] / [["007","012"],["009","011"]] / [[]] if empty
        num_obs_ref (list[list[str]])    : Obs number of the Reference acquisition for each filters.            Ex : [["004"]] / [["002"],["004"]] / [[]] if empty
        num_obs_bkgsci (list[list[str]]) : Obs number of the Background Science acquisition for each filters.   Ex : [["003"]] / [["008"],["010"]] / [[]] if empty
        num_obs_bkgref (list[list[str]]) : Obs number of the Background Reference acquisition for each filters. Ex : [["005"]] / [["003"],["005"]] / [[]] if empty
        
    Returns:
        None
    """

    assert os.path.exists(uncal_dir), "Wrong rate directory !"

    if not os.path.exists(rate_dir): os.makedirs(rate_dir)
    
    # Loot on filters
    nb_filter = len(filter_name)
    for ft in range(nb_filter):
                     
        #Coronagraphic Science obs + TA
        for id_s in range(len(num_obs_sci[ft])):
            if not os.path.exists(rate_dir+"obs"+str(num_obs_sci[ft][id_s])+"/"):    os.makedirs(rate_dir+"obs"+str(num_obs_sci[ft][id_s])+"/")
            if not os.path.exists(rate_dir+"obs"+str(num_obs_sci[ft][id_s])+"/TA/"): os.makedirs(rate_dir+"obs"+str(num_obs_sci[ft][id_s])+"/TA/")
            
            #Stage 1 files for Science and associate TA
            files_sci    = sorted(glob.glob(uncal_dir+'obs'+str(num_obs_sci[ft][id_s])+'/*_mirimage_uncal.fits'))
            files_sci_TA = sorted(glob.glob(uncal_dir+'obs'+str(num_obs_sci[ft][id_s])+'/TA/*_mirimage_uncal.fits'))
            stage1(files_sci,    rate_dir+"obs"+str(num_obs_sci[ft][id_s])+"/")
            stage1(files_sci_TA, rate_dir+"obs"+str(num_obs_sci[ft][id_s])+"/TA/")            
            
        #Coronagraphic Reference obs + TA
        for id_r in range(len(num_obs_ref[ft])):
            if not os.path.exists(rate_dir+"obs"+str(num_obs_ref[ft][id_r])+"/"):    os.makedirs(rate_dir+"obs"+str(num_obs_ref[ft][id_r])+"/")
            if not os.path.exists(rate_dir+"obs"+str(num_obs_ref[ft][id_r])+"/TA/"): os.makedirs(rate_dir+"obs"+str(num_obs_ref[ft][id_r])+"/TA/")    
            
            #Stage 1 files for Reference and associate TA
            files_ref    = sorted(glob.glob(uncal_dir+'obs'+str(num_obs_ref[ft][id_r])+'/*_mirimage_uncal.fits'))
            files_ref_TA = sorted(glob.glob(uncal_dir+'obs'+str(num_obs_ref[ft][id_r])+'/TA/*_mirimage_uncal.fits'))
            stage1(files_ref,    rate_dir+"obs"+str(num_obs_ref[ft][id_r])+"/")
            stage1(files_ref_TA, rate_dir+"obs"+str(num_obs_ref[ft][id_r])+"/TA/") 
                      
        # Background Science obs            
        for id_bs in range(len(num_obs_bkgsci[ft])):
            if not os.path.exists(rate_dir+"obs"+str(num_obs_bkgsci[ft][id_bs])+"/"): os.makedirs(rate_dir+"obs"+str(num_obs_bkgsci[ft][id_bs])+"/")
                
            files_bkg = sorted(glob.glob(uncal_dir+'obs'+str(num_obs_bkgsci[ft][id_bs])+'/*_mirimage_uncal.fits'))
            stage1(files_bkg, rate_dir+"obs"+str(num_obs_bkgsci[ft][id_bs])+"/") 
             
        # Background Reference obs    
        for id_br in range(len(num_obs_bkgref[ft])):
            if not os.path.exists(rate_dir+"obs"+str(num_obs_bkgref[ft][id_br])+"/"): os.makedirs(rate_dir+"obs"+str(num_obs_bkgref[ft][id_br])+"/")
                
            files_ref_bkg = sorted(glob.glob(uncal_dir+'obs'+str(num_obs_bkgref[ft][id_br])+'/*_mirimage_uncal.fits')) 
            stage1(files_ref_bkg, rate_dir+"obs"+str(num_obs_bkgref[ft][id_br])+"/") 


### STAGE 2 ###

def stage2(files, output_dir, output_file):
    """
    Applique la calibration du pipeline officiel JWST pour passer de RATE à CAL (stage 2) 

    Args:
        files (str): path des fichiers uncal, peut être une list de fichier
        output_dir (str): chemin d'accès pour le répertoire de sauvegarde des produits du stage 2
        output_file (str): base du nom du fichier à sauvegarder

    Returns:
        None
    """
    image2dict = defaultdict(dict) # Set up a dictionary to define how the Image2 pipeline should be configured.
    image2dict['bkg_subtract']['skip'] = True
    image2dict['flat_field']['skip'] = True 
    image2dict['photom']['skip'] = False
    image2dict['assign_wcs']['skip'] = False

    incr = 1 #for the dither number
    for f in files:
        Image2Pipeline.call(f, output_dir=output_dir, output_file=output_file+'_dither'+str(incr), steps=image2dict, save_results=True)
        incr += 1

def MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref):
    """
    Create folder for output and proceed to the stage 1 data reduction

    Args:
        rate_dir (str)                   : Path where RATE (Stage 1 data) observation are.                      Ex : "/home/login/data/JWST/MIRI/RATE/P03662/"
        cal_dir (str)                    : Path where CAL (Stage 2 data) observation are (saved).               Ex : "/home/login/data/JWST/MIRI/CAL/P03662/"
        prog_id (str)                    : ID of the program (format = Pxxxx).                                  Ex : 'P03662'
        name_sci (str)                   : Name of the target.                                                  Ex : 'TWA7'
        name_ref (str)                   : Name of the reference star.                                          Ex : 'REF_CD23_9765'
        filter_name (list[str])          : Name of filter used.                                                 Ex : ["F1140C"] / ["F1065C","F1140C"]
        num_obs_sci (list[list[str]])    : Obs number of the Science acquisition for each filters.              Ex : [["001","002"]] / [["007","012"],["009","011"]] / [[]] if empty
        num_obs_ref (list[list[str]])    : Obs number of the Reference acquisition for each filters.            Ex : [["004"]] / [["002"],["004"]] / [[]] if empty
        num_obs_bkgsci (list[list[str]]) : Obs number of the Background Science acquisition for each filters.   Ex : [["003"]] / [["008"],["010"]] / [[]] if empty
        num_obs_bkgref (list[list[str]]) : Obs number of the Background Reference acquisition for each filters. Ex : [["005"]] / [["003"],["005"]] / [[]] if empty
        
    Returns:
        None
    """
    
    assert os.path.exists(rate_dir), "Wrong rate directory !"

    if not os.path.exists(cal_dir): os.makedirs(cal_dir)
    
    # Loot on filters
    nb_filter = len(filter_name)
    for ft in range(nb_filter):
                     
        #Coronagraphic Science obs + TA
        for id_s in range(len(num_obs_sci[ft])):
            if not os.path.exists(cal_dir+"obs"+str(num_obs_sci[ft][id_s])+"/"):    os.makedirs(cal_dir+"obs"+str(num_obs_sci[ft][id_s])+"/")
            if not os.path.exists(cal_dir+"obs"+str(num_obs_sci[ft][id_s])+"/TA/"): os.makedirs(cal_dir+"obs"+str(num_obs_sci[ft][id_s])+"/TA/")
            
            #Stage 1 files for Science and associate TA
            files_sci    = sorted(glob.glob(rate_dir+'obs'+str(num_obs_sci[ft][id_s])+'/*_mirimage_rate.fits'))
            files_sci_TA = sorted(glob.glob(rate_dir+'obs'+str(num_obs_sci[ft][id_s])+'/TA/*_mirimage_rate.fits'))
            print("science files",files_sci)
            stage2(files_sci,    cal_dir+"obs"+str(num_obs_sci[ft][id_s])+"/",    prog_id+'_'+str(num_obs_sci[ft][id_s])+'_'+name_sci)
            stage2(files_sci_TA, cal_dir+"obs"+str(num_obs_sci[ft][id_s])+"/TA/", prog_id+'_'+str(num_obs_sci[ft][id_s])+'_'+name_sci+'_TA')            
            
        #Coronagraphic Reference obs + TA
        for id_r in range(len(num_obs_ref[ft])):
            if not os.path.exists(cal_dir+"obs"+str(num_obs_ref[ft][id_r])+"/"):    os.makedirs(cal_dir+"obs"+str(num_obs_ref[ft][id_r])+"/")
            if not os.path.exists(cal_dir+"obs"+str(num_obs_ref[ft][id_r])+"/TA/"): os.makedirs(cal_dir+"obs"+str(num_obs_ref[ft][id_r])+"/TA/")    
            
            #Stage 1 files for Reference and associate TA
            files_ref    = sorted(glob.glob(rate_dir+'obs'+str(num_obs_ref[ft][id_r])+'/*_mirimage_rate.fits'))
            files_ref_TA = sorted(glob.glob(rate_dir+'obs'+str(num_obs_ref[ft][id_r])+'/TA/*_mirimage_rate.fits'))
            stage2(files_ref,    cal_dir+"obs"+str(num_obs_ref[ft][id_r])+"/",    prog_id+'_'+str(num_obs_ref[ft][id_r])+'_'+name_ref)
            stage2(files_ref_TA, cal_dir+"obs"+str(num_obs_ref[ft][id_r])+"/TA/", prog_id+'_'+str(num_obs_ref[ft][id_r])+'_'+name_ref+'_TA') 
                      
        # Background Science obs            
        for id_bs in range(len(num_obs_bkgsci[ft])):
            if not os.path.exists(cal_dir+"obs"+str(num_obs_bkgsci[ft][id_bs])+"/"): os.makedirs(cal_dir+"obs"+str(num_obs_bkgsci[ft][id_bs])+"/")
                
            files_bkg = sorted(glob.glob(rate_dir+'obs'+str(num_obs_bkgsci[ft][id_bs])+'/*_mirimage_rate.fits'))
            stage2(files_bkg, cal_dir+"obs"+str(num_obs_bkgsci[ft][id_bs])+"/", prog_id+'_'+str(num_obs_bkgsci[ft][id_bs])+'_'+name_sci+'_background') 
             
        # Background Reference obs    
        for id_br in range(len(num_obs_bkgref[ft])):
            if not os.path.exists(cal_dir+"obs"+str(num_obs_bkgref[ft][id_br])+"/"): os.makedirs(cal_dir+"obs"+str(num_obs_bkgref[ft][id_br])+"/")
                
            files_ref_bkg = sorted(glob.glob(rate_dir+'obs'+str(num_obs_bkgref[ft][id_br])+'/*_mirimage_rate.fits')) 
            stage2(files_ref_bkg, cal_dir+"obs"+str(num_obs_bkgref[ft][id_br])+"/", prog_id+'_'+str(num_obs_bkgref[ft][id_br])+'_'+name_ref+'_background') 


### MASTER BACKGROUND ###

def MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name, num_obs, method="minimum"):
    """
    Do the minimum or mean between dither 1 and dither 2 of a background observation

    Args:
        cal_dir (str)             : Path where CAL (Stage 2 data) observation are.                       Ex : "/home/login/data/JWST/MIRI/CAL/P03662/"
        master_bkg_dir (str)      : Path where Master Background (Stage 2 data) observation are (saved). Ex : "/home/login/data/JWST/MIRI/MASTER_BKG/P03662/
        prog_id (str)             : ID of the program (format = Pxxxx).                                  Ex : 'P03662'
        num_obs (list[list[str]]) : Obs number of the Background.                                        Ex : [["003"],["005"]]  / [[]] if empty
        method (str)              : Method used                                                          Ex : "minimum" or "mean"  
        
    Returns:
        None
    """
    
    if (method != "minimum") and (method != "mean"):
        method = "minimum"
    print('Master background method : '+method)


    nb_filter = np.shape(num_obs)[0]
    for ft in range(nb_filter):
        nb_obs = np.shape(num_obs[ft])[0]

        if not os.path.exists(master_bkg_dir): os.makedirs(master_bkg_dir)

        #loop on obs 
        for id in range(nb_obs):
            if not os.path.exists(master_bkg_dir+"obs"+str(num_obs[ft][id])+"/"): os.makedirs(master_bkg_dir+"obs"+str(num_obs[ft][id])+"/")                
            files = sorted(glob.glob(cal_dir+'obs'+str(num_obs[ft][id])+'/'+prog_id+'_'+str(num_obs[ft][id])+'_'+name+'_background_dither*_cal.fits'))
            img = fits.open(files[0])
            
            if len(files) == 1:
                print("Only one dither.")
                master_bkg = fits.open(files[0])[1].data
            else:
                dither1 = fits.open(files[0])[1].data
                dither2 = fits.open(files[1])[1].data
                if method == "minimum":
                    master_bkg = np.minimum(dither1,dither2)
                elif method == "mean":
                    master_bkg = np.nanmean([dither1,dither2], axis=0)

            mbkg_name = prog_id+'_'+str(num_obs[ft][id])+'_'+name+'_master_bkg_cal.fits'
            img[0].header['FILENAME'] = mbkg_name
            hdu = fits.PrimaryHDU()
            hdu.data = master_bkg
            hdu.header = img[0].header
            hdu.writeto(master_bkg_dir+'obs'+str(num_obs[ft][id])+'/'+mbkg_name,overwrite=True)
            img.close()
            print("master background saved : "+master_bkg_dir+'obs'+str(num_obs[ft][id])+'/'+prog_id+'_'+str(num_obs[ft][id])+'_'+name+'_master_bkg_cal.fits')