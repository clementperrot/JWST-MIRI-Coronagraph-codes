#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch stage 1 et stage 2 du programme P03662 : GO - Imaging shepherding and carving planets in debris disks    
Auteur: Clément PERROT
Date: 2026-11-05
"""

import Miri_corono_stage_1_2 as stg

prog_id        = 'P03662'
uncal_dir      = "/volumes/dio/data5/JWST_RAW/MAST/UNCAL/"+prog_id+"/"
rate_dir       = "/volumes/dio/data5/JWST_RAW/MAST/RATE/"+prog_id+"/"
cal_dir        = "/volumes/dio/data5/JWST_RAW/MAST/CAL/"+prog_id+"/"
master_bkg_dir = "/volumes/dio/data5/JWST_RAW/MAST/MASTER_BKG/"+prog_id+"/" 

# HD 181327 
 
dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'HD181327'
name_ref        = 'REF_HD203010'
filter_name     = ["F1140C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["006","007"]] # Sciences Roll 
num_obs_ref    = [["009"]] # Reference Roll 
num_obs_bkgsci = [["008"]] # Science Background
num_obs_bkgref = [["010"]] # Reference Background

stage2.stage_2_miri_corono_ultimate_NObkg_calints(path, output_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

### master background (minimum) for SCIENCE
#stage2.stage_2_miri_corono_master_background(output_dir, master_bkg_dir, prog_id, name_sci, ["008"])
### master background (minimum) for REFERENCE
#stage2.stage_2_miri_corono_master_background(output_dir, master_bkg_dir, prog_id, name_ref, ["010"])


# TWA 7 

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci        = 'TWA7'
name_ref        = 'REF_CD23_9765'
filter_name     = ["F1140C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["001","002"]] # Sciences Roll 
num_obs_ref    = [["004"]] # Reference Roll 
num_obs_bkgsci = [["003"]] # Science Background
num_obs_bkgref = [["005"]] # Reference Background

stage2.stage_2_miri_corono_ultimate_NObkg_calints(path, output_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

### master background (minimum) for SCIENCE
#stage2.stage_2_miri_corono_master_background(output_dir, master_bkg_dir, prog_id, name_sci, ["003"])
### master background (minimum) for REFERENCE
#stage2.stage_2_miri_corono_master_background(output_dir, master_bkg_dir, prog_id, name_ref, ["005"])
