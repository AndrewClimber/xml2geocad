# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import configparser as CP
import os, sys


def printHeader(handle):
    handle.write("!Geocad Enterprise Edition 1.1"+'\n')
    handle.write("!2018-10-31 15:17:08"+'\n')
    handle.write("!#BLOCK0=BLOCK0"+'\n')
    handle.write("!$Наименование"+'\n')
    handle.write("!$Код"+'\n')
    handle.write("#BLOCK0"+'\n')
    handle.write("$"+'\n')
    handle.write("$2663230"+'\n')
    handle.write("+0"+'\n')


def printZoneRecord(outstr, handle, ord_nmb):
    if ord_nmb < printZoneRecord.ord_nmb:
        printZoneRecord.ord_nmb = ord_nmb
        handle.write('+0'+'\n')
        handle.write(outstr+'\n')
    else:
        printZoneRecord.ord_nmb = ord_nmb
        handle.write(outstr+'\n')

def openFile(outfile):
    try:
        handle = open(outfile, "a")
    except IOError:
        print("IOError:", outfile)
        sys.exit()
    return handle

def getZoneRecord(inpath, XMLfile, outpath, outfile):
    try:
        tree = ET.parse(inpath+XMLfile)
        root = tree.getroot()
    except ET.ParseError:
        print('Parsing error. Bad XML:',inpath+XMLfile)
        sys.exit()
    i = getZoneRecord.file_num
    handle_list = openFile(outpath+'reestr'+'.lst')
    for zones in tree.iter('zones_and_territories_record'):
        for reg_num in zones.iter('reg_numb_border'):
            handle_list.write(str(i)+' '+reg_num.text)
        for type_zone in zones.iter('type_zone'):
            for value in type_zone.iter('value'):
                handle_list.write(' '+value.text+'\n')
        print(outfile)
        handle = openFile(outpath+outfile)
        printHeader(handle)
        for ordinate in zones.iter('ordinate'):
            for x in ordinate.iter('x'):
                outstr = x.text + '\t'
            for y in ordinate.iter('y'):
                outstr = outstr + y.text
            for ord_nmb in ordinate.iter('ord_nmb'):
                outstr = ord_nmb.text + '\t' + outstr
                printZoneRecord(outstr.replace('.',','), handle, int(ord_nmb.text))
        handle.close()
        printZoneRecord.ord_nmb = 1
        i += 1
        outfile = str(i)+'.txt'

    getZoneRecord.file_num = i



def main():
    printZoneRecord.ord_nmb = 1
    getZoneRecord.file_num = 1
    conf = CP.ConfigParser()
    conf.read('config.ini')

    for f in os.listdir(conf['path']['outputdir']):
        os.remove(conf['path']['outputdir']+f)


    printZoneRecord.outfile = conf['files']['startfile']
    for f in os.listdir(conf['path']['inputdir']):
        print(f)
        getZoneRecord(conf['path']['inputdir'], f, conf['path']['outputdir'], str(getZoneRecord.file_num)+'.txt')

if __name__ == "__main__":
    main()
