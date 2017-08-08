import os
import platform
import sys
import binascii
import ctypes
import datetime
import time

from readwritecompare import readwritecompare

class workload(object):
    def __init__(self, drive_number):
        self.drive_number = drive_number


    def wl_type0(self,rwc,startLba,num_blocks,block_size,pattern):
        rwc.write_lba(startLba, num_blocks, block_size, pattern)

        rwc.read_lba(startLba, num_blocks, block_size)

        library = ctypes.cdll.LoadLibrary(os.getcwd() + '/LinuxNVMeIOCTL.so')

        startLba_local_trim = int(startLba, 16)
        numOfLogicalBlocks_local = num_blocks * block_size


        print "Starting trim .. "
        if (numOfLogicalBlocks_local > 100):
            trim_lba_local = startLba_local_trim
            trim_size_local = 100
            count = numOfLogicalBlocks_local / 100
            for i in range(0, count):
                ioctlReturnCode = library.dsm_deallocate(ctypes.c_int(self.drive_number), ctypes.c_int(trim_lba_local),
                                                         ctypes.c_int(trim_size_local))
                trim_lba_local = trim_lba_local + 80
            lba_left_local = numOfLogicalBlocks_local - count * 80

            ioctlReturnCode = library.dsm_deallocate(ctypes.c_int(self.drive_number), ctypes.c_int(trim_lba_local),
                                                     ctypes.c_int(lba_left_local))
        else:

            ioctlReturnCode = library.dsm_deallocate(ctypes.c_int(self.drive_number), ctypes.c_int(startLba_local_trim),
                                                     ctypes.c_int(numOfLogicalBlocks_local))

        time.sleep(2)
        rwc.pattern_used = '0x00'
        rwc.read_lba(startLba, num_blocks, block_size)
        exit(0)

    def wl_type1(self,rwc,startLba,num_blocks,block_size,pattern):
        try:

            while (1):

                rwc.write_lba(startLba, num_blocks, block_size, pattern)

                rwc.read_lba(startLba, num_blocks, block_size)

                library = ctypes.cdll.LoadLibrary(os.getcwd() + '/LinuxNVMeIOCTL.so')

                startLba_local_trim = int(startLba, 16)
                numOfLogicalBlocks_local = num_blocks * block_size

                if (numOfLogicalBlocks_local > 100):
                    trim_lba_local = startLba_local_trim
                    trim_size_local = 100
                    count = numOfLogicalBlocks_local / 100
                    for i in range(0, count):
                        ioctlReturnCode = library.dsm_deallocate(ctypes.c_int(self.drive_number), ctypes.c_int(trim_lba_local),
                                                                 ctypes.c_int(trim_size_local))
                        trim_lba_local = trim_lba_local + 80
                    lba_left_local = numOfLogicalBlocks_local - count * 80

                    ioctlReturnCode = library.dsm_deallocate(ctypes.c_int(self.drive_number), ctypes.c_int(trim_lba_local),
                                                             ctypes.c_int(lba_left_local))
                else:

                    ioctlReturnCode = library.dsm_deallocate(ctypes.c_int(self.drive_number), ctypes.c_int(startLba_local_trim),
                                                             ctypes.c_int(numOfLogicalBlocks_local))

                time.sleep(2)
                rwc.pattern_used = '0x00'
                rwc.read_lba(startLba, num_blocks, block_size)
        except (KeyboardInterrupt, SystemExit):
            print '\n \n program stopped manually'
            sys.exit(0)

    def wl_type2(self, rwc, startLba, num_blocks, block_size, pattern):
        try:
            for i in range(0,2):

                rwc.write_lba(startLba, num_blocks, block_size, pattern)
        except (KeyboardInterrupt, SystemExit):
            print '\n \n program stopped manually'
            sys.exit(0)