#!/usr/bin/python
# Google Weather Jabber-service
#
# copyright 2011 Verzakov Maxim aka xam_vz 
#
# License: GPL-v3
#
import ConfigParser
import sys

from twisted.internet import reactor

import j2j

def info():
    print('\nUsage: main PATH\n\n\tPATH: the path to the configuration \
file\n')

def main(conf):
    version = '0.0'
    config = ConfigParser.ConfigParser()
    config.read(conf)
  
    try:
        jid = config.get('component', 'jid')
        password = config.get('component', 'password')
        host = config.get('component', 'host')
        port = config.get('component', 'port')
    except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
        print('\n Wrong configuration file\n')
        return
    c = j2j.j2jComponent(version, config, jid)
    c.connect(port, password, host)
    reactor.run() 

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        info()
