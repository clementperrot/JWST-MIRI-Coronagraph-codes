#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch stage 1 et stage 2 du programme P09056 : GO - Imaging the Coldest Planets Around the Nearest Accelerating Stars
Auteur: Clément PERROT
Date: 2026-11-05
"""

import Miri_corono_stage_1_2 as stg

prog_id        = 'P09056'
uncal_dir      = "/volumes/dio/data5/JWST_RAW/MAST/UNCAL/"+prog_id+"/"
rate_dir       = "/volumes/dio/data5/JWST_RAW/MAST/RATE/"+prog_id+"/"
cal_dir        = "/volumes/dio/data5/JWST_RAW/MAST/CAL/"+prog_id+"/"
master_bkg_dir = "/volumes/dio/data5/JWST_RAW/MAST/MASTER_BKG/"+prog_id+"/"

# HIP 46655 - roll 1

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP46655'
name_ref       = 'REF_HD79356'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["006"],["005"]] # Sciences Roll 
num_obs_ref    = [["003"],["004"]] # Reference Roll 
num_obs_bkgsci = [["008"],["007"]] # Science Background
num_obs_bkgref = [["001"],["002"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HIP 46655 - roll 2 - données pas encore publique

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP46655'
name_ref       = 'REF_HD79356'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [[],[]] #[["054"],["053"]] # Sciences Roll                    #données non publique
num_obs_ref    = [[],[]] #[["051"],["052"]] # Reference Roll                    #données non publique
num_obs_bkgsci = [[],[]] #[["056"],["055"]] # Science Background                   #données non publique
num_obs_bkgref = [[],[]] #[["049"],["050"]] # Reference Background                   #données non publique

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HIP 108706 - roll 1

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP108706'
name_ref       = 'REF_BD+28-4305'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["014"],["013"]] # Sciences Roll 
num_obs_ref    = [["011"],["012"]] # Reference Roll 
num_obs_bkgsci = [["016"],["015"]] # Science Background
num_obs_bkgref = [["009"],["010"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HIP 108706 - roll 2 - données pas encore publique

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP108706'
name_ref       = 'REF_BD+28-4305'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [[],[]] #[["046"],["045"]] # Sciences Roll                    #données non publique
num_obs_ref    = [["043"],["044"]] # Reference Roll 
num_obs_bkgsci = [[],[]] #[["048"],["047"]] # Science Background                   #données non publique
num_obs_bkgref = [["041"],["042"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HIP 80459 - données pas encore publique

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP80459'
name_ref       = 'REF_HD234402'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [[],[]] #[["022"],["021"]] # Sciences Roll                   #données non publique
num_obs_ref    = [["019"],["020"]] # Reference Roll 
num_obs_bkgsci = [[],[]] #[["024"],["023"]] # Science Background                   #données non publique
num_obs_bkgref = [["017"],["018"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HIP 88478

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP88478'
name_ref       = 'REF_HD145250'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["030"],["029"]] # Sciences Roll 
num_obs_ref    = [["027"],["028"]] # Reference Roll 
num_obs_bkgsci = [["032"],["031"]] # Science Background
num_obs_bkgref = [["025"],["026"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")

# HIP 25878

dostage1       = False  # calwebb_detector1 from uncal to rate
dostage2       = True   # calwebb_image2 from rate to cal
domasterbkg    = True   # home made, do master background from both bkg dither (minimum or mean)

name_sci       = 'HIP25878'
name_ref       = 'REF_HD39853'
filter_name    = ["F1065C","F1550C"]
# For each filter : Science, Reference, Sci Background, Ref Background
num_obs_sci    = [["038"],["037"]] # Sciences Roll 
num_obs_ref    = [["035"],["036"]] # Reference Roll 
num_obs_bkgsci = [["040"],["039"]] # Science Background
num_obs_bkgref = [["033"],["034"]] # Reference Background

if dostage1:
    stg.MIRI_stage_1(uncal_dir, rate_dir, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if dostage2:
    stg.MIRI_stage_2_no_bkg(rate_dir, cal_dir, prog_id, name_sci, name_ref, filter_name, num_obs_sci, num_obs_ref, num_obs_bkgsci, num_obs_bkgref)

if domasterbkg:
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_sci, num_obs_bkgsci, method="minimum")
    stg.MIRI_stage_2_master_background(cal_dir, master_bkg_dir, prog_id, name_ref, num_obs_bkgref, method="minimum")
