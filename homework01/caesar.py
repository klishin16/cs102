def encrypt_caesar(plaintext):
    """
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    ciphertext = ''
    for char in plaintext:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
            code = ord(char) + 3
            if code > ord('Z') or code > ord('z'):
                code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext):
    """
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    # PUT YOUR CODE HERE
    return plaintext