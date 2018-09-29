from io import BufferedReader, TextIOWrapper, BytesIO

def make_fake_file(contents):
    return TextIOWrapper(BufferedReader(BytesIO(contents.encode())))