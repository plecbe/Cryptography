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
__module__  = "MyRot13.py"
__date__    = "2023-03-29"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to transform a string by rotating the letters 13 positions.
# The same algorithm is used for encoding and decoding since the alphabet includes 26 letters
# and shifting a letter 13 places twice moves it at its original place.
#

import argparse

# Constants
UPPER_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_ALPHA = "abcdefghijklmnopqrstuvwxyz"
# Change text
def Rot13(P_text):
    result = ""
    for c in P_text:
        if c in UPPER_ALPHA:
            result = result + chr(((ord(c) - ord("A") + 13) % 26) + ord("A"))
        elif c in LOWER_ALPHA:
            result = result + chr(((ord(c) - ord("a") + 13) % 26) + ord("a"))
        else:
            result = result + c
    return result

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to be encoded or decoded")
    args = parser.parse_args()
    p_filename = args.filename

    # Open the file
    with open(p_filename, 'r') as f:
        # Read first line
        line = f.readline()
        while line:
            print(Rot13(line), end = "")
            line = f.readline()
    exit(0)        

if __name__ == "__main__":
    main()

#EOF
