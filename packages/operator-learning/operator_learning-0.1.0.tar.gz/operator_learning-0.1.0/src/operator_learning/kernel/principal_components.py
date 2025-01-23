import logging
from math import sqrt
from typing import Literal

import numpy as np

from scipy.linalg import eigh, lstsq
from scipy.sparse.linalg import eigsh

from operator_learning.linalg import add_diagonal_, stable_topk
from operator_learning.structs import FitResult

logger = logging.getLogger("operator_learning")

def fit(
    kernel_X: np.ndarray,
    tikhonov_reg: float = 0.0,  
    rank: int | None = None, 
    svd_solver: Literal[
        "arnoldi", "full"
    ] = "arnoldi",  
) -> FitResult:
    """Fits the principal components estimator

    Args:
        kernel_X (np.ndarray): Kernel matrix of the input data.
        tikhonov_reg (float, optional): Tikhonov (ridge) regularization parameter. Defaults to 0.0.
        rank (int | None, optional): Rank of the estimator. Defaults to None.
        svd_solver (Literal[ &quot;arnoldi&quot;, &quot;full&quot; ], optional): Solver for the generalized eigenvalue problem. Defaults to "arnoldi".

    """
    npts = kernel_X.shape[0]
    add_diagonal_(kernel_X, npts * tikhonov_reg)
    if svd_solver == "arnoldi":
        _num_arnoldi_eigs = min(rank + 5, kernel_X.shape[0])
        values, vectors = eigsh(kernel_X, k=_num_arnoldi_eigs)
    elif svd_solver == "full":
        values, vectors = eigh(kernel_X)
    else:
        raise ValueError(f"Unknown svd_solver {svd_solver}")
    add_diagonal_(kernel_X, -npts * tikhonov_reg)

    values, stable_values_idxs = stable_topk(values, rank, ignore_warnings=False)
    vectors = vectors[:, stable_values_idxs]
    Q = sqrt(npts) * vectors / np.sqrt(values)
    kernel_X_eigvalsh = np.sqrt(np.abs(values)) / npts
    result: FitResult = {"U": Q, "V": Q, "svals": kernel_X_eigvalsh}
    return result


def fit_nystroem(
    kernel_X: np.ndarray,  # Kernel matrix of the input inducing points
    kernel_Y: np.ndarray,  # Kernel matrix of the output inducing points
    kernel_Xnys: np.ndarray,  # Kernel matrix between the input data and the input inducing points
    kernel_Ynys: np.ndarray,  # Kernel matrix between the output data and the output inducing points
    tikhonov_reg: float = 0.0,  # Tikhonov (ridge) regularization parameter (can be 0)
    rank: int | None = None,  # Rank of the estimator
    svd_solver: Literal["arnoldi", "full"] = "arnoldi",
) -> FitResult:
    """Fits the principal components estimator using the Nyström method

    Args:
        kernel_X (np.ndarray): Kernel matrix of the input inducing points.
        kernel_Y (np.ndarray): Kernel matrix of the output inducing points.
        kernel_Xnys (np.ndarray): Kernel matrix between the input data and the input inducing points.
        kernel_Ynys (np.ndarray): Kernel matrix between the output data and the output inducing points.
        tikhonov_reg (float, optional): Tikhonov (ridge) regularization parameter. Defaults to 0.0.
        rank (int | None, optional): Rank of the estimator. Defaults to None.
        svd_solver (Literal[ "arnoldi", "full" ], optional): Solver for the generalized eigenvalue problem. Defaults to "arnoldi".
    """
    ncenters = kernel_X.shape[0]
    npts = kernel_Xnys.shape[0]
    eps = 1000 * np.finfo(kernel_X.dtype).eps
    reg = max(eps, tikhonov_reg)
    kernel_Xnys_sq = kernel_Xnys.T @ kernel_Xnys
    add_diagonal_(kernel_X, reg * ncenters)
    if svd_solver == "full":
        values, vectors = eigh(
            kernel_Xnys_sq, kernel_X
        )  # normalization leads to needing to invert evals
    elif svd_solver == "arnoldi":
        _oversampling = max(10, 4 * int(np.sqrt(rank)))
        _num_arnoldi_eigs = min(rank + _oversampling, ncenters)
        values, vectors = eigsh(
            kernel_Xnys_sq,
            M=kernel_X,
            k=_num_arnoldi_eigs,
            which="LM",
        )
    else:
        raise ValueError(f"Unknown svd_solver {svd_solver}")
    add_diagonal_(kernel_X, -reg * ncenters)

    values, stable_values_idxs = stable_topk(values, rank, ignore_warnings=False)
    vectors = vectors[:, stable_values_idxs]

    U = sqrt(ncenters) * vectors / np.sqrt(values)
    V = np.linalg.multi_dot([kernel_Ynys.T, kernel_Xnys, vectors])
    V = lstsq(kernel_Y, V)[0]
    V = sqrt(ncenters) * V / np.sqrt(values)

    kernel_X_eigvalsh = np.sqrt(np.abs(values)) / npts
    result: FitResult = {"U": U, "V": V, "svals": kernel_X_eigvalsh}
    return result
