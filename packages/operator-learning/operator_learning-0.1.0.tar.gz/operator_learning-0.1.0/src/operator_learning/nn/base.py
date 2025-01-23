from operator_learning.structs import EigResult, FitResult
import torch
import scipy.linalg
import numpy as np
from typing import Literal


def fit_ridgels(
    cov_X: torch.Tensor,
    tikhonov_reg: float = 0.0,
) -> FitResult:
    """Fit the ridge least squares estimator for the transfer operator.

    Args:
        cov_X (torch.Tensor): covariance matrix of the input data.
        tikhonov_reg (float, optional): Ridge regularization. Defaults to 0.0.

    Returns:
        FitResult: as defined in operator_learning.structs
    """
    dim = cov_X.shape[0]
    reg_input_covariance = cov_X + tikhonov_reg * torch.eye(
        dim, dtype=cov_X.dtype, device=cov_X.device
    )
    values, vectors = torch.linalg.eigh(reg_input_covariance)
    # Divide columns of vectors by square root of eigenvalues
    rsqrt_evals = 1.0 / torch.sqrt(values + 1e-10)
    Q = vectors @ torch.diag(rsqrt_evals)
    result: FitResult = FitResult({"U": Q, "V": Q, "svals": values})
    return result


def eig(
    fit_result: FitResult,
    cov_XY: torch.Tensor,
) -> EigResult:
    """Computes the eigendecomposition of the transfer operator.

    Args:
        fit_result (FitResult): Fit result from the fit_ridgels function.
        cov_XY (torch.Tensor): Cross covariance matrix between the input and output data.

    Returns:
        EigResult: as defined in ``operator_learning.structs``
    """
    U = fit_result["U"]
    # Using the trick described in https://arxiv.org/abs/1905.11490
    M = torch.linalg.multi_dot([U.T, cov_XY, U])
    # Convertion to numpy
    M = M.numpy(force=True)
    values, lv, rv = scipy.linalg.eig(M, left=True, right=True)
    r_perm = torch.tensor(np.argsort(values), device=cov_XY.device)
    l_perm = torch.tensor(np.argsort(values.conj()), device=cov_XY.device)
    values = values[r_perm]
    # Back to torch
    values = torch.tensor(values, device=cov_XY.device)
    lv = torch.tensor(lv, device=cov_XY.device)
    rv = torch.tensor(rv, device=cov_XY.device)

    # Normalization in RKHS norm
    rv = U.cfloat() @ rv
    rv = rv[:, r_perm]
    rv = rv / torch.linalg.norm(rv, axis=0)
    # # Biorthogonalization
    lv = torch.linalg.multi_dot([cov_XY.T.cfloat(), U.cfloat(), lv])
    lv = lv[:, l_perm]
    l_norm = torch.sum(lv * rv, axis=0)
    lv = lv / l_norm
    result: EigResult = EigResult({"values": values, "left": lv, "right": rv})
    return result


def evaluate_eigenfunction(
    X: torch.Tensor,
    eig_result: EigResult,
    which: Literal["left", "right"] = "right",
):
    
    vr_or_vl = eig_result[which]
    return X.to(vr_or_vl.dtype) @ vr_or_vl
