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
__module__  = "MyXor.py"
__date__    = "2023-07-06"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to encode or decode a text with a simple XOR with a secret key.
# Encoding and decoding are the same operation since if A XOR B = C then C XOR B = A
#

import argparse
import struct

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="File to be encoded or decoded")
    parser.add_argument("output", help="Output file")
    args = parser.parse_args()
    p_input = args.input
    p_output = args.output
   
    # Ask for key
    key = input("Enter secret key: ")
    
    # Open the files
    with open(p_input, 'rb') as fi:
        with open(p_output, 'wb') as fo:
            size = len(key)
            buffer = fi.read()
            for i in range(len(buffer)):
                cipher = buffer[i] ^ ord(key[i % size])
                fo.write(cipher.to_bytes(1,"little"))
    fi.close()
    fo.close()
    exit(0)
    
if __name__ == "__main__":
    main()

#EOF
