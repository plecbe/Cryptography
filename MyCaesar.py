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
__module__  = "MyCaesar.py"
__date__    = "2023-03-26"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to encode or decode a text with the Caesar cipher
# The Caesar cipher substitutes a letter with the one placed some positions higher,
# the difference being decided by the user.
# Decoding the ciphertext is the same as encoding with a negative shift.
#

import argparse

# Some constants
UPPER_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWER_ALPHA = "abcdefghijklmnopqrstuvwxyz"

# Encode text line
def CaesarEncode(P_text, P_shift):
    result = ""
    for char in P_text:
        if char in UPPER_ALPHA:
            result = result + chr(((ord(char) - ord("A") + P_shift) % 26) + ord("A"))
        elif char in LOWER_ALPHA:
            result = result + chr(((ord(char) - ord("a") + P_shift) % 26) + ord("a"))
        else:
            result = result + char
    return result

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to be encoded or decoded")
    args = parser.parse_args()
    p_filename = args.filename
    # Ask for the number of positions to shift the letter
    shift = int(input("Shift: "))
    # Open the file
    with open(p_filename, 'r') as f:
        line = f.readline()
        while line:
            # Encode the line
            print(CaesarEncode(line, shift), end = "")
            line = f.readline()
    exit(0)        

if __name__ == "__main__":
    main()

#EOF
