#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 17:33:33 2023
@author: fordb
Volumetric postprocessor for semiautomated cmb detection

Takes the result_[rootName].txt as an input argument, and loads the 
nonproj_cmbseg_v5_threshdeg2x5scaled_[rootname].nii assuming it is in the same
directory. It computes the clusters in the nii, and loads the CMBs from the 
result file. It tries to match the results to the nii file based on each 
individual cmb volume, as well as the slices (assumed to be z-coords) that
the cmb spans. As long as the data are not peppered with cmbs, it should not
fail. As-is, this script just flops over if there is not a nice one-to-one
match of cmbs from the text file to specific rois in the .nii file. 

Would be good to improve that in the future probably

"""
import re, sys, os
import nibabel as nib
import numpy as np
from scipy.ndimage import label


txtfile_path = None

# Check if the command line argument for the file path is provided
if len(sys.argv) < 2:
    print("Please provide the path to the cmb result_[rootName].txt file as a command line argument.")
    print("The nonproj_cmbseg_v5_threshdeg2x5scaled_[rootname].nii should be in the same directory.")
    #sys.exit(1)
    txtfile_path = "/home/fordb/Desktop/microbleed_testing/_ob_pad/result_0a070a45d388c728c25604b5e29b55a1_pad.txt"

else:
    txtfile_path = sys.argv[1]

directory, filename = os.path.split(txtfile_path)
file_name, file_extension = os.path.splitext(filename)
nii_file_name = file_name.replace("result_","nonproj_cmbseg_v5_threshdeg2x5scaled_")
niifile_path = os.path.join(directory, nii_file_name) + ".nii"
#niifile_path = "/home/fordb/Desktop/microbleed_testing/_ob_pad/nonproj_cmbseg_v5_threshdeg2x5scaled_0a070a45d388c728c25604b5e29b55a1_pad.nii"
img = nib.load(niifile_path)
data = img.get_fdata()
voxel_dimensions = img.header.get_zooms()
voxel_volume = voxel_dimensions[0] * voxel_dimensions[1] * voxel_dimensions[2]
zSize = data.shape[2]

labeled_data, num_clusters = label(data)
unique_values = np.arange(1, num_clusters + 1)
labeled_clusters = np.where(labeled_data > 0, unique_values[labeled_data - 1], 0)

unique_values, value_counts = np.unique(labeled_clusters, return_counts=True)
reported_data = np.zeros((int(np.max(unique_values)+1), 2), dtype=object)

# Iterate over unique values
for i in range(int(np.max(unique_values)+1)):
    # Find voxel coordinates where value occurs
    coordinates = np.where(labeled_clusters == i)
    z_coordinates = np.unique(coordinates[2])
    try:
        #print(f"Number of Voxels: {value_counts[np.where(unique_values == i)][0]}")
        reported_data[i, 0] = value_counts[np.where(unique_values == i)][0]
    except:
        #print("Number of Voxels: 0")
        reported_data[i, 0] = 0
    try:
        #print(f"Unique Z Coordinates: {z_coordinates.tolist()}")
        reported_data[i, 1] = z_coordinates.tolist()
    except:
        #print("Unique Z Coordinates: None")
        reported_data[i, 1] = []
    print("Val:"+str(i)+", "+str(reported_data[i, 0])+" vox, zspan "+\
          str(min(reported_data[i, 1]))+":"+str(max(reported_data[i, 1])))

delimiters = r" is | cubic mm and found on slice | and found on slice "

#this list will be a list of lists
#[CMB#, CMB Size in Voxels, List of z coordinates this CMB spans, List of ROI matches from nii]
cmbData = []
# Open the file and read its contents line by line
with open(txtfile_path, "r") as file:
    for line in file:
        line = line.strip()  # Remove leading/trailing whitespace and newline characters
        if line.startswith("CMB #"):
            #print(line)  # Print the line that begins with " CMB #"
            fline = line[5:]
            flineList = re.split(delimiters, fline)
            fflineList = []
            fflineList.append(int(flineList[0]))
            fflineList.append(int(round(float(flineList[1])/voxel_volume)))
            fflineList.append([int(value)- 1  for value in flineList[2:]])
            # the -1 accounts for 0 vs 1 start indexing
            fflineList.append([])
            cmbData.append(fflineList)
            print(fflineList)
            for j in range(len(reported_data)):
                if fflineList[1] == reported_data[j,0]:
                    if fflineList[2] == reported_data[j,1]:
                        print("Matched CMB " +str(fflineList[0])+" w/ROI "+str(j))
                        cmbData[-1][-1].append(j)
            
#now generate a new nii with the cmbs labelled to match the results file. 
if len(cmbData) > 0:
    #actually need to write a new file
    newNiiData = np.zeros_like(data)
    successes = 0
    failures = 0
    for cmb in cmbData:
        if len(cmb[3]) == 1:
            #single match, process file
            newNiiData += np.multiply(labeled_clusters == cmb[3][0], cmb[0])
            successes += 1
        else:
            print("Found " +str(len(cmb[3])) + " matching ROIs for CMB# " + str(cmb[0]))
            failures += 1

    print("Successfully identified " + str(successes) + " of " + str(successes+failures)+ " cmbs")
    if failures == 0:
        #write the new file
        newNiiImg = nib.Nifti1Image(newNiiData, img.affine, img.header)
        outfile = os.path.join(directory, file_name.replace("result_","result_cmbs_")) + ".nii.gz"
        nib.save(newNiiImg, outfile)
        print("New results volume written to: " + outfile)
    else:
        print("Did not write new nii.gz file because of an inability to ensure accurate identification")
else:
    print("No cmbs detected in this dataset, not writing an output .nii.gz")