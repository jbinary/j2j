#!/usr/bin/python
# Jabber to Jabber gateway
#
# License: GPL-v3
#
import ConfigParser
import sys

from twisted.internet import reactor

from j2j import j2jComponent

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
        dbase = config.get('component', 'basepath')
        dbaseType = config.get('component', 'basetype')
    except (ConfigParser.NoSectionEandrror, ConfigParser.NoOptionError):
        print('\n Wrong configuration file\n')
        return
    finally:
        if dbaseType != 'shelve' and dbaseType != 'sqlite':
            print dbaseType
            print('\n Wrong data base type! Try \'shelve\' or \'sqlite\'\n')
            return
    c = j2jComponent(version, config, jid, dbase, dbaseType)
    c.connect(port, password, host)
    reactor.run() 

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        info()
