#!/bin/python3

import sys, os, subprocess, shutil
from os.path import join

FILE_NAME = 'hog_contest.py'
OUTPUT_PATH = 'results.txt'
N_THREADS = 4

# option to include 'staff solution' on leaderboard
STAFF_SOLN_PATH = ""#"staff_soln_dp.strat"

PY_EXE = sys.executable
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
STRAT_DIR = join(PROJ_DIR, 'strat')
HOGCONV_PATH = join(PROJ_DIR, 'hogconv.py')
BACON_PATH = join(PROJ_DIR, 'bin/bacon')

if len(sys.argv) <= 1:
    print ("Welcome to the Hog Contest simulation tool (c) Alex Yu (sxyu@berkeley.edu) 2018.\n")
    print ("Usage: python[3] contest.py [submission_root_directories] [-o output_name = results.txt] [-n submission_filename = hog_contest.py] [-t num_threads = 4]\n")
    print ("Example: python3 contest.py -n hog_contest.py -o results.txt ~/hog_contest/")
    sys.exit(0)
    
def execute(command, quiet = False):
    print ("---------------------------------")
    print ("contest.py: Executing " + command)
    if quiet:
        FNULL = open(os.devnull, 'w')
        process = subprocess.Popen(command, shell=True, stdout=FNULL)
    else:
        process = subprocess.Popen(command, shell=True)
    process.wait()
    
# clear and recreate strategy directory
if os.path.exists(STRAT_DIR):
    if os.path.isdir(STRAT_DIR):
        shutil.rmtree(STRAT_DIR)
    else:
        os.remove(STRAT_DIR)
os.makedirs(STRAT_DIR)
    
subm_paths = []
strat_paths = []
change_arg = ""

for arg in sys.argv:
    if arg in ['-n', '-o', '-t']:
        change_arg = arg
        continue
    if change_arg:
        if change_arg == '-n':
            FILE_NAME = arg
        elif change_arg == '-o':
            OUTPUT_PATH = arg
        elif change_arg == '-t':
            N_THREADS = int(arg)
            
        change_arg = ''
        continue
        
    root = arg
    
    if root == '':
        root = '.'
        
    for root, subdirs, files in os.walk(root):
        for file in files:
            if file == FILE_NAME:
                subm_paths.append('"' + join(root, file) + '"')

execute(PY_EXE + ' ' + HOGCONV_PATH + ' -o "' + STRAT_DIR + '" ' + ' '.join(subm_paths))

for root, subdirs, files in os.walk(STRAT_DIR):
    for file in files:
        strat_paths.append('"' + join(root, file) + '"')
        
if STAFF_SOLN_PATH:
    strat_paths.append('"' + STAFF_SOLN_PATH + '"')

if strat_paths:        
    execute(BACON_PATH + ' -rm all', True)
    execute(BACON_PATH + ' -i -f ' + ' '.join(strat_paths))
    execute(BACON_PATH + ' -t ' + str(N_THREADS) + ' -f ' + OUTPUT_PATH)

    print ("contest.py: All Done. Results saved to: " + OUTPUT_PATH)
else:
    print ("contest.py: No strategies converted! Exiting...")
