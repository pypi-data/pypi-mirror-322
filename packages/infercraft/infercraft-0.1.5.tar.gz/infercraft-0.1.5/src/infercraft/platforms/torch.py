import torch
from numpy import ndarray
import io


class TorchPlatform:
    def __init__(self, pt_bytes):
        pt_io = io.BytesIO(pt_bytes)
        model: torch.nn.Module = torch.jit.load(pt_io)
        self.model = model

    def infer(self, X: ndarray) -> ndarray:
        """
        Predict with batched input.

        Args:
            X: tensor in shape of (batch_size, in_dim1, in_dim2, ...)

        Returns:
            y, tensor in shape (batch_size, out_dim1, ...)
        """
        X = torch.from_numpy(X)

        model = self.model

        model.eval()
        with torch.no_grad():
            y = model(X)

        return y.cpu().numpy()
