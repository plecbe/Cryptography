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
__module__  = "MyVigenere.py"
__date__    = "2023-03-26"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to encode or decode a text with the Vigénère cipher
# The Vigénère cipher combines a letter of the clear text with a letter from the secret key,
# and replaces it with the character found at the intersection of the row given by the clear text 
# and the column given by the key in the following table:
#   |ABCDEFGHIJKLMNOPQRSTUVWXYZ
#   +--------------------------
#  A|ABCDEFGHIJKLMNOPQRSTUVWXYZ
#  B|BCDEFGHIJKLMNOPQRSTUVWXYZA
#  C|CDEFGHIJKLMNOPQRSTUVWXYZAB
#    .....

import argparse

# Constants
UPPER_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
# Global variables
vig_table = []

# Encode text
def VigenereEncode(P_text, P_key):
    result = ""
    for i in range(len(P_text)):
        print("i: {0} char: {1} key: {2}".format(i, P_text[i],P_key[i % len(P_key)] ))
        result += vig_table[ord(P_text[i]) - ord("A")][ord(P_key[i % len(P_key)]) - ord("A")]
    return result

# Decode text
def VigenereDecode(P_text, P_key):
    result = ""
    for i in range(len(P_text)):
        row = vig_table[ord(P_key[i % len(P_key)]) - ord("A")]
        for j in range(len(row)):
            if row[j] == P_text[i]:
                result += chr(j + ord("A"))
                break
    return result

# Main program
def main():
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="File to be encoded or decoded")
    parser.add_argument("-d", "--decode", help="Decode (default)", action = "store_true")
    parser.add_argument("-e", "--encode", help="Encode", action = "store_true")
    args = parser.parse_args()
    p_filename = args.filename
    p_decode = args.decode
    p_encode = args.encode

    # Build the Vigenere table 
    row = UPPER_ALPHABET
    for i in range(len(UPPER_ALPHABET)):
        vig_table.append([])
        for j in range(len(UPPER_ALPHABET)):
            vig_table[i].append(row[j])
        row = row[1:len(UPPER_ALPHABET)] + row[0]
    # Ask for key
    key = input("Enter secret key: ")
    
    # Default action is to decode the file
    if p_encode:
        p_decode = False
        print ("Encoding " + p_filename)
    else:
        p_decode = True
        print ("Decoding " + p_filename)    

    # Open the file
    with open(p_filename, 'r') as f:
        text = f.read()
        # Strip text from non letters
        text1=""
        for i in range(len(text)):
            if text[i].isalpha():
                if text[i].lower() in ["é", "è", "ê"]:
                    text1 += "E"
                elif text[i].lower() in ["à", "â"]:
                    text1 += "A"
                elif text[i].lower() in ["î"]:
                    text1 += "I"
                elif text[i].lower() in ["ô"]:
                    text1 += "O"
                elif text[i].lower() in ["ù"]:
                    text1 += "U"
                else:    
                    text1 += text[i].upper()
        # Encode or decode
        if p_decode:
            print(VigenereDecode(text1, key))
        else:
            print(VigenereEncode(text1, key))
            
    exit(0)
if __name__ == "__main__":
    main()

#EOF
