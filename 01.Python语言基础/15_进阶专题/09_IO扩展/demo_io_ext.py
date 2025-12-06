"""IO 扩展示例：StringIO/BytesIO、struct、gzip、zipfile"""

from __future__ import annotations

import gzip
import io
import struct
import zipfile
from io import BytesIO, StringIO


def demo_stringio_bytesio() -> None:
    text_buf = StringIO()
    text_buf.write("hello\n")
    text_buf.write("world")
    print("StringIO:", text_buf.getvalue())

    byte_buf = BytesIO()
    byte_buf.write(b"hello")
    print("BytesIO:", byte_buf.getvalue())


def demo_struct() -> None:
    data = struct.pack('<Ihf', 0x12345678, -1, 3.14)
    uid, flag, score = struct.unpack('<Ihf', data)
    print("struct packed:", data)
    print("unpacked:", uid, flag, score)


def demo_gzip_zipfile() -> None:
    text = b"hello gzip" * 10
    compressed = gzip.compress(text)
    print("gzip len ->", len(text), "->", len(compressed))
    print("gzip decompress ok:", gzip.decompress(compressed)[:10])

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('hello.txt', '你好，zip!')

    buf.seek(0)
    with zipfile.ZipFile(buf, 'r') as zf:
        print("zip names:", zf.namelist())
        print("zip content:", zf.read('hello.txt').decode())


def main():
    demo_stringio_bytesio()
    demo_struct()
    demo_gzip_zipfile()


if __name__ == "__main__":
    main()
