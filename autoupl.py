#!/bin/python3

import sys, os, subprocess, shutil, random, string, shutil
from os.path import join

token = "amGC6IVPCONBLfo5M6A5E1vIZcQiNS"
if len(sys.argv) > 1:
    token = sys.argv[1]

# FILL THIS OUT
EMAIL = "oski@berkeley.edu"
OK_ASSIGNMENT = "cal/cs61a/sp19/proj01contest"

DEPLOY_SSH = False
# if copy local
DEPLOY_PATH = "/home/hogcon/public_html"

# if using ssh
SSH_USER, SSH_PASS, SSH_PATH = "oski", "oskipass", "ssh.berkeley.edu:public_html/hog.html"
SCP, SCP_PW = "scp", False
# END
    
PY_EXE = sys.executable
PROJ_DIR = os.path.dirname(os.path.abspath(__file__))
CONTESTPY_PATH = join(PROJ_DIR, 'contest.py')
HOGHTML_PATH = join(PROJ_DIR, 'hoghtml.py')
OK_PATH = join(PROJ_DIR, 'ok')
OK_TOKEN_CMD = "--get-token"
OK_SUBM_API_URL = "https://okpy.org/api/v3/assignment/" + OK_ASSIGNMENT + "/submissions?access_token="
SUBM_FILE_NAME = "hog_contest.py"

TEMPLATE_FILE, OUT_FILE = "hog.template.html", "hog.html"

def execute(command, input = "", pipe_output = False):
    print ("---------------------------------")
    print ("autoupl.py: Executing " + command)
    if pipe_output:
        process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, input=input)#, encoding='UTF-8')
    else:
        process = subprocess.run(command, shell=True, input=input)#, encoding='UTF-8')
    return process.stdout

if not token:
    token = execute(PY_EXE + " " + OK_PATH + ' ' + OK_TOKEN_CMD, EMAIL, True).split('\n')[3].split()[1].strip()
else:
    print ("Using provided Okpy security token.")
dirname = "hc" + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(14))
print("randomly generated directory name: " + dirname)

import json, urllib.request
with urllib.request.urlopen(OK_SUBM_API_URL + token) as response:
   html = response.read().decode('UTF-8')
   jsonfile = json.loads(html)
   if jsonfile['code'] != 200:
       print('OKPY API HTTP error: ' + str(jsonfile['code']))
       sys.exit(0)
   dat = jsonfile['data']
   
   cnt = 0
   for subm in dat['backups']:
       if not subm['submit']: continue
       out_name = '-'.join((x['email'] for x in subm['group']))
       for msg in subm['messages']:
            if SUBM_FILE_NAME in msg['contents']:
                contents = msg['contents'][SUBM_FILE_NAME]
                break
       else:
            continue
       cnt += 1
       subm_dir = join(dirname, out_name)
       os.makedirs(subm_dir)
       contents = contents.replace('\t', '    ') # fix tabs
       with open(join(subm_dir, SUBM_FILE_NAME), 'w', encoding="UTF-8") as f:
           f.write(contents)
   print("{} submissions downloaded from Okpy.org".format(cnt))
   execute(PY_EXE + " " + CONTESTPY_PATH + ' ' + dirname)
   execute(PY_EXE + " " + HOGHTML_PATH + ' ' + TEMPLATE_FILE + ' results.txt ' + OUT_FILE)
   if DEPLOY_SSH:
       if SSH_PASS:
           execute(SCP + (" -pw \"" + SSH_PASS + "\"" if SCP_PW else "") + " \"" + OUT_FILE + "\" " + SSH_USER + "@" + SSH_PATH)
   else:
       print("Deploying to", DEPLOY_PATH)
       shutil.copy(OUT_FILE, DEPLOY_PATH)
   
shutil.rmtree(dirname, True) # clean up
