def encrypt_caesar(plaintext :str, shift :int) -> str:
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
    ciphertext = ''
    for char in plaintext:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
            code = ord(char) + shift
            if code > ord('Z') or code > ord('z'):
                code -= 26
            ciphertext += chr(code)
        else:
            ciphertext += char
    return ciphertext


def decrypt_caesar(ciphertext :str, shift :int) -> str:
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
    plaintext = ''
    for char in ciphertext:
        if (char >= 'a' and char <= 'z') or (char >= 'A' and char <= 'Z'):
            code = ord(char) - shift
            if code < ord('a') and code > ord('Z') or code < ord('A'):
                code += 26
            plaintext += chr(code)
        else:
            plaintext += char
    return plaintext