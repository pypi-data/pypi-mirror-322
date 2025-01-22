from __future__ import annotations

import enum
from pathlib import Path
from typing import Literal

import numpy as np
from numpy.typing import NDArray

_PKG_NAME: str = Path(__file__).parent.stem

VERSION = "2025.739265.2"

__version__ = VERSION

DATA_DIR: Path = Path.home() / _PKG_NAME
"""
Defines a subdirectory named for this package in the user's home path.

If the subdirectory doesn't exist, it is created on package invocation.
"""
if not DATA_DIR.is_dir():
    DATA_DIR.mkdir(parents=False)

np.set_printoptions(precision=24, floatmode="fixed")

type HMGPubYear = Literal[1982, 1984, 1992, 2010, 2023]

type ArrayBoolean = NDArray[np.bool_]
type ArrayFloat = NDArray[np.float16 | np.float32 | np.float64 | np.float128]
type ArrayINT = NDArray[np.intp]

type ArrayDouble = NDArray[np.float64]
type ArrayBIGINT = NDArray[np.int64]

DEFAULT_REC_RATIO = 0.85


@enum.unique
class RECForm(enum.StrEnum):
    """For derivation of recapture ratio from market shares."""

    INOUT = "inside-out"
    OUTIN = "outside-in"
    FIXED = "proportional"


@enum.unique
class UPPAggrSelector(enum.StrEnum):
    """
    Aggregator for GUPPI and diversion ratio estimates.

    """

    AVG = "average"
    CPA = "cross-product-share weighted average"
    CPD = "cross-product-share weighted distance"
    CPG = "cross-product-share weighted geometric mean"
    DIS = "symmetrically-weighted distance"
    GMN = "geometric mean"
    MAX = "max"
    MIN = "min"
    OSA = "own-share weighted average"
    OSD = "own-share weighted distance"
    OSG = "own-share weighted geometric mean"
