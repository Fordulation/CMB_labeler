This is a fork of https://github.com/LupoLab-UCSF/CMB_labeler, unpacked and updated to fix broken functionality.

# ORIGINAL AUTHORS/CONTRIBUTORS:
Wei Bian, Melanie A. Morrison, Xiaowei Zhu, Sivakami Avadiappan, Yicheng Chen, Seyedmehdi Payabvash, Mihir Shah, Christopher. P. Hess, Janine M. Lupo 

# REVELANT PUBLICATIONS: 
*They requested that you cite the following publications when using their software in your research.*

Morrison MA, Payabvash S, Chen Y, Avadiappan S, Shah M, Bian W, Zou X, Hess C, Lupo JM. A user-guided tool for semi-automated cerebral microbleed detection and volume segmentation: evaluating vascular injury and data labelling for machine learning; 2018, NeuroImage: Clinical, 20: 498-505.

Bian W, Hess CP, Chang SM, et al. Computer-aided detection of radiation-induced cerebral microbleeds on susceptibility-weighted MR images. NeuroImage Clin 2013; 2:282–90.

# INPUT: 
The algorithm accepts a single, non-projected volumetric T2*-weighted or SWI dataset in NIFTI format (.nii). 
A file with input parameters called cmb_threshold is also required. This file is included; a detailed description of each parameter can be found in Bian et al. 2013.

# OUTPUT: 
Primary outputs include:

a) scaled_[rootName].nii – image scaled to [0,255]

b) FRST_map_masked[rootName].nii – cmb candidates after FRST

c) FRST_Vessel_mask[rootName].nii – mask of vessels 

d) cmb[rootName].nii – cmb candidates after region growing 

e)  nonproj_cmbseg_v5_thresdeg2x5final_usercorrected[rootName].nii – *final cmb candidates*

f) nonproj_cmbseg_v5_thresdeg2x5denoised[rootName].nii – all cmb candidates automatically removed at denoising stage

g)  nonproj_cmbseg_v5_thresdeg2x5false_positives[rootName].nii – all cmb candidates manually removed as false positives by the user

h) result_[rootName].txt – a text file containing all cmb counts and cmb volumes
   
# FORMAT: 
MATLAB Protected Files 

# USAGE: 


1) Download cmb_detection_2018_nifti_protected.zip
2) Download Imagine-Legacy-master.zip (NEW JULY 2020)
3) Replace the Imagine directory currently in the cmb_detection_2018_nifti_protected directory with Imagine-Legacy-master
4) Add cmb_detection_2018_nifti_protected and sub folders to your path
5) cd to the test_subect directory or your equivalent subject directory with your swi.nii file (this will also be the output directory)
6) run the following:

cmb_detection('input file','path to cmb_threshold parameter file in directory','diagnostics flag','semi-automatic detection flag');

e.g. 
cmb_detection(‘test_swi.nii’, ‘/yourPath/cmb_detection_2018_nifti_protected’, ‘diagoff’, ‘semion’);

*When diagoff, the script runs faster and does not produce intermediate files for optimization purposes.

*When semion, the user-guided classification is enabled.

Note: Please use MATLAB version(s) R2017+ for full functionality (i.e. slice scroll, window zoom) of the user-guided GUI. 

Update 2021: Please use cmbevaluation2.p recently uploaded instead of the version in the .zip folder IF you wish to run SEMIOFF (i.e. fully automated, though output will have false positives)

# PERFORMANCE: 
The algorithm was optimized on a 7T SWI dataset acquired from 10 adult brain tumor patients with radiological evidence of CMBs following radiation therapy. The overall sensitivity is 86.7%. Performance measures will vary with user classification outcomes.

# TEST SET: 
A test set has been included in this repository. This includes 10 SWI datasets with radiotherapy-induced cerebral microbleed. Five were acquired on a 3T GE system (P01-P05), the other 5 were acquired on a 7T GE system (P06-P10).

# USER SUPPORT:
Melanie A. Morrison 
E: melanie.morrison@ucsf.edu, melanie.morrison@hotmail.com
