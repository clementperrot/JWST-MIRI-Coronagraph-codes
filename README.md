# JWST/MIRI Coronagraph codes
Codes related to JWST/MIRI data reduction and post-processing for the Exoplanetary Systems team at Paris Observatory/LIRA

## Files description :

*obs_information.ipynb :*
3 small functions to read information and organize data downloaded from MAST. 
- move_file_JWST() : The main function, allows you to move files downloaded from MAST into dedicated directories. The directory structure is as follows: /PXXXX/obsYYY, where XXXXX is the program ID and YYY is the observation ID.
- version_fits_JWST() : For each file in the directory, display the version of the pipeline that generated it.
- obs_information_JWST() : Displays the following information for each file in the selected directory: Observation ID, Observatory Day, Calibration Version, CRDS Version, Acquisition Type, Filter, Exposure Time, Observation Category, Target Name.

*Miri_corono_stage_1_2.ipynb :*
Functions for reducing data from JWST/MIRI coronagraphic observations. These functions allow you to perform Stage 1 (uncal to rate), Stage 2 (rate to cal), and to construct the master backgrounds (cal).
An execution template is available at the end of the notebook.
