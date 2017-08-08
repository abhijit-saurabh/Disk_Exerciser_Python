import os
import platform
import sys
import binascii
import subprocess
import re


class readwritecompare(object):
    def __init__(self, device):
        self.device = device
        self.pattern_used = '0xff'
#########################################################################################################################################


        ######################### write_lba #########################
        # Inputs: startingLBA - starting LBA address in hex (0x100)
        #         num_blocks_to_write - number of blocks to write (in dec)
        #         blockSize - block size in multiple of 512 bytes (in dec)
        #         pattern - pattern in hex (0xff or 0xee  .. etc)
        # Outputs: void
    def write_lba(self,startingLBA,num_blocks_to_write,blockSize,pattern):

        startingLBAOffset = int(startingLBA, 16)
        startingByteOffset = startingLBAOffset * 512
        blockSize_local = int(blockSize)*512
        blocksToWrite = int(num_blocks_to_write)
        self.pattern_used = pattern

        pattern_local = int(pattern, 16)
        dataBuffer = bytearray(blockSize_local)
        for i in range(0, len(dataBuffer)):
            dataBuffer[i] = pattern_local


        try:
            fd = os.open(self.device, os.O_RDWR)
        except OSError:
            print 'Unable to open a drive handle for: ' + device
            sys.exit(-1)

        byteOffset = startingByteOffset
        while blocksToWrite > 0:
            try:
                # print 'Seeking to Byte Offset: ' + str(byteOffset) + '...'
                os.lseek(fd, byteOffset, os.SEEK_SET)
            except OSError:
                os.close(fd)
                # print 'Error seeking to Byte Offset: ' + str(byteOffset) + '!'
                sys.exit(-1)

            try:
                # print 'Writing ' + str(blockSize) + 'Bs of data from ' + device + ' at Byte Offset: ' + str(byteOffset) \
                      # + '...'
                os.write(fd, dataBuffer)
            except OSError:
                os.close(fd)
                print 'Error writing ' + str(blockSize) + 'Bs of data from ' + device + ' at Byte Offset: ' + str(byteOffset) + '!'
                sys.exit(-1)

            blocksToWrite -= 1
            byteOffset += blockSize_local

        os.close(fd)
#############################################################################################################################################


        ######################### read_lba #########################
        # Inputs: startingLBA - starting LBA address in hex (0x100)
        #         num_blocks_to_read - number of blocks to write (in dec)
        #         blockSize - block size in multiple of 512 bytes (in dec)
        #
        # Outputs: returns read data as a string
    def read_lba(self, startingLBA, num_blocks_to_read, blockSize):

        startingLBAOffset = int(startingLBA, 16)
        startingByteOffset = startingLBAOffset * 512
        blockSize_local = int(blockSize) * 512
        blocksToRead = num_blocks_to_read

        try:
            #print 'Opening a drive handle for: ' + self.device + '...'
            fdr = os.open(self.device, os.O_RDONLY)
        except OSError:
            print 'Unable to open a drive handle for: ' + device

            sys.exit(-1)
        my_data = ''
        byteOffset = startingByteOffset
        while blocksToRead > 0:
            try:
                #print 'Seeking to Byte Offset: ' + str(byteOffset) + '...'
                os.lseek(fdr, byteOffset, os.SEEK_SET)
            except OSError:
                os.close(fdr)
                print 'Error seeking to Byte Offset: ' + str(byteOffset) + '!'
                sys.exit(-1)

            try:
               # print 'Reading ' + str(blockSize_local) + 'Bs of data from ' + self.device + ' at Byte Offset: ' + str(byteOffset) \
                #     + '...'
                dataRead = os.read(fdr, blockSize_local)
                my_data = binascii.hexlify(dataRead)
                self.compare_data(my_data,self.pattern_used,blocksToRead)

                blocksToRead -= 1
                byteOffset += blockSize_local
            except OSError:
                os.close(fdr)
                print 'Error reading ' + str(blockSize) + 'Bs of data from ' + device + ' at Byte Offset: ' \
                 + str(byteOffset) + '!'
                sys.exit(-1)


        os.close(fdr)
################################################################################################################################################

    ######################### compare_lba_data #########################
    # Inputs: data - data string to be compared
    #         pattern - pattern to be compared with (0xff or 0xee etc)
    # Outputs: exit once a miscompare is detected and report the corresponding LBA.
    def compare_data(self,data,pattern,blocks):
        pattern_verify = pattern.replace("0x", "")
        dr = iter(data)
        count=0
        for a in dr:

            pattern_temp = a + next(dr)

            if pattern_temp != pattern_verify:
                location = count/512
                location/=2
                print "miscompare occured at an offset of block ",blocks," in the buffer and  bad data is ",data
                exit(0)

            count += 1
###################################################################################################################################################

    def get_device_number(self,device):

        return device[9]

    def get_disk_size(self,device):
        cmd = device.replace('/dev/','')
        words = {}
        fd = open('/proc/partitions','r')
        my_data = fd.readlines()
        for a in my_data:
            if re.search(cmd,a):

                words = a.split()
                return words[2]