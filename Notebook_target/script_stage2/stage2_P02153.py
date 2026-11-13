#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch stage 1 et stage 2 du programme P02153 : GO - Detecting a Young 2 Jupiter Mass Planet Embedded in the Disk of HD 163296   
Auteur: Clément PERROT
Date: 2026-11-05
"""

import Miri_corono_stage_1_2 as stg
 
prog_id        = 'P02153'
uncal_dir      = "/volumes/dio/data5/JWST_RAW/MAST/UNCAL/"+prog_id+"/"
rate_dir       = "/volumes/dio/data5/JWST_RAW/MAST/RATE/"+prog_id+"/"
cal_dir        = "/volumes/dio/data5/JWST_RAW/MAST/CAL/"+prog_id+"/"
master_bkg_dir = "/volumes/dio/data5/JWST_RAW/MAST/MASTER_BKG/"+prog_id+"/"

# HD 163296 - Obs 1 et 2 failed

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HD163296'
name_ref        = 'REF_2MJ17583283'
filter_name     = ["F1140C"] 
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["006","007"]] # Sciences Roll
num_obs_ref    = [["005"]] # Reference Roll 
num_obs_bkgsci = [["003"]] # Science Background
num_obs_bkgref = [["004"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")


