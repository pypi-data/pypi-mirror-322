import numpy as np
import asyncio
from ray import ObjectRef
from actor_engine import ActorEngine


class EngineProxy:
    """
    this class servers as a proxy for an actor engine. but for the
    purpose of reduce the remote syntax from ray
    """

    def __init__(self, actor_engine: ObjectRef):
        self.engine: ObjectRef[ActorEngine] = actor_engine

    def infer(self, X: np.ndarray) -> asyncio.Future:

        # ray object ref is compatible with asyncio future
        fut: asyncio.Future = self.engine.infer.remote(X)
        return fut
