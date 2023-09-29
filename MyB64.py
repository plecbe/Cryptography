"""
----LICENSE----
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>

"""
__module__  = "MyB64.py"
__date__    = "2023-09-28"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to encode or decode a text to/from base64
# Encoding: 3 6-bits characters are concatenated to form a 24-bit string,
# which is divided into 4 6-bits numbers.
# These numbers are then replaced by their ASCII equivalent from the set
# [A-Za-z0-9+/] (64 values).
# The result is padded with '=' if the number of input characters is not a multiple of 3.
#

import argparse
import struct

alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

def b64encode(P_buffer):   
    # Divide buffer into 24 bits chunks
    # You have to keep them in the 'right' order: if the string is "ABC" = 
    # address:     00         01         02
    #              0x41       0x42       0x43
    # hex         |0100 00 01|0100 0 010|01 00 0011|
    # octal       |0100 00|01 0100|0 010 01|00 0011|
    #              o20     o24     o11      o03
    # The high order byte must be at the lowest address, so you have to parse the string in Big Endian order!
    P_output=""
    # Pad the input with null bytes
    padcount = len(P_buffer)%3
    while len(P_buffer)%3 != 0:
        P_buffer += bytes(1)
        
    for i in range(0, len(P_buffer), 3):
        x1 = int.from_bytes(P_buffer[i:i+3],"big") >> 18 & 0x00003F # Keep upper 6 bits
        x2 = int.from_bytes(P_buffer[i:i+3],"big") >> 12 & 0x00003F # Keep 2nd octal number
        x3 = int.from_bytes(P_buffer[i:i+3],"big") >> 6 & 0x00003F # Keep 3nd octal number
        x4 = int.from_bytes(P_buffer[i:i+3],"big") & 0x00003F # Keep last octal number
        # Check if input was padded
        if i == len(P_buffer) - 3:
            if padcount != 0:
                x4 = 64
            if padcount == 1:
                x3 = 64
        outstr = alpha[x1] + alpha[x2] + alpha[x3] + alpha[x4]
        P_output += outstr
    return(P_output)

def b64decode(P_buffer):
    # Divide string into 4 byte chunks.
    # Convert each byte to its 6 bit representation and concatenate them
    # Pad the input with '='
    P_outbuf = bytearray()
    while len(P_buffer)%4 != 0:
        P_buffer += "="
    for i in range(0,len(P_buffer), 4):
        value = 0    
        for j in range (4):
            if P_buffer[i+j] != "=":
                value += alpha.rfind(P_buffer[i+j]) * (64 ** (3-j))
                threebytes = struct.pack("BBB", (value >> 16) & 0x000000FF, (value >> 8) & 0x000000FF, value & 0x000000FF)
            else:
                # If we have a single padding "=", it means we have 2 valid bytes 
                # and we must discard the 2 rightmost bits of the 18 bits
                if j == 3:
                    threebytes = struct.pack("BB", (value >> 10) & 0x000000FF, (value >> 2) & 0x000000FF)
                    break
                else:
                    # Else we have 2 padding "=", we have only one single valid byte 
                    # and we must discard the 4 rightmost bits of the 12 bits
                    threebytes = struct.pack("B", (value >> 4) & 0x000000FF)
                    break
        P_outbuf.extend(threebytes)
    return(P_outbuf)    
        
# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="File to be encoded or decoded")
    parser.add_argument("-e", "--encode", help="Encode (Default)", action = "store_true")
    parser.add_argument("-d", "--decode", help="Decode", action = "store_true")
    opts, rem_args = parser.parse_known_args()
    if opts.decode:
        parser.add_argument("-o", "--output", required = True, help="Decoded output file", action = "store")   
    args = parser.parse_args()
    p_input = args.input
    p_encode = args.encode
    p_decode = args.decode
        
    #Default is to encode
    if not p_decode:       
        # Open the file
        with open(p_input, 'rb') as fi:
            buffer = fi.read()
            # Encode it
            output = b64encode(buffer)
        fi.close()
        print (output)
    else:
        p_output = args.output
        # Open the input file
        with open(p_input, 'r') as fi:
            # Open the output file
            with open(p_output, 'wb') as fo:
                text = ""
                strippedtext = ""
                # Read the file and strip \nl
                for line in fi:
                    strippedtext += line.strip()
                # Decode it
                output = b64decode(strippedtext)
                # Write the output
                fo.write(output)
        fo.close()
        fi.close()
    exit(0)
    
if __name__ == "__main__":
    main()

#EOF
