from os import path

from platforms.torch import TorchPlatform
from platforms.onnx import OnnxPlatform


p_mapping = {
    "torch_script": TorchPlatform,
    "onnx": OnnxPlatform
}

ext_mapping = {
    ".pt": "torch_script",
    ".onnx": "onnx"
}


def by_id(id):
    return p_mapping[id]


def to_id(filename):
    _, ext = path.splitext(filename)
    p = ext_mapping[ext]
    if p is None:
        raise ValueError(
            f"don't know how to run this file, please explicitly specify the platform")
    return p


def accept(filename):
    _, ext = path.splitext(filename)
    return ext in ext_mapping
