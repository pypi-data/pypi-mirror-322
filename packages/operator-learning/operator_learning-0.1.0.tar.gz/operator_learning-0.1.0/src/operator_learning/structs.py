from typing import TypedDict, Union
import numpy as np

from torch import Tensor


class FitResult(TypedDict):
    U: Union[np.ndarray, Tensor]
    V: Union[np.ndarray, Tensor]
    svals: Union[np.ndarray, Tensor] | None


class EigResult(TypedDict):
    values: Union[np.ndarray, Tensor]
    left: Union[np.ndarray, Tensor] | None
    right: Union[np.ndarray, Tensor]
