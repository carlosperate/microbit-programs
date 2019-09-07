"""
This script is used to write a file in a specific flash location.
It overwrites the file continuously until it falls on the right place.
Assumes the given address to check for is the 1st byte of a file chunk.
"""
import machine
import os
from microbit import *

# Configure Me ---------------------------------------------------------
file_start_address = 0x38c00
file_name = 'two_chunks.py'
file_content = 'a = """abcdefghijklmnopqrstuvwxyz\n' + \
      'abcdefghijklmnopqrstuvwxyz\n' + \
      'abcdefghijklmnopqrstuvwxyz\n' + \
      'abcdefghijklmnopqrst"""\n'


# Code starts ----------------------------------------------------------
chunk_marker = machine.mem8[file_start_address]
count = 1
while chunk_marker != 0xfe:
    # Write the file we want
    with open(file_name, 'w') as f:
        f.write(file_content)
    # Write and remove a small file, used to offset the next round around the
    # filesystem space by one chunk (so we don't loop on the same spots)
    #with open('small_file_to_delete.py', 'w') as f:
    #    f.write('hello')
    #os.remove('small_file_to_delete.py')
    chunk_marker = machine.mem8[file_start_address]
    count += 1
    print('{}: {}'.format(count, chunk_marker))
print(chunk_marker)
display.show(Image.HAPPY)