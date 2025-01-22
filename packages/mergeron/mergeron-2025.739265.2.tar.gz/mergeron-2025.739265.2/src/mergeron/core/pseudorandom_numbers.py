"""
Functions for generating synthetic data under specified distributions.

Uses multiple CPUs when available, with PCG64DXSM as the PRNG
https://github.com/numpy/numpy/issues/16313.

"""

from __future__ import annotations

import concurrent.futures
from collections.abc import Sequence
from multiprocessing import cpu_count
from typing import Literal

import numpy as np
from attrs import Attribute, define, field
from numpy.random import PCG64DXSM, Generator, SeedSequence

from .. import VERSION, ArrayDouble  # noqa: TID252

__version__ = VERSION

NTHREADS = 2 * cpu_count()
DEFAULT_DIST_PARMS: ArrayDouble = np.array([0.0, 1.0], float)
DEFAULT_BETA_DIST_PARMS: ArrayDouble = np.array([1.0, 1.0], float)


def prng(_s: SeedSequence | None = None, /) -> np.random.Generator:
    """Adopt the PCG64DXSM bit-generator, the future default in numpy.default_rng().

    Parameters
    ----------
    _s
        SeedSequence, for generating random numbers in repeatable fashion.

    Returns
    -------
        A numpy random BitGenerator.

    """
    return Generator(PCG64DXSM(_s))


def gen_seed_seq_list_default(
    _sseq_list_len: int = 3, /, *, generated_entropy: Sequence[int] | None = None
) -> list[SeedSequence]:
    """
    Return specified number of SeedSequences, for generating random variates

    Initializes a specified number of SeedSequences based on a set of
    10 generated "seeds" in a hard-coded list. If the required number of
    random variates is larger than 10, the user must first generate
    a sufficient number of seeds to draw upon for initializing SeedSequences.
    The generated seeds can be reused in subsequent calls to this function.

    Parameters
    ----------
    _sseq_list_len
        Number of SeedSequences to initialize

    generated_entropy
        A list of integers with length not less than _s, to be used as seeds
        for initializing SeedSequences. A list of 10 appropriately generated
        integers is used as default.

    Returns
    -------
        A list of numpy SeedSequence objects, which can be used to seed prng() or to spawn
        seed sequences that can be used as seeds to generate non-overlapping streams in parallel.

    Raises
    ------
    ValueError
        When, :math:`\\_sseq\\_list\\_len > max(10, len(generated\\_entropy))`.

    References
    ----------
    *See*, https://numpy.org/doc/stable/reference/random/parallel.html


    """

    generated_entropy = generated_entropy or [
        92156365243929466422624541055805800714117298857186959727264899187749727119124,
        45508962760932900824607908382088764294813063250106926349700153055300051503944,
        11358852481965974965852447884047438302274082458147659701772223782670581495409,
        98335771128074178116267837103565107347248838466705856121954317889296202882090,
        99169860978478959086120522268530894898455162069966492625932871292847103049882,
        87208206842095975410011581094164970201731602958127872604742955058753939512957,
        3615645999448046437740316672917313005913548649308233620056831197005377987468,
        108909094416963715978441140822183411647298834317413586830609215654532919223699,
        88096344099146385192471976829122012867254940684757663128881853302534662995332,
        63206306147411023146090085885772240748399174641427012462446714431253444120718,
    ]

    if _sseq_list_len > (_lge := len(generated_entropy)):
        _e_str_segs = (
            "This function can presently create SeedSequences for generating up to ",
            f"{_lge:,d} independent random variates. If you really need to generate ",
            f"more than {_lge:,d} seeded independent random variates, please pass a ",
            "sufficiently large list of seeds as generated_entropy. See,",
            "{}/{}.".format(
                "https://numpy.org/doc/stable/reference/random",
                "bit_generators/generated/numpy.random.SeedSequence.html",
            ),
        )
        raise ValueError("".join(_e_str_segs))

    return [SeedSequence(_s, pool_size=8) for _s in generated_entropy[:_sseq_list_len]]


