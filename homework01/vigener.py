def encrypt_vigenere(plaintext, keyword):
    """
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ''
    l = len(keyword)
    for i, ch in enumerate(plaintext):
        if ('A' <= ch <= 'Z') or ('a' <= ch <= 'z'):
            s = ord(keyword[i % l])
            if ('A' <= ch <= 'Z'):
                s-=ord('A')
            else:
                s-=ord('a')
            move = ord(ch) + s

            if('A' <= ch <= 'Z') and move > ord('Z'): move-=26
            elif ('a' <= ch <= 'z') and move > ord('z'): move-=26
            ciphertext += chr(move)
    return ciphertext


def decrypt_vigenere(ciphertext, keyword):
    """
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ''
    l = len(keyword)
    for i, ch in enumerate(ciphertext):
        if ('A' <= ch <= 'Z') or ('a' <= ch <= 'z'):
            s = ord(keyword[i % l])
            if ('A' <= ch <= 'Z'):
                s-=ord('A')
            else:
                s-=ord('a')
            move = ord(ch) - s

            if('A' <= ch <= 'Z') and move < ord('A'): move+=26
            elif ('a' <= ch <= 'z') and move < ord('a'): move+=26
            plaintext += chr(move)
    return plaintext