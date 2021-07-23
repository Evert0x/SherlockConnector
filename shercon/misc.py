import sha3

def identifier(protocol):
    k = sha3.keccak_256()
    k.update(protocol.encode())
    return k.hexdigest()