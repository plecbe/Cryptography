# Cryptography

Various cryptographic tools

- MyDecodeByFreq.py is an interactive tool to decode English messages encoded by substitution. It computes the frequencies of the letters in the ciphertext and replaces them by their equivalent from the classical frequency scheme. You can then tune the translation table.
- MyCaesar.py is an encode/decode tool using the Caesar cipher (substitution with character 3 ranks higher in the alphabet).
- MyXor.py is an encode/decode tool using the exclusive OR (XOR) binary operator between the input file and a byte from a secret key.
- MyVigenere.py is an encode/decode tool using the Vigenère algorithm (substitution with a character found in a matrix combining a character from the clear text and a character from a secret key).
- MyRot13 rotates alphabetics characters by 13 positions (doing it twice gives the original).
- MyB64 encodes/decodes to/from Base64.
- MySha1.py computes the SHA-1 hash of a file. Implemented following the English and French Wikipedia entries. 
- MySha256.py computes the SHA-256 (SHA-2, length=256, 64 rounds) hash of a file. Implemented following the Wikipedia entry.
- MyMd5.py computes the MD5 hash of a file.
- MyRC4.py encodes/decodes text or hex values with the RC4 symetrical, variable key length stream encryption algorithm.
