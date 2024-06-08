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
__module__  = "MySha256.py"
__date__    = "2023-11-05"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to compute the SHA-256 hash
#

import struct
import argparse


# SHA-256 padding function
# Ensure blocks are 512 bits long by adding one single bit set ('1'),then zeroes, then the original length
def pad(P_buffer):
    length = len(P_buffer) * 8                      # Buffer length in bits
    P_buffer += b'\x80'                             # Pad with a single '1' bit
    P_buffer += b'\x00' * (56 - len(P_buffer) % 64) # Pad with zeroes
    # Append the buffer length in bits as a 64-bit big-endian integer
    P_buffer += struct.pack('>Q', length)                
    return P_buffer

def ror(P_word, P_n):
    # Shift 32 bit right by P_n positions, and OR it with the word left shifted by 32-P_n positions
    return ((P_word >> P_n) | (P_word << (32 - P_n))) & 0xFFFFFFFF


def sha256(P_buffer):
    # Define SHA-256 constants
    K = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
    ]

    # Initial hash values
    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    # Pad the input to a multiple of 512 bits
    P_buffer = pad(P_buffer)
 
    # Work on chunks of 512 bits (64 bytes)
    for i in range(0, len(P_buffer), 64):
        # Initialize the intermediate 64 32 bit word buffer
        w = [0] * 64
        # Slice the 512 bit block into 16 32 bit words
        # The first 16 words are copied from the input buffer
        for j in range(16):
            w[j] = struct.unpack('>I', P_buffer[i + j * 4:i + j * 4 + 4])[0]
        # The remaining words are rotations of XORed words in selected preceding positions        
        for j in range(16, 64):
            s0 = ror(w[j-15], 7) ^ ror(w[j-15], 18) ^ (w[j-15] >> 3)
            s1 = ror(w[j-2], 17) ^ ror(w[j-2], 19) ^ (w[j-2] >> 10)
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xFFFFFFFF
        # Initialize the output 256 bit vector
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        # Compute the compression function
        for j in range(64):
            S1 = ror(e, 6) ^ ror(e, 11) ^ ror(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = h + S1 + ch + K[j] + w[j]
            S0 = ror(a, 2) ^ ror(a, 13) ^ ror(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = S0 + maj

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF
        # Output vector = output vector from previous block + new computed values 
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    # Concatenate the 8 32 bit hash values
    hash256 = struct.pack('>8I', h0, h1, h2, h3, h4, h5, h6, h7)
    # Return the hexadecimal value
    return hash256.hex()

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File for which SHA-256 will be computed")
    args = parser.parse_args()
    p_filename = args.filename
    with open(p_filename, 'rb') as f:
        content = f.read()   
        print(sha256(content))
    exit(0)

if __name__ == "__main__":
    main()

#EOF
