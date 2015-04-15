#! /usr/bin/python
##gets the smoothness of each subject to average and use for 3dClustSim for thresholding
import os
import sys
import glob
import string
import subprocess

PREF_DIR = '/Users/dardenne/Desktop/RE_fMRI' #data directory
scripts = 'scripts' #scripts directory (where subject list is)
subject_list = os.path.join(PREF_DIR, scripts, 'subject_list.txt')
final_smooth = os.path.join(PREF_DIR,scripts,'smoothness.txt')  #output file for all the smoothness data

#read subject file (list of all subids) and put them in subjects
subjects = []
subj_file = open(subject_list,'r')
for subj in subj_file.readlines():
	subj = subj.strip('\n')
	subj = subj.strip('/')
	subjects.append(subj)
subj_file.close()

#loop through subjects
for subj in subjects:
	
	data_path = os.path.join(PREF_DIR, 'data',subj,'brik',subj+'.results/') #AFNI data dir

	#local smoothness file for each subject
	smoothness_file = data_path + 'smoothness.txt'
	if os.path.exists(smoothness_file): #remove old if it exists already
		os.system('rm ' + smoothness_file)
	
	#afni command for estimating smoothness
	cmd_str = '3dFWHMx -arith -mask ' + data_path + 'mask_anat.' + subj + '+tlrc -dset ' + data_path + 'GLM_residuals+tlrc -out ' + smoothness_file
	print cmd_str
	#nasty subprocess stuff to assign the output of a shell script to a variable
	proc=subprocess.Popen(cmd_str,shell=True,stdout=subprocess.PIPE, )
	output = proc.communicate()[0]
	output = output.strip('\n')
	output = output.split('  ')

	# compile smoothness data to a text file
	s_file = open(final_smooth,'a')
	s_file.write(str(float(output[0])))
	s_file.write('\t')
	s_file.write(str(float(output[1])))
	s_file.write('\t')
	s_file.write(str(float(output[2])))
	s_file.write('\n')
	s_file.close()

	print "finished " + subj + "!!"

#Take average across subjects, then use this command once to run simulation
# 3dClustSim -mask master_funcres+tlrc -fwhmxyz 3.2647 3.0611 2.9082 -pthr .05 .02 .01 .005 .001