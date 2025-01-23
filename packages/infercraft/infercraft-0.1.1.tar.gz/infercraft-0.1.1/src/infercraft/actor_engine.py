from ray import remote, get_runtime_context
from ray.runtime_context import RuntimeContext
from numpy import ndarray
from platform_factory import by_id


@remote
class ActorEngine:

    def __init__(self, model_source, platform_id):
        """
        Args:
            model_source: the file-like containing the serilized model.
            platform_id: a identifier to specify which platform to execute it
        """

        make_model = by_id(platform_id)
        self.platform = make_model(model_source)

    def infer(self, X: ndarray) -> ndarray:
        """
        Predict with batched input.

        Args:
            X: tensor in shape of (batch_size, in_dim1, in_dim2, ...)

        Returns:
            y, tensor in shape (batch_size, out_dim1, ...)
        """
        return self.platform.infer(X)
