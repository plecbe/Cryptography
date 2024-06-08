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
__module__  = "MyMd5.py"
__date__    = "2024-05-20"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to compute the MD5 hash
#

import struct
import argparse
import math

# Rotate left function
def rol(P_word, P_n):
    # Shift 32-bit word left by P_n positions, and OR it with the word rotated right by 32-P_n positions 
    return (P_word << P_n) & 0xFFFFFFFF | (P_word >> (32 - P_n))


# MD5 padding function
# Ensure blocks are 512 bits long by adding one single bit set ('1'),then zeroes, then the original length as a little endian (contrarily to the SHAxx algorithms which use a big-endian length)
def md5_pad(P_buffer):
    length = len(P_buffer) * 8                      # Buffer length in bits
    P_buffer += b'\x80'                             # Pad with a single '1' bit
    P_buffer += b'\x00' * (56 - len(P_buffer) % 64) # Pad with zeroes
    # Append the buffer length in bits as a 64-bit little-endian integer
    P_buffer += struct.pack('<Q', length)                
    return P_buffer


def md5(P_buffer):
    # MD5 constants
    # s : per round shift amount
    s = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4
    # K : added to one of the hashed values
    # K[i] = floor(2^32 x abs(sin(i+1)) (32 bits, little endian)
    K = [0] * 64
    for i in range(64):
        K[i] = math.trunc(2 ** 32 * abs(math.sin(i+1))) & 0xFFFFFFFF

    # MD5 initial hash values
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476
    
    # Pad the input to a multiple of 512 bits
    P_buffer = md5_pad(P_buffer)
    
    # Work on chunks of 512 bits (64 bytes)
    for offset in range(0, len(P_buffer), 64):
        # Slice the 512 bit block into 16 32 bit words
        M = [0] * 16
        for j in range (16):
            M[j] = struct.unpack('<I', P_buffer[offset + j * 4:offset + j * 4 + 4])[0]
        #Initialize the hash values for this chunk    
        A, B, C, D = a0, b0, c0, d0
        for i in range(64):
            if 0 <= i <= 15:
                F = (B & C) | (~B & D)
                g = i
            elif 16 <= i <= 31:
                F = (D & B) | (~D & C)
                g = (5*i + 1) % 16
            elif 32 <= i <= 47:
                F = B ^ C ^ D
                g = (3*i + 5) % 16
            elif 48 <= i <= 63:
                F = C ^ (B | ~D)
                g = (7*i) % 16

            F = (F + A + K[i] + M[g]) & 0xFFFFFFFF
            A = D
            D = C
            C = B
            B = (B + rol(F, s[i])) & 0xFFFFFFFF
        # Add results from this block to the previous ones
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF

    # Produce the final hash value (little-endian) as a 128-bit number
    md5hash = struct.pack('<4I', a0, b0, c0, d0)
    # Return in hexadecimal format
    return md5hash.hex()

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File for which MD5 will be computed")
    args = parser.parse_args()
    p_filename = args.filename
    with open(p_filename, 'rb') as f:
        content = f.read()   
        print(md5(content))
    exit(0)

if __name__ == "__main__":
    main()

#EOF
