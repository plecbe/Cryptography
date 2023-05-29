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
__module__  = "MyDecodeByFreq.py"
__date__    = "2023-03-25"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to decode an English file encoded by substitution
# It computes the frequency of the letters and substitutes the original letters
# by the one in the same rank of frequency based on the order: 
# ETAOINSRHDLUCMFYWGPBVKXQJZ
#

import argparse

# Main program
def main():
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # Classical frequency order in English
    REF_LIST = "ETAOINSRHDLUCMFYWGPBVKXQJZ"
    # Parse filename   
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="file to be decoded")
    args = parser.parse_args()
    filename = args.filename
    print ("Filename: ",filename)
    
    # Open the file
    with open(filename, 'r') as f:
        # Initialize counters
        nblines = 0
        nbchar = 0
        freq = {}
        for i in range(65,65+26):
            freq[chr(i)] = 0
        # Read first line
        line = f.readline()
        while line:
            # Count lines and characters
            nblines += 1
            for c in line:
                if c.isalpha():
                    nbchar += 1
                    freq[c.upper()] += 1
            line = f.readline()    
        print("Number of lines: " + str(nblines))
        print("Number of letters: " + str(nbchar))
        print("Char - Count   - Frequency - Original")
        sorted_list = sorted(freq.items(), key = lambda x:x[1], reverse = True)
        i = 0
        for char, count in sorted_list:
            print("{0:<4} - {1:8d} - {2:8f} - {3}".format(char, count, count/nbchar, REF_LIST[i]))
            i += 1
    f.close()
    # Build original dictionary in decreasing frequency
    origdict = ""
    for char, count in sorted_list:
        origdict += char
    # Print translation table
    print ("Original alphabet: " + origdict)
    print ("Translated to    : " + REF_LIST)
    ans = "a"
    ans1 = "y"
    loop = True
    first = True
    while loop:
        loop = False
        while not ans in "ynYN":
            # Prompt for modification
            ans = input("Do you want to make modifications (y/n)?")
            if ans in "yY":
                ch1 = "*"
                while not ch1 in ALPHABET:
                    ch1 = input("Char in encoded text: ").upper()
                ch2 = "*"
                while not ch2 in ALPHABET:
                    ch2 = input("To be replaced by: ").upper()
                index1 = origdict.find(ch1)
                temp = REF_LIST[index1]
                REF_LIST = REF_LIST.replace(ch2,"*")
                REF_LIST = REF_LIST.replace(temp,ch2)
                REF_LIST = REF_LIST.replace("*",temp)
                print("New substitution map:")
                print(origdict)
                print(REF_LIST)
                ans = "a"
                loop = True
        if loop or first:
            loop = True
            first = False
            # Perform substitution
            with open(filename, 'r') as f:
                line = f.readline().upper()
                while line:
                    translatetable = line.maketrans(origdict, REF_LIST)    
                    print (line.translate(translatetable))
                    line = f.readline().upper()
            f.close()
            ans = "a"           
    exit(0)        

if __name__ == "__main__":
    main()

#EOF
