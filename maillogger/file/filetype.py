_SIGNATURE_BYTES = 768


def is_gzip(filepath: str) -> bool:
    with open(filepath, mode='rb') as fd:
        signature = fd.read(_SIGNATURE_BYTES)

    return (len(signature) > 2 and
            signature[0] == 0x1F and
            signature[1] == 0x8B and
            signature[2] == 0x8)
