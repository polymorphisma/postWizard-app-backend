import uuid


def generate_uuid():
    return str(uuid.uuid4())


def extract_extension(filename):
    value = filename.split('.')
    return value[-1]
