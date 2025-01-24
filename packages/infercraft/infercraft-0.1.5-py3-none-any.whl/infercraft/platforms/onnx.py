import onnxruntime as ort
from numpy import ndarray


class OnnxPlatform:
    def __init__(self, onnx_bytes):
        session: ort.InferenceSession = ort.InferenceSession(onnx_bytes)
        self.session = session

    def infer(self, X: ndarray) -> ndarray:
        """
        Predict with batched input.

        Args:
            X: tensor in shape of (batch_size, in_dim1, in_dim2, ...)

        Returns:
            y, tensor in shape (batch_size, out_dim1, ...)
        """
        s = self.session
        input_name = s.get_inputs()[0].name
        y = s.run(None, {input_name: X})[0]
        return y
