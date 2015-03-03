def parse_index(file_stream):
    lines = [l.replace("\n", "") for l in file_stream.readlines()]
    index = []
    try:
        for l in lines:
            components = l.split(",")
            rdi = IndexEntry(
                components[0],
                components[1],
                components[2],
                int(components[3]))
            index.append(rdi)

    except Exception:
        raise ValueError("Bad index file")

    return index


class IndexEntry(object):
    def __init__(self, res_file_name, relative_url, md5_checksum, size_in_bytes):
        self.filename = res_file_name
        self.cached_name = relative_url
        self.md5_checksum = md5_checksum
        self.size_in_bytes = size_in_bytes