from dataclasses import dataclass
from os import path
import os
from platform_factory import accept, to_id


@dataclass
class model_desc:
    path: str
    platform_id: str


def dir_to_desc_map(dir):
    files = os.listdir(dir)

    def is_ok(filename):
        is_file = path.isfile(
            path.join(dir, filename)
        )
        is_model = accept(filename)
        return is_file and is_model

    model_files = list(filter(is_ok, files))

    desc_map = {}
    for f in model_files:
        desc = model_desc(
            path.join(dir, f), to_id(f)
        )
        desc_map[f] = desc
    return desc_map
