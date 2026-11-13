#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch stage 1 et stage 2 du programme P09252 : GO - Confirming the presence of a gas giant planet orbiting a nearby solar-type star    
Auteur: Clément PERROT
Date: 2026-11-05
"""

import Miri_corono_stage_1_2 as stg

prog_id        = 'P09252'
uncal_dir      = "/volumes/dio/data5/JWST_RAW/MAST/UNCAL/"+prog_id+"/"
rate_dir       = "/volumes/dio/data5/JWST_RAW/MAST/RATE/"+prog_id+"/"
cal_dir        = "/volumes/dio/data5/JWST_RAW/MAST/CAL/"+prog_id+"/"
master_bkg_dir = "/volumes/dio/data5/JWST_RAW/MAST/MASTER_BKG/"+prog_id+"/"

### Alpha Cen. Offset and bright sources.

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'ALPHA_CEN'
name_ref        = 'REF_EPS_MUS'
filter_name     = ["F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["004","006"]] # Sciences Roll
num_obs_ref    = [["001","003","008","010"]] # Reference Roll 
num_obs_bkgsci = [["005","007"]] # Science Background
num_obs_bkgref = [["002","009"]] # Reference Background  <--- "052" est une ref 9SGD mais sans TA et qui ressemble a un BKG

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum") 
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")


