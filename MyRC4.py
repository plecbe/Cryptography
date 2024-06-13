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
__module__  = "MyRC4.py"
__date__    = "2024-06-13"
__version__ = "X0.0"
__author__  = "P.Leclercq"

#
# Module to encrypt or decrypt a text with the RC4 stream algorithm
#

def RC4(P_key, P_text, P_op):
    # Transform ASCII key in numerical values
    keylength = len(P_key)
    key = [0] * keylength
    for i in range(0, keylength):
        key[i] = ord(P_key[i])
    # Initialize the lookup vector
    S = [0] * 256
    for i in range(0, 256):
        S[i] = i
    # Key Scheduling Algorithm (KSA)
    j = 0
    for i in range(0, 256):
        j = (j + S[i] + key[i % keylength]) % 256
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
    # Pseudo-random generator (PRGA)
    K = [0] * len(P_text)
    P_ciphertext = ""
    i = 0
    j = 0
    for count in range(0, len(P_text)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        t = (S[i] + S[j]) % 256
        K[count] = S[t]
        c = ord(P_text[count]) ^ K[count]
        if P_op == "E":
            P_ciphertext = P_ciphertext + format(c,"02x")
        else:
            P_ciphertext = P_ciphertext + chr(c)
    return P_ciphertext

# Main program
def main():
    key = input("RC4 - Enter key: ")
    text = input("RC4 - Enter text - ASCII to encrypt, hex to decrypt: ")
    op = "A"
    while (op != "D") and (op != "E"):
        op = input("RC4 - (E)ncrypt or (D)ecrypt: ")
    if op == "E":
        ciphertext = RC4(key, text, "E")
        print (ciphertext)
    else:
        # Transform hex string into chars
        ciphertext = ""
        for i in range(0, len(text), 2):
            ciphertext = ciphertext + chr(int(text[i:i+2], 16))
        plaintext = RC4(key, ciphertext, "D")
        print (plaintext)
    exit(0)

if __name__ == "__main__":
    main()

#EOF
    

        
