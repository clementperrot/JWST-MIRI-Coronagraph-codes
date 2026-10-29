# JWST/MIRI Coronagraph codes
Codes related to JWST/MIRI data reduction and post-processing for the Exoplanetary Systems team at Paris Observatory/LIRA

## Directories and Files description :

- Background_analysis : codes for JWST/MIRI background analysis (coronagraph) - Work in progress
	
- Development : Divers codes I'm working on - Work in progress

- Module : Finalized codes than can be import
	
- Notebook_proposal : Divers codes for JWST proposals
	
- Notebook_target : Notebook for data reduction and post-processing for specific targets, could be outdated


Short description of finished codes and modules :

*obs_information.ipynb :*

3 small functions to read information and organize data downloaded from MAST. 
- move_file_JWST() : The main function, allows you to move files downloaded from MAST into dedicated directories. The directory structure is as follows: /PXXXX/obsYYY, where XXXXX is the program ID and YYY is the observation ID.
- version_fits_JWST() : For each file in the directory, display the version of the pipeline that generated it.
- obs_information_JWST() : Displays the following information for each file in the selected directory: Observation ID, Observatory Day, Calibration Version, CRDS Version, Acquisition Type, Filter, Exposure Time, Observation Category, Target Name.

*Miri_corono_stage_1_2.ipynb :*

Functions for reducing data from JWST/MIRI coronagraphic observations. These functions allow you to perform Stage 1 (uncal to rate), Stage 2 (rate to cal), and to construct the master backgrounds (cal).
An execution template is available at the end of the notebook.

*imodex_miri_postprocess_pipeline.py :*

'imp.py' is a personal library of useful code for post-processing JWST/MIRI coronagraphic data; it includes functions for reading the data, removing NaNs and outliers (sigma clipping), and applying post-processing algorithms (RDI with flux adjustment, PCA, linear combination).
