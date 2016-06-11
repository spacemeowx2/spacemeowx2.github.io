#coding: utf-8
import os
import sys
import re
import shutil
import codecs

def isSpaceWrote(parent):
    return not re.match(r'.*\d{8}\\space$', parent) == None
def getDateFromParent(parent):
    m = re.match(r'.*(\d{4})(\d{2})(\d{2})\\space$', parent)
    return '-'.join(m.groups())
def procMarkdown(content, date):
    tmpl = u'''---
title: \g<1>
date: %s
categories: tech
tags: []
---
''' % (date)
    return re.sub(r'^# ([^\r\n].*)', tmpl, content, count=1)
def getTitle(content):
    return re.search(r'title: ([^\r\n].*)', content).groups()[0].strip()
def imageList(content):
    m = re.findall(r'!\[.*?\]\((.*?)\)', content)
    return m
def virName(name):
    name = name.replace('_', '__')
    name = name.replace('/', '_')
    return name
def replaceImages(content, title):
    def rep(m):
        desc, url = m.groups()
        url = title + '/' + virName(url)
        return '![%s](%s)' % (desc, url)
    return re.sub(r'!\[(.*?)\]\((.*?)\)', rep, content)
def readFile(filename):
    with codecs.open(filename, 'r', 'utf-8') as file:
        return file.read()
def writeFile(filename, content):
    with codecs.open(filename, 'w', 'utf-8') as file:
        file.write(content)
def copyFileList(basePath, fileList, toPath):
    for filename in fileList:
        virname = virName(filename)
        filename = os.path.normpath(filename)
        oriFile = os.path.join(basePath, filename)
        destFile = os.path.join(toPath, virname)
        print destFile
        destPath = os.path.split(destFile)[0]
        if not os.path.exists( destPath ):
            os.makedirs(destPath)
        shutil.copyfile(oriFile, destFile)
def fileNameFilter(filename):
    filename = re.sub(r'[\\\/:\*\?"<>\| ]', '_', filename)
    filename = filename.replace('\r', '').replace('\n', '')
    return filename
'''
2016Sprint
├── 20160516
│   └── space
│       ├── README.md
│       └── img
└── 20160520
...
'''
def main(seasonDir):
    DEFAULT_FILENAME = 'README.md'
    POST_DIR = os.path.normpath('source/_posts')
    for parent,dirnames,filenames in os.walk(seasonDir):
        if isSpaceWrote(parent):
            wDate = getDateFromParent(parent)
            #wTitle = 
            for filename in filenames:
                if filename.split('.')[-1] != 'md':
                    continue
                inputFilename = os.path.join(parent, filename)
                content = readFile(inputFilename)
                content = procMarkdown(content, wDate)
                title = getTitle(content)
                if len(title) == 0:
                    print inputFilename, ' title not found, skip'
                    continue
                
                titleFilename = fileNameFilter(title)
                print titleFilename
                mdFilename = os.path.join(POST_DIR, titleFilename+'.md')
                mdPath = os.path.join(POST_DIR, titleFilename)
                #print imageList(content)
                if not os.path.exists( mdFilename ):
                    usedFile = imageList(content)
                    content = replaceImages(content, titleFilename)
                    if len(usedFile) > 0:
                        copyFileList(parent, usedFile, mdPath)
                        pass
                    
                    writeFile(mdFilename, content)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print "usage: git2source.py <season dir>"