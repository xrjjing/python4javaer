"""最小化 MinIO 内存 mock。"""

from typing import Dict, Tuple


class InMemoryObjectStore:
    def __init__(self):
        self._store: Dict[Tuple[str, str], bytes] = {}

    def put_object(self, bucket: str, object_name: str, data: bytes) -> None:
        self._store[(bucket, object_name)] = data

    def get_object(self, bucket: str, object_name: str) -> bytes:
        key = (bucket, object_name)
        if key not in self._store:
            raise FileNotFoundError(f"{bucket}/{object_name} 不存在")
        return self._store[key]

    def list_objects(self, bucket: str):
        for (b, name), data in self._store.items():
            if b == bucket:
                yield {"object_name": name, "size": len(data)}


def get_fake_minio():
    """返回一个内存对象存储实例，接口与常用 MinIO client 近似。"""
    return InMemoryObjectStore()
