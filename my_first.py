#!/usr/bin/python
# Sample program or step 1 in becoming a DFIR Wizard!
# No license as this code is simple and free!
import sys
import pytsk3
import datetime
import hashlib
import collections


hashMap = {}

def setup():
    """TODO
    """
    pass

def print_partition_table(partitionTable):
    """Print out the partition table

    In following format,
        addr desc start(start*512) len(mb)

    Args: 
        partitionTable
    """
    if partitionTable:
        print '%-5s %-20s %-20s %-10s' %  \
            ('addr', 'desc' ,'start(start*512)', 'len(mb)')
    for partition in partitionTable:
        print '%-5s %-20s %-20s %-10s' % \
            (partition.addr, partition.desc,
            '%ss(%s)' % (partition.start, partition.start * 512),
            '%s(%s)' % (partition.len,partition.len*512/1024/1024))

def get_partitions():
    """TODO
    """
    partitions = []

    return partitions



def walk_file_system(filesystemObject, parentDirectories = []):
    """Walk through the file system using depth first

    Args:
        filesystemObject
        parentDirectories: default is [] which means it is the top level

    """
    parentDirectory = '/%s' % ('/'.join(parentDirectories))
    fileObject = filesystemObject.open_dir(parentDirectory)
    for entry in fileObject:
        indent = ' ' * 4 * (len(parentDirectories))
        print indent, entry.info.name.name
        if (entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR and
            entry.info.name.name != '.' and entry.info.name.name != '..'):
            parentDirectories.append(entry.info.name.name)
            # Recursion
            walk_file_system(filesystemObject, parentDirectories)
            parentDirectories.pop()
        elif entry.info.meta.type == pytsk3.TSK_FS_META_TYPE_REG:
            if entry.info.meta.size != 0:
                #print 'Do hash'
                filedata = entry.read_random(0, entry.info.meta.size)
                md5hash = hashlib.md5()
                md5hash.update(filedata)
                sha1hash = hashlib.sha1()
                sha1hash.update(filedata)
                fullFilePath = ('%s/%s' % (parentDirectory, entry.info.name.name)).replace('//','/')
                hashMap[fullFilePath] = md5hash.hexdigest()
            else:
                fullFilePath = ('%s/%s' % (parentDirectory, entry.info.name.name)).replace('//','/')
                hashMap[fullFilePath] = 'd41d8cd98f00b204e9800998ecf8427e'


def main():
    #TODO move image loading to a method or util class
    imagefile = './forensic_image/AssignmentImage.dmg'
    imagehandle = pytsk3.Img_Info(imagefile)
    partitionTable = pytsk3.Volume_Info(imagehandle)
    print_partition_table(partitionTable)
    filesystemObject = pytsk3.FS_Info(imagehandle, offset=512)
    #print dir(filesystemObject)

    walk_file_system(filesystemObject)
    print 'The lenght of the dictionary is %d' % len(hashMap)
    rev_multidict = {}
    for key, value in hashMap.items():
        rev_multidict.setdefault(value, set()).add(key)

    for v in [values for key, values in rev_multidict.items() if len(values) > 1]:
        print list(v)

    print '========'
    fileobject = filesystemObject.open_dir("/")

    for a_file in fileobject:
        if a_file.info.meta.type == pytsk3.TSK_FS_META_TYPE_DIR:
            print ''

        #print dir(a_file.info.meta)
        #print (a_file.info.meta.type)
        #print "File Inode:",a_file.info.meta.addr
        #print "File Name:",a_file.info.name.name
        #print "File Creation Time:",datetime.datetime.fromtimestamp(a_file.info.meta.crtime).strftime('%Y-%m-%d %H:%M:%S')
        #outfile = open('tmp/%s' % a_file.info.name.name, 'w')
        #filedata = a_file.read_random(0,a_file.info.meta.size)
        #outfile.write(filedata)


if __name__ == '__main__':
    main()