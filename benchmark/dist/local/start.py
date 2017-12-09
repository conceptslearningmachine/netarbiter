#!/usr/bin/python
# Author: Hee Won Lee <knowpd@research.att.com>
# Created on 12/8/2017

config_file = 'config.yaml'

import os, sys, subprocess, copy, yaml

def run_bash(cmd):
    #proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,  shell=True, executable='/bin/bash')
    #(stdout, stderr) = proc.communicate()
    #return stdout + stderr

    # Refer to http://stackoverflow.com/questions/4417546/constantly-print-subprocess-output-while-process-is-running
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    # Poll process for new output until finished
    while True:
        nextline = process.stdout.readline()
        if nextline == '' and process.poll() is not None:
            break
        sys.stdout.write(nextline)
        sys.stdout.flush()

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        raise exitCode

# Read config.yaml
with open(config_file) as stream:
    config = yaml.load(stream)

# Preclude items that are `enabled = false`
myconf = copy.deepcopy(config)
conf_disabled= []
for k1, v1 in config.iteritems():
    for k2, v2 in v1.iteritems():
        if k2 == 'enabled' and v2 == False:
            conf_disabled.append(k1)
            myconf.pop(k1)
# For debugging
#print conf_disabled
#print myconf

# Add to environment variables
myenv = {}
for k1, v1 in myconf.iteritems():
    for k2, v2 in v1.iteritems():
        if k2 == 'env':
            for k3, v3 in v2.iteritems():
                var = k1.upper() + '_' + k3.upper()
                myenv[var] = str(v3)
                os.environ[var] = str(v3)
                #print  var + ' = ' + str(v3)

# For debugging
#print myenv
#print os.getenv('INFLUXDB_IP', '')
#print os.environ.get('INFLUXDB_IP')
#print os.environ

# Run
run_bash('cd fio; ./run.sh')