@define
class MultithreadedRNG:
    """Fill given array on demand with pseudo-random numbers as specified.

    Random number generation is multithreaded, using twice
    the number of threads as available CPU cores by default.
    If a seed sequence is provided, it is used in a thread-safe way
    to generate repeatable i.i.d. draws. All arguments are validated
    before commencing multithreaded random number generation.
    """

    values: ArrayDouble = field(kw_only=False, default=None)
    """Output array to which generated data are over-written

    Array-length defines the number of i.i.d. (vector) draws.
    """

    dist_type: Literal[
        "Beta", "Dirichlet", "Gaussian", "Normal", "Random", "Uniform"
    ] = field(kw_only=True, default="Uniform")
    """Distribution for the generated random numbers.

    Default is "Uniform".
     """

    @dist_type.validator
    def __dtv(
        _instance: MultithreadedRNG, _attribute: Attribute[str], _value: str, /
    ) -> None:
        if _value not in (
            _rdts := ("Beta", "Dirichlet", "Gaussian", "Normal", "Random", "Uniform")
        ):
            raise ValueError(f"Specified distribution must be one of {_rdts}")

    dist_parms: ArrayDouble | None = field(kw_only=True, default=DEFAULT_DIST_PARMS)
    """Parameters, if any, for tailoring random number generation
    """

    @dist_parms.validator
    def __dpv(
        _instance: MultithreadedRNG, _attribute: Attribute[str], _value: ArrayDouble, /
    ) -> None:
        if _value is not None:
            if not isinstance(_value, Sequence | np.ndarray):
                raise ValueError(
                    "When specified, distribution parameters must be a list, tuple or Numpy array"
                )

            elif (
                _instance.dist_type != "Dirichlet"
                and (_lrdp := len(_value)) != (_trdp := 2)
            ) or (
                _instance.dist_type == "Dirichlet"
                and (_lrdp := len(_value)) != (_trdp := _instance.values.shape[1])
            ):
                raise ValueError(f"Expected {_trdp} parameters, got, {_lrdp}")

            elif (
                _instance.dist_type in ("Beta", "Dirichlet")
                and (np.array(_value) <= 0.0).any()
            ):
                raise ValueError(
                    "Shape and location parameters must be strictly positive"
                )

    seed_sequence: SeedSequence | None = field(kw_only=True, default=None)
    """Seed sequence for generating random numbers."""

    nthreads: int = field(kw_only=True, default=NTHREADS)
    """Number of threads to spawn for random number generation."""

    def fill(self) -> None:
        """Fill the provided output array with random number draws as specified."""

        if (
            self.dist_parms is None
            or not (
                _dist_parms := np.array(self.dist_parms)  # one-shot conversion
            ).any()
        ):
            if self.dist_type == "Beta":
                _dist_parms = DEFAULT_BETA_DIST_PARMS
            elif self.dist_type == "Dirichlet":
                _dist_parms = np.ones(self.values.shape[1], float)
            else:
                _dist_parms = DEFAULT_DIST_PARMS

        if self.dist_parms is None or np.array_equal(
            self.dist_parms, DEFAULT_DIST_PARMS
        ):
            if self.dist_type == "Uniform":
                _dist_type = "Random"
            elif self.dist_type == "Normal":
                _dist_type = "Gaussian"
        else:
            _dist_type = self.dist_type

        _step_size = (len(self.values) / self.nthreads).__ceil__()
        # int; function gives float unsuitable for slicing

        _seed_sequence = self.seed_sequence or SeedSequence(pool_size=8)

        _random_generators = tuple(
            prng(_t) for _t in _seed_sequence.spawn(self.nthreads)
        )

        def _fill(
            _rng: np.random.Generator,
            _dist_type: str,
            _dist_parms: ArrayDouble,
            _out: ArrayDouble,
            _first: int,
            _last: int,
            /,
        ) -> None:
            _sz: tuple[int, ...] = _out[_first:_last].shape
            match _dist_type:
                case "Beta":
                    _shape_a, _shape_b = _dist_parms
                    _out[_first:_last] = _rng.beta(_shape_a, _shape_b, size=_sz)
                case "Dirichlet":
                    _out[_first:_last] = _rng.dirichlet(_dist_parms, size=_sz[:-1])
                case "Gaussian":
                    _rng.standard_normal(out=_out[_first:_last])
                case "Normal":
                    _mu, _sigma = _dist_parms
                    _out[_first:_last] = _rng.normal(_mu, _sigma, size=_sz)
                case "Random":
                    _rng.random(out=_out[_first:_last])
                case "Uniform":
                    _uni_l, _uni_h = _dist_parms
                    _out[_first:_last] = _rng.uniform(_uni_l, _uni_h, size=_sz)
                case _:
                    "Unreachable. The validator would have rejected this as invalid."

        with concurrent.futures.ThreadPoolExecutor(self.nthreads) as _executor:
            for i in range(self.nthreads):
                _range_first = i * _step_size
                _range_last = min(len(self.values), (i + 1) * _step_size)

                _executor.submit(
                    _fill,
                    _random_generators[i],
                    _dist_type,
                    _dist_parms,
                    self.values,
                    _range_first,
                    _range_last,
                )
