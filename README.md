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
1) scaled_[rootName].nii – image scaled to [0,255]
2) FRST_map_masked[rootName].nii – cmb candidates after FRST
3) FRST_Vessel_mask[rootName].nii – mask of vessels 
4) cmb[rootName].nii – cmb candidates after region growing 
5) nonproj_cmbseg_label_v5_thresdeg2x5scaled_[rootName].nii – an *n*ary mask of the cmb candidate rois. 
6) nonproj_cmbseg_v5_threshdeg2x5scaled_[rootName].nii – a binary mask for all cmb candidate voxels. 
7) nonproj_cmbseg_v5_thresdeg2x5denoisedscaled_[rootName].nii – all cmb candidates automatically removed at denoising stage
8) nonproj_cmbseg_v5_thresdeg2x5final_usercorrectedscaled_[rootName].nii – Original documentation was incorrect, but this appears to be a binary representation of the cmd candidates removed automatically at denoising as well as removed via user correction. Unfortunately this is missing some ROI automatically removed, so it cannot be used as an exclusionary mask in combination with output (5) or (6) to produce a final volume of potential cmbs.
9) result_[rootName].txt – a text file containing all cmb counts and cmb volumes - BUT NOT LOCATIONS!

   
# FORMAT: 
MATLAB Protected Files 

# PREREQUISITES: 
1) MATLAB installed with statistics and machine learning toolbox

# USAGE: 
1) Add cmb_detection_2018_nifti_protected and sub folders to your matlab path
2) In matlab, cd to the test_subect directory or your equivalent subject directory with your swi.nii file (this will also be the output directory)
3) Run the following:
```>> cmb_detection('input file','path to cmb_threshold parameter file in directory','diagnostics flag','semi-automatic detection flag');```
e.g. 
```>> cmb_detection(‘test_swi.nii’, ‘/yourPath/cmb_detection_2018_nifti_protected’, ‘diagoff’, ‘semion’);```


*When diagoff, the script runs faster and does not produce intermediate files for optimization purposes.
*When semion, the user-guided classification is enabled.
Note: Please use MATLAB version(s) R2017+ for full functionality (i.e. slice scroll, window zoom) of the user-guided GUI. 
Update 2021: Please use the base directory cmbevaluation2.p instead of the version in cmb_detection_2018_nifti_protected IF you wish to run SEMIOFF (i.e. fully automated, though output will have false positives)

# PERFORMANCE: 
The algorithm was optimized on a 7T SWI dataset acquired from 10 adult brain tumor patients with radiological evidence of CMBs following radiation therapy. The overall sensitivity is 86.7%. Performance measures will vary with user classification outcomes.

# TEST SET: 
A test set is available in the original repository (https://github.com/LupoLab-UCSF/CMB_labeler), but removed in this repository. 

# USER SUPPORT (ORIGINAL):
Melanie A. Morrison 
E: melanie.morrison@ucsf.edu, melanie.morrison@hotmail.com
