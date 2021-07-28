import cryptocode


def encrypt_me(word, api_key):
    return cryptocode.encrypt(word, api_key)


def decrypt_me(word, api_key):
    return cryptocode.decrypt(word, api_key)
