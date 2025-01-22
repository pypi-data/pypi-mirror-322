"""
Non-public functions called in data_generation.py
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Literal

import numpy as np
from attrs import evolve
from numpy.random import SeedSequence

from .. import DEFAULT_REC_RATIO, VERSION, ArrayDouble, RECForm  # noqa: TID252
from ..core.empirical_margin_distribution import mgn_data_resampler  # noqa: TID252
from ..core.pseudorandom_numbers import (  # noqa: TID252
    DEFAULT_DIST_PARMS,
    MultithreadedRNG,
    prng,
)
from . import (
    DEFAULT_EMPTY_ARRAY,
    DEFAULT_FCOUNT_WTS,
    FM2Constraint,
    MarginDataSample,
    PCMDistribution,
    PCMSpec,
    PriceDataSample,
    PriceSpec,
    SeedSequenceData,
    ShareDataSample,
    ShareSpec,
    SHRDistribution,
    SSZConstant,
)

__version__ = VERSION


def gen_share_data(
    _sample_size: int,
    _share_spec: ShareSpec,
    _fcount_rng_seed_seq: SeedSequence | None,
    _mktshr_rng_seed_seq: SeedSequence,
    _nthreads: int = 16,
    /,
) -> ShareDataSample:
    """Helper function for generating share data.

    Parameters
    ----------
    _share_spec
        Class specifying parameters for generating market share data
    _fcount_rng_seed_seq
        Seed sequence for assuring independent and, optionally, redundant streams
    _mktshr_rng_seed_seq
        Seed sequence for assuring independent and, optionally, redundant streams
    _nthreads
        Must be specified for generating repeatable random streams

    Returns
    -------
        Arrays representing shares, diversion ratios, etc. structured as a :ShareDataSample:

    """

    _recapture_form, _dist_type_mktshr, _dist_parms_mktshr, _firm_count_prob_wts = (
        getattr(_share_spec, _f)
        for _f in ("recapture_form", "dist_type", "dist_parms", "firm_counts_weights")
    )

    _ssz = _sample_size

    if _dist_type_mktshr == SHRDistribution.UNI:
        _mkt_share_sample = gen_market_shares_uniform(
            _ssz, _dist_parms_mktshr, _mktshr_rng_seed_seq, _nthreads
        )

    elif _dist_type_mktshr.name.startswith("DIR_"):
        _firm_count_prob_wts = (
            None
            if _firm_count_prob_wts is None
            else np.array(_firm_count_prob_wts, dtype=np.float64)
        )
        _mkt_share_sample = gen_market_shares_dirichlet_multimarket(
            _ssz,
            _recapture_form,
            _dist_type_mktshr,
            _dist_parms_mktshr,
            _firm_count_prob_wts,
            _fcount_rng_seed_seq,
            _mktshr_rng_seed_seq,
            _nthreads,
        )

    else:
        raise ValueError(
            f'Unexpected type, "{_dist_type_mktshr}" for share distribution.'
        )

    # If recapture_form == "inside-out", recalculate _aggregate_purchase_prob
    _frmshr_array = _mkt_share_sample.mktshr_array[:, :2]
    _r_bar = _share_spec.recapture_ratio or DEFAULT_REC_RATIO
    if _recapture_form == RECForm.INOUT:
        _mkt_share_sample = ShareDataSample(
            _mkt_share_sample.mktshr_array,
            _mkt_share_sample.fcounts,
            _mkt_share_sample.nth_firm_share,
            _r_bar / (1 - (1 - _r_bar) * _frmshr_array.min(axis=1, keepdims=True)),
        )

    return _mkt_share_sample


def gen_market_shares_uniform(
    _s_size: int = 10**6,
    _dist_parms_mktshr: ArrayDouble | None = DEFAULT_DIST_PARMS,
    _mktshr_rng_seed_seq: SeedSequence | None = None,
    _nthreads: int = 16,
    /,
) -> ShareDataSample:
    """Generate merging-firm shares from Uniform distribution on the 3-D simplex.

    Parameters
    ----------
    _s_size
        size of sample to be drawn

    _mktshr_rng_seed_seq
        seed for rng, so results can be made replicable

    _nthreads
        number of threads for random number generation

    Returns
    -------
        market shares and other market statistics for each draw (market)

    """

    _frmshr_array: ArrayDouble = np.empty((_s_size, 2), dtype=np.float64)

    _dist_parms_mktshr = _dist_parms_mktshr or DEFAULT_DIST_PARMS
    _mrng = MultithreadedRNG(
        _frmshr_array,
        dist_type="Uniform",
        dist_parms=_dist_parms_mktshr,
        seed_sequence=_mktshr_rng_seed_seq,
        nthreads=_nthreads,
    )
    _mrng.fill()
    # Convert draws on U[0, 1] to Uniformly-distributed draws on simplex, s_1 + s_2 <= 1
    _frmshr_array.sort(axis=1)

    _frmshr_array = np.array(
        (_frmshr_array[:, 0], _frmshr_array[:, 1] - _frmshr_array[:, 0]),
        _frmshr_array.dtype,
    ).T  # faster than np.stack() and variants

    # Keep only share combinations representing feasible mergers
    # This is a no-op for 64-bit floats, but is necessary for 32-bit floats
    _frmshr_array = _frmshr_array[_frmshr_array.min(axis=1) > 0]

    # Let a third column have values of "np.nan", so HHI calculations return "np.nan"
    _mktshr_array = np.pad(
        _frmshr_array, ((0, 0), (0, 1)), "constant", constant_values=np.nan
    )

    _fcounts = np.empty((_s_size, 1), np.int64)
    _nth_firm_share, _aggregate_purchase_prob = (
        np.empty(_fcounts.shape, np.float64)
        for _ in ("nth_firm_share", "aggregate_purchase_prob")
    )

    # This array is meant to be ignored, so a sentinel value is fine
    _fcounts.fill(-9999)

    _nth_firm_share.fill(np.nan)
    _aggregate_purchase_prob.fill(np.nan)

    return ShareDataSample(
        _mktshr_array, _fcounts, _nth_firm_share, _aggregate_purchase_prob
    )


def gen_market_shares_dirichlet_multimarket(
    _s_size: int = 10**6,
    _recapture_form: RECForm = RECForm.INOUT,
    _dist_type_dir: SHRDistribution = SHRDistribution.DIR_FLAT,
    _dist_parms_dir: ArrayDouble | None = None,
    _firm_count_wts: ArrayDouble | None = None,
    _fcount_rng_seed_seq: SeedSequence | None = None,
    _mktshr_rng_seed_seq: SeedSequence | None = None,
    _nthreads: int = 16,
    /,
) -> ShareDataSample:
    """Dirichlet-distributed shares with multiple firm-counts.

    Firm-counts may be specified as having Uniform distribution over the range
    of firm counts, or a set of probability weights may be specified. In the
    latter case the proportion of draws for each firm-count matches the
    specified probability weight.

    Parameters
    ----------
    _s_size
        sample size to be drawn

    _firm_count_wts
        firm count weights array for sample to be drawn

    _dist_type_dir
        Whether Dirichlet is Flat or Asymmetric

    _recapture_form
        r_1 = r_2 if "proportional", otherwise MNL-consistent

    _fcount_rng_seed_seq
        seed firm count rng, for replicable results

    _mktshr_rng_seed_seq
        seed market share rng, for replicable results

    _nthreads
        number of threads for parallelized random number generation

    Returns
    -------
        array of market shares and other market statistics

    """

    # _firm_count_wts: ArrayDouble = (
    #     DEFAULT_FCOUNT_WTS if _firm_count_wts is None else _firm_count_wts
    # )
    _firm_count_wts = DEFAULT_FCOUNT_WTS if _firm_count_wts is None else _firm_count_wts

    _min_choice_wt = 0.03 if _dist_type_dir == SHRDistribution.DIR_FLAT_CONSTR else 0.00
    _fcount_keys, _choice_wts = zip(
        *(
            _f
            for _f in zip(
                2 + np.arange(len(_firm_count_wts)),
                _firm_count_wts / _firm_count_wts.sum(),
                strict=True,
            )
            if _f[1] > _min_choice_wt
        )
    )
    _choice_wts = _choice_wts / sum(_choice_wts)

    _fc_max = _fcount_keys[-1]
    _dir_alphas_full = (
        [1.0] * _fc_max if _dist_parms_dir is None else _dist_parms_dir[:_fc_max]
    )
    if _dist_type_dir == SHRDistribution.DIR_ASYM:
        _dir_alphas_full = [2.0] * 6 + [1.5] * 5 + [1.25] * min(7, _fc_max)

    if _dist_type_dir == SHRDistribution.DIR_COND:

        def _gen_dir_alphas(_fcv: int) -> ArrayDouble:
            _dat = [2.5] * 2
            if _fcv > len(_dat):
                _dat += [1.0 / (_fcv - 2)] * (_fcv - 2)
            return np.array(_dat, dtype=np.float64)

    else:

        def _gen_dir_alphas(_fcv: int) -> ArrayDouble:
            return np.array(_dir_alphas_full[:_fcv], dtype=np.float64)

    _fcounts = prng(_fcount_rng_seed_seq).choice(
        _fcount_keys, size=(_s_size, 1), p=_choice_wts
    )

    _mktshr_seed_seq_ch = (
        _mktshr_rng_seed_seq.spawn(len(_fcount_keys))
        if isinstance(_mktshr_rng_seed_seq, SeedSequence)
        else SeedSequence(pool_size=8).spawn(len(_fcounts))
    )

    _aggregate_purchase_prob, _nth_firm_share = (
        np.empty((_s_size, 1)) for _ in range(2)
    )
    _mktshr_array = np.empty((_s_size, _fc_max), dtype=np.float64)
    for _f_val, _f_sseq in zip(_fcount_keys, _mktshr_seed_seq_ch, strict=True):
        _fcounts_match_rows = np.where(_fcounts == _f_val)[0]
        _dir_alphas_test = _gen_dir_alphas(_f_val)

        try:
            _mktshr_sample_f = gen_market_shares_dirichlet(
                _dir_alphas_test,
                len(_fcounts_match_rows),
                _recapture_form,
                _f_sseq,
                _nthreads,
            )
        except ValueError as _err:
            print(_f_val, len(_fcounts_match_rows))
            raise _err

        # Push data for present sample to parent
        _mktshr_array[_fcounts_match_rows] = np.pad(
            _mktshr_sample_f.mktshr_array,
            ((0, 0), (0, _fc_max - _mktshr_sample_f.mktshr_array.shape[1])),
            "constant",
        )
        _aggregate_purchase_prob[_fcounts_match_rows] = (
            _mktshr_sample_f.aggregate_purchase_prob
        )
        _nth_firm_share[_fcounts_match_rows] = _mktshr_sample_f.nth_firm_share

    if (_iss := np.round(np.einsum("ij->", _mktshr_array))) != _s_size or _iss != len(
        _mktshr_array
    ):
        raise ValueError(
            "DATA GENERATION ERROR: {} {} {}".format(
                "Generation of sample shares is inconsistent:",
                "array of drawn shares must some to the number of draws",
                "i.e., the sample size, which condition is not met.",
            )
        )

    return ShareDataSample(
        _mktshr_array, _fcounts, _nth_firm_share, _aggregate_purchase_prob
    )


def gen_market_shares_dirichlet(
    _dir_alphas: ArrayDouble,
    _s_size: int = 10**6,
    _recapture_form: RECForm = RECForm.INOUT,
    _mktshr_rng_seed_seq: SeedSequence | None = None,
    _nthreads: int = 16,
    /,
) -> ShareDataSample:
    """Dirichlet-distributed shares with fixed firm-count.

    Parameters
    ----------
    _dir_alphas
        Shape parameters for Dirichlet distribution

    _s_size
        sample size to be drawn

    _recapture_form
        r_1 = r_2 if RECForm.FIXED, otherwise MNL-consistent. If
        RECForm.OUTIN; the number of columns in the output share array
        is len(_dir_alphas) - 1.

    _mktshr_rng_seed_seq
        seed market share rng, for replicable results

    _nthreads
        number of threads for parallelized random number generation

    Returns
    -------
        array of market shares and other market statistics

    """

    if not isinstance(_dir_alphas, np.ndarray):
        _dir_alphas = np.array(_dir_alphas)

    if _recapture_form == RECForm.OUTIN:
        _dir_alphas = np.concatenate((_dir_alphas, _dir_alphas[-1:]))

    _mktshr_seed_seq_ch = (
        _mktshr_rng_seed_seq
        if isinstance(_mktshr_rng_seed_seq, SeedSequence)
        else SeedSequence(pool_size=8)
    )

    _mktshr_array = np.empty((_s_size, len(_dir_alphas)), dtype=np.float64)
    _mrng = MultithreadedRNG(
        _mktshr_array,
        dist_type="Dirichlet",
        dist_parms=_dir_alphas,
        seed_sequence=_mktshr_seed_seq_ch,
        nthreads=_nthreads,
    )
    _mrng.fill()

    if (_iss := np.round(np.einsum("ij->", _mktshr_array))) != _s_size or _iss != len(
        _mktshr_array
    ):
        print(_dir_alphas, _iss, repr(_s_size), len(_mktshr_array))
        print(repr(_mktshr_array[-10:, :]))
        raise ValueError(
            "DATA GENERATION ERROR: {} {} {}".format(
                "Generation of sample shares is inconsistent:",
                "array of drawn shares must sum to the number of draws",
                "i.e., the sample size, which condition is not met.",
            )
        )

    # If recapture_form == 'inside_out', further calculations downstream
    _aggregate_purchase_prob = np.empty((_s_size, 1), dtype=np.float64)
    _aggregate_purchase_prob.fill(np.nan)
    if _recapture_form == RECForm.OUTIN:
        _aggregate_purchase_prob = 1 - _mktshr_array[:, [-1]]  # type: ignore
        _mktshr_array = _mktshr_array[:, :-1] / _aggregate_purchase_prob  # type: ignore

    return ShareDataSample(
        _mktshr_array,
        (_mktshr_array.shape[-1] * np.ones((_s_size, 1))).astype(np.int64),
        _mktshr_array[:, [-1]],
        _aggregate_purchase_prob,
    )


def gen_divr_array(
    _recapture_form: RECForm,
    _recapture_ratio: float | None,
    _frmshr_array: ArrayDouble,
    _aggregate_purchase_prob: ArrayDouble = DEFAULT_EMPTY_ARRAY,
    /,
) -> ArrayDouble:
    """
    Given merging-firm shares and related parameters, return diverion ratios.

    If recapture is specified as :attr:`mergeron.RECForm.OUTIN`, then the
    choice-probability for the outside good must be supplied.

    Parameters
    ----------
    _recapture_form
        Enum specifying Fixed (proportional), Inside-out, or Outside-in

    _recapture_ratio
        If recapture is proportional or inside-out, the recapture ratio
        for the firm with the smaller share.

    _frmshr_array
        Merging-firm shares.

    _aggregate_purchase_prob
        1 minus probability that the outside good is chosen; converts
        market shares to choice probabilities by multiplication.

    Raises
    ------
    ValueError
        If the firm with the smaller share does not have the larger
        diversion ratio between the merging firms.

    Returns
    -------
        Merging-firm diversion ratios for mergers in the sample.

    """

    _divr_array: ArrayDouble
    if _recapture_form == RECForm.FIXED:
        _divr_array = _recapture_ratio * _frmshr_array[:, ::-1] / (1 - _frmshr_array)  # type: ignore

    else:
        _purchprob_array = _aggregate_purchase_prob * _frmshr_array
        _divr_array = _purchprob_array[:, ::-1] / (1 - _purchprob_array)

    _divr_assert_test = (
        (np.round(np.einsum("ij->i", _frmshr_array), 15) == 1)
        | (np.argmin(_frmshr_array, axis=1) == np.argmax(_divr_array, axis=1))
    )[:, None]
    if not all(_divr_assert_test):
        raise ValueError(
            "{} {} {} {}".format(
                "Data construction fails tests:",
                "the index of min(s_1, s_2) must equal",
                "the index of max(d_12, d_21), for all draws.",
                "unless frmshr_array sums to 1.00.",
            )
        )

    return _divr_array


def gen_margin_price_data(
    _frmshr_array: ArrayDouble,
    _nth_firm_share: ArrayDouble,
    _aggregate_purchase_prob: ArrayDouble,
    _pcm_spec: PCMSpec,
    _price_spec: PriceSpec,
    _hsr_filing_test_type: SSZConstant,
    _pcm_rng_seed_seq: SeedSequence,
    _pr_rng_seed_seq: SeedSequence | None = None,
    _nthreads: int = 16,
    /,
) -> tuple[MarginDataSample, PriceDataSample]:
    """Generate margin and price data for mergers in the sample.

    Parameters
    ----------
    _frmshr_array
        Merging-firm shares; see :class:`mergeron.gen.ShareSpec`.

    _nth_firm_share
        Share of the nth firm in the sample.

    _aggregate_purchase_prob
        1 minus probability that the outside good is chosen; converts
        market shares to choice probabilities by multiplication.

    _pcm_spec
        Enum specifying whether to use asymmetric or flat margins. see
        :class:`mergeron.gen.PCMSpec`.

    _price_spec
        Enum specifying whether to use symmetric, positive, or negative
        margins; see :class:`mergeron.gen.PriceSpec`.

    _hsr_filing_test_type
        Enum specifying restriction, if any, to impose on market data sample
        to model HSR filing requirements; see :class:`mergeron.gen.SSZConstant`.

    _pcm_rng_seed_seq
        Seed sequence for generating margin data.

    _pr_rng_seed_seq
        Seed sequence for generating price data.

    _nthreads
        Number of threads to use in generating price data.

    Returns
    -------
        Simulated margin- and price-data arrays for mergers in the sample.
    """

    _margin_data = MarginDataSample(
        np.empty_like(_frmshr_array), np.ones(len(_frmshr_array)) == 0
    )

    _price_array, _price_ratio_array = (
        np.ones_like(_frmshr_array, np.float64),
        np.empty_like(_frmshr_array, np.float64),
    )

    _pr_max_ratio = 5.0
    match _price_spec:
        case PriceSpec.SYM:
            _nth_firm_price = np.ones((len(_frmshr_array), 1), np.float64)
        case PriceSpec.POS:
            _price_array, _nth_firm_price = (
                np.ceil(_p * _pr_max_ratio) for _p in (_frmshr_array, _nth_firm_share)
            )
        case PriceSpec.NEG:
            _price_array, _nth_firm_price = (
                np.ceil((1 - _p) * _pr_max_ratio)
                for _p in (_frmshr_array, _nth_firm_share)
            )
        case PriceSpec.ZERO:
            _price_array_gen = prng(_pr_rng_seed_seq).choice(
                1 + np.arange(_pr_max_ratio), size=(len(_frmshr_array), 3)
            )
            _price_array = _price_array_gen[:, :2]
            _nth_firm_price = _price_array_gen[:, [2]]  # type: ignore
            # del _price_array_gen
        case PriceSpec.CSY:
            # TODO:
            # evolve FM2Constraint (save running MNL test twice); evolve copy of _mkt_sample_spec=1q
            # generate the margin data
            # generate price and margin data
            _frmshr_array_plus = np.hstack((_frmshr_array, _nth_firm_share))
            _pcm_spec_here = evolve(_pcm_spec, firm2_pcm_constraint=FM2Constraint.IID)
            _margin_data = _gen_margin_data(
                _frmshr_array_plus,
                np.ones_like(_frmshr_array_plus, np.float64),
                _aggregate_purchase_prob,
                _pcm_spec_here,
                _pcm_rng_seed_seq,
                _nthreads,
            )

            _pcm_array, _mnl_test_array = (
                getattr(_margin_data, _f) for _f in ("pcm_array", "mnl_test_array")
            )

            _price_array_here = 1 / (1 - _pcm_array)
            _price_array = _price_array_here[:, :2]
            _nth_firm_price = _price_array_here[:, [-1]]
            if _pcm_spec.firm2_pcm_constraint == FM2Constraint.MNL:
                # Generate i.i.d. PCMs then take PCM0 and construct PCM1
                # Regenerate MNL test
                _purchase_prob_array = _aggregate_purchase_prob * _frmshr_array
                _pcm_array[:, 1] = np.divide(
                    (
                        _m1_nr := np.divide(
                            np.einsum(
                                "ij,ij,ij->ij",
                                _price_array[:, [0]],
                                _pcm_array[:, [0]],
                                1 - _purchase_prob_array[:, [0]],
                            ),
                            1 - _purchase_prob_array[:, [1]],
                        )
                    ),
                    1 + _m1_nr,
                )
                _mnl_test_array = (_pcm_array[:, [1]] >= 0) & (_pcm_array[:, [1]] <= 1)

            _margin_data = MarginDataSample(_pcm_array[:, :2], _mnl_test_array)
            del _price_array_here
        case _:
            raise ValueError(
                f'Specification of price distribution, "{_price_spec.value}" is invalid.'
            )
    if _price_spec != PriceSpec.CSY:
        _margin_data = _gen_margin_data(
            _frmshr_array,
            _price_array,
            _aggregate_purchase_prob,
            _pcm_spec,
            _pcm_rng_seed_seq,
            _nthreads,
        )

    _price_array = _price_array.astype(np.float64)
    _rev_array = _price_array * _frmshr_array
    _nth_firm_rev = _nth_firm_price * _nth_firm_share

    # Although `_test_rev_ratio_inv` is not fixed at 10%,
    # the ratio has not changed since inception of the HSR filing test,
    # so we treat it as a constant of merger enforcement policy.
    _test_rev_ratio, _test_rev_ratio_inv = 10, 1 / 10

    match _hsr_filing_test_type:
        case SSZConstant.HSR_TEN:
            # See, https://www.ftc.gov/enforcement/premerger-notification-program/
            #   -> Procedures For Submitting Post-Consummation Filings
            #    -> Key Elements to Determine Whether a Post Consummation Filing is Required
            #           under heading, "Historical Thresholds"
            # Revenue ratio has been 10-to-1 since inception
            # Thus, a simple form of the HSR filing test would impose a 10-to-1
            # ratio restriction on the merging firms' revenues
            _rev_ratio = (_rev_array.min(axis=1) / _rev_array.max(axis=1)).round(4)
            _hsr_filing_test = _rev_ratio >= _test_rev_ratio_inv
            # del _rev_array, _rev_ratio
        case SSZConstant.HSR_NTH:
            # To get around the 10-to-1 ratio restriction, specify that the nth firm test:
            # if the smaller merging firm matches or exceeds the n-th firm in size, and
            # the larger merging firm has at least 10 times the size of the nth firm,
            # the size test is considered met.
            # Alternatively, if the smaller merging firm has 10% or greater share,
            # the value of transaction test is considered met.
            _rev_ratio_to_nth = np.round(np.sort(_rev_array, axis=1) / _nth_firm_rev, 4)
            _hsr_filing_test = (
                np.einsum(
                    "ij->i",
                    1 * (_rev_ratio_to_nth > [1, _test_rev_ratio]),
                    dtype=np.int64,
                )
                == _rev_ratio_to_nth.shape[1]
            )

            # del _nth_firm_rev, _rev_ratio_to_nth
        case _:
            # Otherwise, all draws meet the filing test
            _hsr_filing_test = np.ones(len(_frmshr_array), dtype=bool)
    _hsr_filing_test = _hsr_filing_test | (
        _frmshr_array.min(axis=1) >= _test_rev_ratio_inv
    )

    return _margin_data, PriceDataSample(_price_array, _hsr_filing_test)


def _gen_margin_data(
    _frmshr_array: ArrayDouble,
    _price_array: ArrayDouble,
    _aggregate_purchase_prob: ArrayDouble,
    _pcm_spec: PCMSpec,
    _pcm_rng_seed_seq: SeedSequence,
    _nthreads: int = 16,
    /,
) -> MarginDataSample:
    _dist_type_pcm, _dist_firm2_pcm, _dist_parms_pcm = (
        getattr(_pcm_spec, _f)
        for _f in ("dist_type", "firm2_pcm_constraint", "dist_parms")
    )

    _pcm_array = (
        np.empty((len(_frmshr_array), 1), dtype=np.float64)
        if _pcm_spec.firm2_pcm_constraint == FM2Constraint.SYM
        else np.empty_like(_frmshr_array, dtype=np.float64)
    )

    _beta_min, _beta_max = [None] * 2  # placeholder
    if _dist_type_pcm == PCMDistribution.EMPR:
        _pcm_array = mgn_data_resampler(
            _pcm_array.shape, seed_sequence=_pcm_rng_seed_seq
        )
    else:
        _dist_type: Literal["Beta", "Uniform"]
        if _dist_type_pcm in (PCMDistribution.BETA, PCMDistribution.BETA_BND):
            _dist_type = "Beta"
            _dist_parms_pcm = (
                (
                    np.array([0, 1, 0, 1], np.float64)
                    if _dist_parms_pcm == PCMDistribution.BETA_BND
                    else np.ones(2, np.float64)
                )
                if _dist_parms_pcm is None
                else _dist_parms_pcm
            )
            _dist_parms = beta_located_bound(_dist_parms_pcm)

        else:
            _dist_type = "Uniform"
            _dist_parms = (
                DEFAULT_DIST_PARMS if _dist_parms_pcm is None else _dist_parms_pcm
            )

        _pcm_rng = MultithreadedRNG(
            _pcm_array,
            dist_type=_dist_type,
            dist_parms=_dist_parms,
            seed_sequence=_pcm_rng_seed_seq,
            nthreads=_nthreads,
        )
        _pcm_rng.fill()
        del _pcm_rng

    if _dist_type_pcm == PCMDistribution.BETA_BND:
        _beta_min, _beta_max = _dist_parms_pcm[2:]
        _pcm_array = (_beta_max - _beta_min) * _pcm_array + _beta_min
        del _beta_min, _beta_max

    if _dist_firm2_pcm == FM2Constraint.SYM:
        _pcm_array = np.column_stack((_pcm_array,) * _frmshr_array.shape[1])
    if _dist_firm2_pcm == FM2Constraint.MNL:
        # Impose FOCs from profit-maximization with MNL demand
        if _dist_type_pcm == PCMDistribution.EMPR:
            print(
                "NOTE: Estimated Firm 2 parameters will not be consistent with "
                "the empirical distribution of margins in the source data. For "
                "consistency, respecify pcm_spec.firm2_pcm_constraint = FM2Constraint.IID."
            )
        _purchase_prob_array = _aggregate_purchase_prob * _frmshr_array

        _pcm_array[:, [1]] = np.divide(
            np.einsum(
                "ij,ij,ij->ij",
                _price_array[:, [0]],
                _pcm_array[:, [0]],
                1 - _purchase_prob_array[:, [0]],
            ),
            np.einsum(
                "ij,ij->ij", _price_array[:, [1]], 1 - _purchase_prob_array[:, [1]]
            ),
        )

        _mnl_test_array = _pcm_array[:, 1].__ge__(0) & _pcm_array[:, 1].__le__(1)
    else:
        _mnl_test_array = np.ones(len(_pcm_array), dtype=bool)

    return MarginDataSample(_pcm_array, _mnl_test_array)


def _beta_located(
    _mu: float | ArrayDouble, _sigma: float | ArrayDouble, /
) -> ArrayDouble:
    """
    Given mean and stddev, return shape parameters for corresponding Beta distribution

    Solve the first two moments of the standard Beta to get the shape parameters.

    Parameters
    ----------
    _mu
        mean
    _sigma
        standardd deviation

    Returns
    -------
        shape parameters for Beta distribution

    """

    _mul = -1 + _mu * (1 - _mu) / _sigma**2
    return np.array([_mu * _mul, (1 - _mu) * _mul], dtype=np.float64)


def beta_located_bound(_dist_parms: ArrayDouble, /) -> ArrayDouble:
    R"""
    Return shape parameters for a non-standard beta, given the mean, stddev, range


    Recover the r.v.s as
    :math:`\min + (\max - \min) \cdot \symup{Β}(a, b)`,
    with `a` and `b` calculated from the specified mean (:math:`\mu`) and
    variance (:math:`\sigma`). [8]_

    Parameters
    ----------
    _dist_parms
        vector of :math:`\mu`, :math:`\sigma`, :math:`\mathtt{\min}`, and :math:`\mathtt{\max}` values

    Returns
    -------
        shape parameters for Beta distribution

    Notes
    -----
    For example, ``beta_located_bound(np.array([0.5, 0.2887, 0.0, 1.0]))``.

    References
    ----------
    .. [8] NIST, Beta Distribution. https://www.itl.nist.gov/div898/handbook/eda/section3/eda366h.htm
    """  # noqa: RUF002

    _bmu, _bsigma, _bmin, _bmax = _dist_parms
    return _beta_located((_bmu - _bmin) / (_bmax - _bmin), _bsigma / (_bmax - _bmin))


def parse_seed_seq_list(
    _sseq_list: Sequence[SeedSequence] | None,
    _mktshr_dist_type: SHRDistribution,
    _price_spec: PriceSpec,
    /,
) -> SeedSequenceData:
    """Initialize RNG seed sequences to ensure independence of distinct random streams.

    The tuple of SeedSequences, is parsed in the following order
    for generating the relevant random variates:
    1.) quantity shares
    2.) price-cost margins
    3.) firm-counts, if :code:`MarketSpec.share_spec.dist_type` is a Dirichlet distribution
    4.) prices, if :code:`MarketSpec.price_spec ==`:attr:`mergeron.gen.PriceSpec.ZERO`.



    Parameters
    ----------
    _sseq_list
        List of RNG seed sequences

    _mktshr_dist_type
        Market share distribution type

    _price_spec
        Price specification

    Returns
    -------
        Seed sequence data

    """
    _seed_count = 2 if _mktshr_dist_type == SHRDistribution.UNI else 3
    _seed_count += 1 if _price_spec == PriceSpec.ZERO else 0

    _fcount_rng_seed_seq: SeedSequence | None = None
    _pr_rng_seed_seq: SeedSequence | None = None

    _sseq_list = (
        _sseq_list
        if _sseq_list
        else tuple(SeedSequence(pool_size=8) for _ in range(_seed_count))
    )

    if (_l := len(_sseq_list)) < _seed_count:
        raise ValueError(
            f"Seed sequence list must contain {_seed_count} seed sequences; "
            f"only {_l} given."
        )

    _mktshr_rng_seed_seq, _pcm_rng_seed_seq = _sseq_list[:2]
    _fcount_rng_seed_seq = (
        None if _mktshr_dist_type == SHRDistribution.UNI else _sseq_list[2]
    )
    _pr_rng_seed_seq = _sseq_list[-1] if _price_spec == PriceSpec.ZERO else None

    return SeedSequenceData(
        _mktshr_rng_seed_seq, _pcm_rng_seed_seq, _fcount_rng_seed_seq, _pr_rng_seed_seq
    )
