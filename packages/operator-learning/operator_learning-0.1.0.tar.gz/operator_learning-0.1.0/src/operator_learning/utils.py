from math import sqrt

import numpy as np

from scipy.spatial.distance import pdist
from typing import Union
import torch


def topk(vec: np.ndarray, k: int):
    assert np.ndim(vec) == 1, "'vec' must be a 1D array"
    assert k > 0, "k should be greater than 0"
    sort_perm = np.flip(np.argsort(vec))  # descending order
    indices = sort_perm[:k]
    values = vec[indices]
    return values, indices


def fuzzy_parse_complex(vec: np.ndarray, tol: float = 10.0):
    assert issubclass(
        vec.dtype.type, np.complexfloating
    ), "The input element should be complex"
    rcond = tol * np.finfo(vec.dtype).eps
    pdist_real_part = pdist(vec.real[:, None])
    # Set the same element whenever pdist is smaller than eps*tol
    condensed_idxs = np.argwhere(pdist_real_part < rcond)[:, 0]
    fuzzy_real = vec.real.copy()
    if condensed_idxs.shape[0] >= 1:
        for idx in condensed_idxs:
            i, j = row_col_from_condensed_index(vec.real.shape[0], idx)
            avg = 0.5 * (fuzzy_real[i] + fuzzy_real[j])
            fuzzy_real[i] = avg
            fuzzy_real[j] = avg
    fuzzy_imag = vec.imag.copy()
    fuzzy_imag[np.abs(fuzzy_imag) < rcond] = 0.0
    return fuzzy_real + 1j * fuzzy_imag


def row_col_from_condensed_index(d, index):
    # Credits to: https://stackoverflow.com/a/14839010
    b = 1 - (2 * d)
    i = (-b - sqrt(b**2 - 8 * index)) // 2
    j = index + i * (b + i + 2) // 2 + 1
    return (int(i), int(j))

def parse_complex_eigenvalues(eigenvalues: Union[torch.Tensor, np.ndarray]):
    """Returns a dictionary with the indices of the real eigenvalues and the indices of one element per each complex conjugate pair

    Args:
        eigenvalues (Union[torch.Tensor, np.ndarray]): 1-dimensional vector of complex eigenvalues

    Returns:
        dict: A dictionary with the indices of the real eigenvalues and the indices of one element per each complex conjugate pair
    """
    assert eigenvalues.dim == 1
    if torch.is_tensor(eigenvalues):
        vec = eigenvalues.numpy(force=True)
    else:
        vec = np.asarray(eigenvalues)
    idxs = np.arange(vec.shape[0], dtype=int)
    eps = np.finfo(vec.dtype).eps
    is_real = np.abs(vec.imag) < eps
    real_idxs = idxs[is_real]
    cplx_eigs = vec[np.logical_not(is_real)]
    cplx_conj_pairs_idxs = _parse_cplx_conj_pairs(cplx_eigs)
    cc_ixs = idxs[np.logical_not(is_real)][cplx_conj_pairs_idxs]
    if torch.is_tensor(eigenvalues):
        real_idxs = torch.tensor(real_idxs, device=eigenvalues.device)
        cc_idxs = torch.tensor(cc_idxs, device=eigenvalues.device)
    return {"real": real_idxs, "complex": cc_ixs}

def _parse_cplx_conj_pairs(cplx_conj_vec: np.ndarray):
    if not cplx_conj_vec.shape[0] % 2 == 0:
        raise ValueError(
            f"The array must consist in a set of complex conjugate pairs, but its shape ({cplx_conj_vec.shape[0]}"
            f" is odd)."
        )
    _v_sort = np.argsort(cplx_conj_vec)
    _v_cj_sort = np.argsort(cplx_conj_vec.conj())

    _diff = cplx_conj_vec[_v_sort] - cplx_conj_vec.conj()[_v_cj_sort]
    if not np.allclose(_diff, np.zeros_like(_diff)):
        raise ValueError(
            "The provided array does not consists of complex conjugate pairs"
        )

    _v = cplx_conj_vec[_v_sort]

    idx_list = []
    for i in range(cplx_conj_vec.shape[0]):
        _idx_tuple = (_v_sort[i], _v_cj_sort[i])
        _idx_tuple_r = (_idx_tuple[1], _idx_tuple[0])
        if _idx_tuple in idx_list:
            continue
        elif _idx_tuple_r in idx_list:
            continue
        else:
            if np.angle(_v[i]) >= 0:
                idx_list.append(_idx_tuple)
            else:
                idx_list.append(_idx_tuple_r)
    _pos_phase_idxs = [i[0] for i in idx_list]
    return np.asarray(_pos_phase_idxs, dtype=int)
