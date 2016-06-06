#!/usr/bin/python
# Sample program or step 1 in becoming a DFIR Wizard!
# No license as this code is simple and free!
import sys
import pytsk3

def setup():
    pass

def print_partition_table(partitionTable):
    """Print out the partition table

    In following format,
        addr desc start(start*512) len(mb)

    Args: 
        partitionTable
    """
    if partitionTable:
        print '%-5s %-20s %-20s %-10s' % ('addr', 'desc' ,'start(start*512)', 'len(mb)')
    for partition in partitionTable:
        print '%-5s %-20s %-20s %-10s' % \
            (partition.addr, partition.desc, 
            '%ss(%s)' % (partition.start, partition.start * 512), '%s(%s)' % (partition.len,partition.len*512/1024/1024))


def main():
    imagefile = './forensic_image/AssignmentImage.dmg'
    imagehandle = pytsk3.Img_Info(imagefile)
    partitionTable = pytsk3.Volume_Info(imagehandle)
    print_partition_table(partitionTable)


if __name__ == '__main__':
    main()