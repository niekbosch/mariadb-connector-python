#!/usr/bin/env python

import sys
import os
import string

class MariaDBConfiguration():
  lib_dirs= ""
  libs= ""
  version= ""
  includes= ""

def mariadb_config(config, option):
  from os import popen
  file= popen("%s --%s" % (config, option))
  data= file.read().strip().split()
  rc= file.close()
  if rc:
    if rc/256:
      data= []
    if rc/256 > 1:
      raise EnvironmentError("mariadb_config not found.\nMake sure that MariaDB Connector/C is installed (e.g. on Debian or Ubuntu 'sudo apt-get install libmariadb-dev'\nIf mariadb_config is not installed in a default path, please set the environment variable MARIADB_CONFIG which points to the location of mariadb_config utility, e.g. MARIADB_CONFIG=/opt/mariadb/bin/mariadb_config")
  return data


def dequote(s):
  if s[0] in "\"'" and s[0] == s[-1]:
   s = s[1:-1]
  return s

def get_config():
  required_version="3.1.0"
  no_env= 0

  try:
    config_prg= os.environ["MARIADB_CONFIG"]
  except KeyError:
    config_prg= 'mariadb_config'

  cc_version= mariadb_config(config_prg, "cc_version")
  if cc_version[0] < required_version:
    print ('MariaDB Connector/Python requires MariaDB Connector/C >= %s, found version %s' % (required_version, cc_version[0]))
    sys.exit(2)
  cfg= MariaDBConfiguration()
  cfg.version= cc_version[0]

  libs= mariadb_config(config_prg, "libs")
  cfg.lib_dirs = [ dequote(i[2:]) for i in libs if i.startswith("-L") ]
  cfg.libs = [ dequote(i[2:]) for i in libs if i.startswith("-l") ]
  includes= mariadb_config(config_prg, "include")
  mariadb_includes = [ dequote(i[2:]) for i in includes if i.startswith("-I") ]
  mariadb_includes.extend(["./include"])
  cfg.includes= mariadb_includes
  return cfg
