
import os
import platform
import sys
import binascii
import ctypes
import datetime
import time

from readwritecompare import readwritecompare
from workload import workload

def __usage():
    print 'NVMe Drive IO Exerciser for Linux (with inbox driver)'
    print ''
    print 'USAGE:'
    print '\tpython trimio.py [device] [workload type] [startLBA (only with work load type 0)] [number of blocks (only with work load type 0)] [Block size (in multiple of 512)] [pattern (in hex )]'
    print ''
    print '\tOptions - '
    print '\t\t-h or --help    # displays this output'

    print ''
    print 'workload types  and usage :'
    print '\t workload type 0 or -wl0: \n'
    print '\t This workload allows user to custom select Start LBA and number of LBAs user wants to perform write/read/compare/trim/read/compare  \n'
    print '\t Usage : python trimio.py /dev/nvme4n1 -wl0 0x1100 -nb12 -bs2 0xdd '
    print '\t -nb12: means number of blocks of block size , here it is 12 blocks'
    print '\t -bs2: means block size of 2 (in multiple of 512 bytes)'
    print '\t workload type 1 or -wl1: \n'
    print '\t This workload allows user to  perform write/read/compare/trim/read/compare all over the disk space touch every LBAs and does in a contious loop \n'
    print '\t Usage : python trimio.py /dev/nvme4n1 -wl1 -bs4 0xdd '
    print '\t workload type 0 or -wl0: \n'
    print '\t This workload allows user to perform preconditioning over the drive with twice drive write.   \n'
    print '\t Usage : python trimio.py /dev/nvme4n1 -wl2 0x1100 -nb128 -bs4 0xdd '


if __name__ == '__main__':

    if ('-h' in sys.argv) or ('--help' in sys.argv) or ('-?' in sys.argv):
        __usage()
        sys.exit(0)

    device= sys.argv[1]
    workload_type =0
    rwc = readwritecompare(device)
    driveNumber = int(rwc.get_device_number(device))
    wl = workload(driveNumber)

    workload_type = int(sys.argv[2].replace('-wl',''))



    if workload_type == 0 :
        startLba = sys.argv[3]
        num_blocks = int(sys.argv[4].replace('-nb',''))
        block_size = int(sys.argv[5].replace('-bs',''))
        pattern = sys.argv[6]
        print "\n Disk running : ",device.replace('/dev/','')
        print "\n Starting LBA : ",startLba
        print "\n Number of Blocks : ",num_blocks
        print "\n Block Size : ",block_size
        print "\n Patter Used : ",pattern.replace("0x", ""),"  in hex"
        print "\n \n IO started at ", datetime.datetime.utcnow()
        wl.wl_type0(rwc, startLba, num_blocks, block_size, pattern)
        print "\n IO Finished at ",datetime.datetime.utcnow()
    elif workload_type == 1 :
        block_size = int(sys.argv[3].replace('-bs',''))
        startLba = '0x0000'
        size = rwc.get_disk_size(device)
        num_blks_disk_available = int(size) / 512
        num_blocks = num_blks_disk_available
        num_blocks = num_blks_disk_available / block_size
        pattern = sys.argv[4]
        print "\n Disk running : ", device.replace('/dev/', '')
        print "\n Starting LBA : ", startLba
        print "\n Number of Blocks : ", num_blocks
        print "\n Block Size : ", block_size
        print "\n Patter Used : ", pattern.replace("0x", ""), "  in hex"
        print "\n \n IO started at ", datetime.datetime.utcnow()
        print "\n \n Press CTRL+C to stop program mannually "
        wl.wl_type1(rwc, startLba, num_blocks, block_size, pattern)
        print "\n IO Finished at ", datetime.datetime.utcnow()
    elif workload_type == 2:
        block_size = int(sys.argv[3].replace('-bs', ''))
        startLba = '0x0000'
        size = rwc.get_disk_size(device)
        num_blks_disk_available = int(size) / 512
        num_blocks = num_blks_disk_available
        num_blocks = num_blks_disk_available / block_size
        pattern = sys.argv[4]
        print "\n Disk running : ", device.replace('/dev/', '')
        print "\n Starting LBA : ", startLba
        print "\n Number of Blocks : ", num_blocks
        print "\n Block Size : ", block_size
        print "\n Patter Used : ", pattern.replace("0x", ""), "  in hex"
        print "\n \n IO started at ", datetime.datetime.utcnow()
        print "\n \n Press CTRL+C to stop program mannually "
        wl.wl_type2(rwc, startLba, num_blocks, block_size, pattern)
        print "\n IO Finished at ", datetime.datetime.utcnow()



def __usage():
    print 'NVMeIOCTLCLI Version Beta - Compliant to NVMe 1.1b'
    print ''
    print 'USAGE:'
    print '\tpython NVMeIOCTLCLI.py [OPTIONS] COMMAND [COMMAND ARGUMENTS] [CONTROLLER] [NAMESPACE]'
    print ''
    print '\tOptions - '
    print '\t\t-h or --help    # displays this output'
    print '\t\t-v or --verbose # show the NVMe commands that are sent and the NVMe completions that are returned'
    print ''
    print '\tCommands - '
    print '\t\t-lc or --list-controllers         # lists all NVMe controllers in the system'
    print '\t\t-ic or --identify-controller      # issues and Identify Controller to the specified controller'
    print '\t\t-in or --identify-namespace       # issues an Identify Namespace to the specified namespace'
    print '\t\t-il or --identify-namespace-list  # issues an Identify Namespace List to the specified controller'