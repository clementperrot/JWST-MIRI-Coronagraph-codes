#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch stage 1 et stage 2 du programme P01668 : GO - Searching for low mass planets in debris disk gaps   
Auteur: Clément PERROT
Date: 2026-11-05
"""

import Miri_corono_stage_1_2 as stg

prog_id        = 'P01668'
uncal_dir      = "/volumes/dio/data5/JWST_RAW/MAST/UNCAL/"+prog_id+"/"
rate_dir       = "/volumes/dio/data5/JWST_RAW/MAST/RATE/"+prog_id+"/"
cal_dir        = "/volumes/dio/data5/JWST_RAW/MAST/CAL/"+prog_id+"/"
master_bkg_dir = "/volumes/dio/data5/JWST_RAW/MAST/MASTER_BKG/"+prog_id+"/"

# HD 107146 

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HD107146'
name_ref        = 'REF_HD111067'
filter_name     = ["F1140C"]  
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["002","003"]] # Sciences Roll
num_obs_ref    = [["004"]] # Reference Roll 
num_obs_bkgsci = [["001"]] # Science Background
num_obs_bkgref = [["005"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HD 92945

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HD92945'
name_ref        = 'REF_HD95234'
filter_name     = ["F1140C"]  
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["007","008"]] # Sciences Roll
num_obs_ref    = [["009"]] # Reference Roll 
num_obs_bkgsci = [["006"]] # Science Background
num_obs_bkgref = [["010"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HD 206893

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HD206893'
name_ref        = 'REF_HD208445'
filter_name     = ["F1140C"]  
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["012","013"]] # Sciences Roll
num_obs_ref    = [["014"]] # Reference Roll 
num_obs_bkgsci = [["011"]] # Science Background
num_obs_bkgref = [["015"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")




