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
__module__  = "MySha1.py"
__date__    = "2023-07-29"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to compute the SHA-1 hash
#

import struct
import argparse

# Circular left shift function
def rol(P_word, P_n):
    # Shift 32 bit word left by n positions, and OR it with the word right shifted by 32-n positions
    return ((P_word << P_n) | (P_word >> (32 - P_n))) & 0xFFFFFFFF

# SHA-1 padding function
def pad(P_buffer):
    length = len(P_buffer) * 8                      # Buffer length in bits
    P_buffer += b'\x80'                             # Pad with a single '1' bit
    P_buffer += b'\x00' * (56 - len(P_buffer) % 64) # Pad with zeros
    # Append the buffer length in bits as a 64-bit big-endian integer
    P_buffer += struct.pack('>Q', length)                
    return P_buffer

# SHA-1 main function
def sha1(P_buffer):
    # Initial 160 bit vector 
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0

    # Pad the input to a multiple of 512 bits
    P_buffer = pad(P_buffer)

    # Work on chunks of 512 bits (64 bytes)
    for i in range(0, len(P_buffer), 64):
        # Initialize the intermediate 80 32 bit word buffer
        w = [0] * 80
        # Slice the 512 bit block into 16 32 bit words
        # The first 16 words are copied from the input buffer
        for j in range(16):
            w[j] = struct.unpack('>I', P_buffer[i + j * 4:i + j * 4 + 4])[0]
        # The remaining words are rotations by 1 bit of XORed words in selected preceding positions
        for j in range(16, 80):
            w[j] = rol(w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16], 1)
        # Initialize the 160 bit output vector
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        # Compute f(bcd) for 80 rounds
        for j in range(80):
            # For the 20 first rounds, the result of the choice function is (b and c) or (not b and d)
            if j < 20:
                f = (b & c) | ((~b) & d)
                k = 0x5A827999
            # For rounds 20 to 39, the result of the parity function is b xor c xor d    
            elif j < 40:
                f = b ^ c ^ d
                k = 0x6ED9EBA1
            # For rounds 40 to 59, the result of the majority function is    (b and c) or (b and d) or (c and d) 
            elif j < 60:
                f = (b & c) | (b & d) | (c & d)
                k = 0x8F1BBCDC
            # For rounds 60 to 79, the result of the parity function is b xor c xor d        
            else:
                f = b ^ c ^ d
                k = 0xCA62C1D6
            # Intermediate buffer values are: 
            #  rol(a,5) + f(b,c,d) + e + k + w[j]
            #  a
            #  rol(b,30)
            #  c
            #  d
            tempa = a
            tempb = b
            tempc = c
            tempd = d
            tempe = e
            a = rol(a, 5) + f + e + k + w[j] & 0xFFFFFFFF
            b = tempa
            c = rol(tempb, 30)
            d = tempc
            e = tempd                                
        # Output vector = output vector from previous block + new computed values    
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Concatenate the 5 32-bit hash values into a 160-bit hash
    hash = struct.pack('>IIIII', h0, h1, h2, h3, h4)
    # Return the hexadecimal value
    return hash.hex()

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File for which SHA-1 will be computed")
    args = parser.parse_args()
    p_filename = args.filename
    with open(p_filename, 'rb') as f:
        content = f.read()   
        print(sha1(content))
    exit(0)

if __name__ == "__main__":
    main()

#EOF
