#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch stage 1 et stage 2 du programme P01386 : ERS - High Contrast Imaging of Exoplanets and Exoplanetary Systems with JWST    
Auteur: Clément PERROT
Date: 2026-11-05
"""

import Miri_corono_stage_1_2 as stg

prog_id        = 'P01386'
uncal_dir      = "/volumes/dio/data5/JWST_RAW/MAST/UNCAL/"+prog_id+"/"
rate_dir       = "/volumes/dio/data5/JWST_RAW/MAST/RATE/"+prog_id+"/"
cal_dir        = "/volumes/dio/data5/JWST_RAW/MAST/CAL/"+prog_id+"/"
master_bkg_dir = "/volumes/dio/data5/JWST_RAW/MAST/MASTER_BKG/"+prog_id+"/"

# HIP 65426

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HIP65426'
name_ref        = 'REF_HIP68245'
filter_name     = ["F1140C","F1550C"]  
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["004","005"],["007","008"]] # Sciences Roll
num_obs_ref    = [["006"],["009"]] # Reference Roll 
num_obs_bkgsci = [["028"],["030"]] # Science Background
num_obs_bkgref = [["029"],["031"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")


# HD 141569

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HD141569'
name_ref        = 'REF_HD140986'
filter_name     = ["F1065C","F1140C","F1550C"]   
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["019","020"],["022","023"],["025","026"]] # Sciences Roll
num_obs_ref    = [["021"],["024"],["027"]] # Reference Roll 
num_obs_bkgsci = [["032"],["034"],["036"]] # Science Background
num_obs_bkgref = [["033"],["035"],["037"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")




