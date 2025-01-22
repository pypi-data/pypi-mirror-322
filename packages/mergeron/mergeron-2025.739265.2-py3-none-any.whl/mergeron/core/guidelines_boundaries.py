"""
Methods for defining and analyzing boundaries for Guidelines standards,
with a canvas on which to draw boundaries for Guidelines standards.

"""

from __future__ import annotations

import decimal
from dataclasses import dataclass
from typing import Literal

import numpy as np
from attrs import Attribute, field, frozen, validators
from mpmath import mp, mpf  # type: ignore

from .. import (  # noqa: TID252
    DEFAULT_REC_RATIO,
    VERSION,
    ArrayDouble,
    HMGPubYear,
    RECForm,
    UPPAggrSelector,
)
from . import guidelines_boundary_functions as gbfn

__version__ = VERSION


mp.dps = 32
mp.trap_complex = True


@dataclass(frozen=True)
class HMGThresholds:
    delta: float
    fc: float
    rec: float
    guppi: float
    divr: float
    cmcr: float
    ipr: float


@frozen
class GuidelinesThresholds:
    """
    Guidelines threholds by Guidelines publication year

    ΔHHI, Recapture Ratio, GUPPI, Diversion ratio, CMCR, and IPR thresholds
    constructed from concentration standards in Guidelines published in
    1982, 1984, 1992, 2010, and 2023.

    """

    pub_year: HMGPubYear = field(
        kw_only=False,
        default=2023,
        validator=validators.in_([1982, 1984, 1992, 2010, 2023]),
    )
    """
    Year of publication of the Guidelines
    """

    safeharbor: HMGThresholds = field(kw_only=True, default=None)
    """
    Negative presumption quantified on various measures

    ΔHHI safeharbor bound, default recapture ratio, GUPPI bound,
    diversion ratio limit, CMCR, and IPR
    """

    presumption: HMGThresholds = field(kw_only=True, default=None)
    """
    Presumption of harm defined in HMG

    ΔHHI bound and corresponding default recapture ratio, GUPPI bound,
    diversion ratio limit, CMCR, and IPR
    """

    imputed_presumption: HMGThresholds = field(kw_only=True, default=None)
    """
    Presumption of harm imputed from guidelines

    ΔHHI bound inferred from strict numbers-equivalent
    of (post-merger) HHI presumption, and corresponding default recapture ratio,
    GUPPI bound, diversion ratio limit, CMCR, and IPR
    """

    def __attrs_post_init__(self, /) -> None:
        # In the 2023 Guidelines, the agencies do not define a
        # negative presumption, or safeharbor. Practically speaking,
        # given resource constraints and loss aversion, it is likely
        # that staff only investigates mergers that meet the presumption;
        # thus, here, the tentative delta safeharbor under
        # the 2023 Guidelines is 100 points
        _hhi_p, _dh_s, _dh_p = {
            1982: (_s1982 := (0.18, 0.005, 0.01)),
            1984: _s1982,
            1992: _s1982,
            2010: (0.25, 0.01, 0.02),
            2023: (0.18, 0.01, 0.01),
        }[self.pub_year]

        object.__setattr__(
            self,
            "safeharbor",
            HMGThresholds(
                _dh_s,
                _fc := int(np.ceil(1 / _hhi_p)),
                _r := float(_r_s := gbfn.round_cust(_fc / (_fc + 1), frac=0.05)),
                _g := float(guppi_from_delta(_dh_s, m_star=1.0, r_bar=_r)),
                _dr := float(1 - _r_s),
                _cmcr := 0.03,  # Not strictly a Guidelines standard
                _ipr := _g,  # Not strictly a Guidelines standard
            ),
        )

        object.__setattr__(
            self, "presumption", HMGThresholds(_dh_p, _fc, _r, _g, _dr, _cmcr, _ipr)
        )

        # imputed_presumption is relevant for presumptions implicating
        # mergers *to* symmetry in numbers-equivalent of post-merger HHI
        # as in 2010 U.S.Guidelines
        object.__setattr__(
            self,
            "imputed_presumption",
            (
                HMGThresholds(
                    2 * (0.5 / _fc) ** 2,
                    _fc,
                    float(
                        _r_i := gbfn.round_cust(
                            (_fc - 1 / 2) / (_fc + 1 / 2), frac=0.05
                        )
                    ),
                    _g,
                    float((1 - _r_i) / 2),
                    _cmcr,
                    _ipr := _g,
                )
                if self.pub_year == 2010
                else HMGThresholds(
                    2 * (1 / (_fc + 1)) ** 2, _fc, _r, _g, _dr, _cmcr, _ipr
                )
            ),
        )


@frozen
class ConcentrationBoundary:
    """Concentration parameters, boundary coordinates, and area under concentration boundary."""

    measure_name: Literal[
        "ΔHHI", "Combined share", "Pre-merger HHI", "Post-merger HHI"
    ] = field(kw_only=False, default="ΔHHI")

    @measure_name.validator
    def __mnv(
        _instance: ConcentrationBoundary, _attribute: Attribute[str], _value: str, /
    ) -> None:
        if _value not in (
            "ΔHHI",
            "Combined share",
            "Pre-merger HHI",
            "Post-merger HHI",
        ):
            raise ValueError(f"Invalid name for a concentration measure, {_value!r}.")

    threshold: float = field(kw_only=False, default=0.01)

    @threshold.validator
    def __tv(
        _instance: ConcentrationBoundary, _attribute: Attribute[float], _value: float, /
    ) -> None:
        if not 0 <= _value <= 1:
            raise ValueError("Concentration threshold must lie between 0 and 1.")

    precision: int = field(
        kw_only=False, default=5, validator=validators.instance_of(int)
    )

    coordinates: ArrayDouble = field(init=False, kw_only=True)
    """Market-share pairs as Cartesian coordinates of points on the concentration boundary."""

    area: float = field(init=False, kw_only=True)
    """Area under the concentration boundary."""

    def __attrs_post_init__(self, /) -> None:
        match self.measure_name:
            case "ΔHHI":
                _conc_fn = gbfn.hhi_delta_boundary
            case "Combined share":
                _conc_fn = gbfn.combined_share_boundary
            case "Pre-merger HHI":
                _conc_fn = gbfn.hhi_pre_contrib_boundary
            case "Post-merger HHI":
                _conc_fn = gbfn.hhi_post_contrib_boundary

        _boundary = _conc_fn(self.threshold, dps=self.precision)
        object.__setattr__(self, "coordinates", _boundary.coordinates)
        object.__setattr__(self, "area", _boundary.area)


@frozen
class DiversionRatioBoundary:
    """
    Diversion ratio specification, boundary coordinates, and area under boundary.

    Along with the default diversion ratio and recapture ratio,
    a diversion ratio boundary specification includes the recapture form --
    whether fixed for both merging firms' products ("proportional") or
    consistent with share-proportionality, i.e., "inside-out";
    the method of aggregating diversion ratios for the two products, and
    the precision for the estimate of area under the divertion ratio boundary
    (also defines the number of points on the boundary).

    """

    diversion_ratio: float = field(kw_only=False, default=0.065)

    @diversion_ratio.validator
    def __dvv(
        _instance: DiversionRatioBoundary,
        _attribute: Attribute[float],
        _value: float,
        /,
    ) -> None:
        if not (isinstance(_value, float) and 0 <= _value <= 1):
            raise ValueError(
                "Margin-adjusted benchmark share ratio must lie between 0 and 1."
            )

    recapture_ratio: float = field(
        kw_only=False,
        default=DEFAULT_REC_RATIO,
        validator=validators.instance_of(float),
    )

    recapture_form: RECForm | None = field(kw_only=True, default=RECForm.INOUT)
    """
    The form of the recapture ratio.

    When :attr:`mergeron.RECForm.INOUT`, the recapture ratio for
    he product having the smaller market-share is assumed to equal the default,
    and the recapture ratio for the product with the larger market-share is
    computed assuming MNL demand. Fixed recapture ratios are specified as
    :attr:`mergeron.RECForm.FIXED`. (To specify that recapture ratios be
    constructed from the generated purchase-probabilities for products in
    the market and for the outside good, specify :attr:`mergeron.RECForm.OUTIN`.)

    The GUPPI boundary is a continuum of diversion ratio boundaries conditional on
    price-cost margins, :math:`d_{ij} = g_i * p_i / (m_j * p_j)`,
    with :math:`d_{ij}` the diverion ratio from product :math:`i` to product :math:`j`;
    :math:`g_i` the GUPPI for product :math:`i`;
    :math:`m_j` the margin for product :math:`j`; and
    :math:`p_i, p_j` the prices of goods :math:`i, j`, respectively.

    """

    @recapture_form.validator
    def __rsv(
        _instance: DiversionRatioBoundary,
        _attribute: Attribute[RECForm],
        _value: RECForm,
        /,
    ) -> None:
        if _value and not (isinstance(_value, RECForm)):
            raise ValueError(f"Invalid recapture specification, {_value!r}.")
        if _value == RECForm.OUTIN and _instance.recapture_ratio:
            raise ValueError(
                f"Invalid recapture specification, {_value!r}. "
                "You may consider specifying `mergeron.RECForm.INOUT` here, and "
                'assigning the default recapture ratio as attribute, "recapture_ratio" of '
                "this `DiversionRatioBoundarySpec` object."
            )
        if _value is None and _instance.agg_method != UPPAggrSelector.MAX:
            raise ValueError(
                f"Specified aggregation method, {_instance.agg_method} requires a recapture specification."
            )

    agg_method: UPPAggrSelector = field(
        kw_only=True,
        default=UPPAggrSelector.MAX,
        validator=validators.instance_of(UPPAggrSelector),
    )
    """
    Method for aggregating the distinct diversion ratio measures for the two products.

    Distinct diversion ratio or GUPPI measures for the two merging-firms' products are
    aggregated using the method specified by the `agg_method` attribute, which is specified
    using the enum :class:`mergeron.UPPAggrSelector`.

    """

    precision: int = field(
        kw_only=False, default=5, validator=validators.instance_of(int)
    )
    """
    The number of decimal places of precision for the estimated area under the UPP boundary.

    Leaving this attribute unspecified will result in the default precision,
    which varies based on the `agg_method` attribute, reflecting
    the limit of precision available from the underlying functions. The number of
    boundary points generated is also defined based on this attribute.

    """

    coordinates: ArrayDouble = field(init=False, kw_only=True)
    """Market-share pairs as Cartesian coordinates of points on the diversion ratio boundary."""

    area: float = field(init=False, kw_only=True)
    """Area under the diversion ratio boundary."""

    def __attrs_post_init__(self, /) -> None:
        _share_ratio = critical_share_ratio(
            self.diversion_ratio, r_bar=self.recapture_ratio
        )
        _upp_agg_kwargs: gbfn.ShareRatioBoundaryKeywords = {
            "recapture_form": getattr(self.recapture_form, "value", "inside-out"),
            "dps": self.precision,
        }

        match self.agg_method:
            case UPPAggrSelector.DIS:
                _upp_agg_fn = gbfn.shrratio_boundary_wtd_avg
                _upp_agg_kwargs |= {"agg_method": "distance", "weighting": None}
            case UPPAggrSelector.AVG:
                _upp_agg_fn = gbfn.shrratio_boundary_xact_avg  # type: ignore
            case UPPAggrSelector.MAX:
                _upp_agg_fn = gbfn.shrratio_boundary_max  # type: ignore
                _upp_agg_kwargs = {"dps": 10}  # replace here
            case UPPAggrSelector.MIN:
                _upp_agg_fn = gbfn.shrratio_boundary_min  # type: ignore
                _upp_agg_kwargs |= {"dps": 10}  # update here
            case _:
                _upp_agg_fn = gbfn.shrratio_boundary_wtd_avg

                _aggregator: Literal["arithmetic mean", "geometric mean", "distance"]
                if self.agg_method.value.endswith("average"):
                    _aggregator = "arithmetic mean"
                elif self.agg_method.value.endswith("geometric mean"):
                    _aggregator = "geometric mean"
                else:
                    _aggregator = "distance"

                _wgt_type: Literal["cross-product-share", "own-share", None]
                if self.agg_method.value.startswith("cross-product-share"):
                    _wgt_type = "cross-product-share"
                elif self.agg_method.value.startswith("own-share"):
                    _wgt_type = "own-share"
                else:
                    _wgt_type = None

                _upp_agg_kwargs |= {"agg_method": _aggregator, "weighting": _wgt_type}

        _boundary = _upp_agg_fn(_share_ratio, self.recapture_ratio, **_upp_agg_kwargs)
        object.__setattr__(self, "coordinates", _boundary.coordinates)
        object.__setattr__(self, "area", _boundary.area)


def guppi_from_delta(
    _delta_bound: float = 0.01,
    /,
    *,
    m_star: float = 1.00,
    r_bar: float = DEFAULT_REC_RATIO,
) -> decimal.Decimal:
    """
    Translate ∆HHI bound to GUPPI bound.

    Parameters
    ----------
    _delta_bound
        Specified ∆HHI bound.
    m_star
        Parametric price-cost margin.
    r_bar
        Default recapture ratio.

    Returns
    -------
        GUPPI bound corresponding to ∆HHI bound, at given margin and recapture ratio.

    """
    return gbfn.round_cust(
        m_star * r_bar * (_s_m := np.sqrt(_delta_bound / 2)) / (1 - _s_m),
        frac=0.005,
        rounding_mode="ROUND_HALF_DOWN",
    )


def critical_share_ratio(
    _guppi_bound: float | decimal.Decimal = 0.075,
    /,
    *,
    m_star: float = 1.00,
    r_bar: float = 1.00,
    frac: float = 1e-16,
) -> decimal.Decimal:
    """
    Corollary to GUPPI bound.

    Parameters
    ----------
    _guppi_bound
        Specified GUPPI bound.
    m_star
        Parametric price-cost margin.
    r_bar
        Default recapture ratio.

    Returns
    -------
        Critical share ratio (share ratio bound) corresponding to the GUPPI bound
        for given margin and recapture ratio.

    """
    return gbfn.round_cust(
        mpf(f"{_guppi_bound}") / mp.fmul(f"{m_star}", f"{r_bar}"), frac=frac
    )


def share_from_guppi(
    _guppi_bound: float | decimal.Decimal = 0.065,
    /,
    *,
    m_star: float = 1.00,
    r_bar: float = DEFAULT_REC_RATIO,
) -> decimal.Decimal:
    """
    Symmetric-firm share for given GUPPI, margin, and recapture ratio.

    Parameters
    ----------
    _guppi_bound
        GUPPI bound.
    m_star
        Parametric price-cost margin.
    r_bar
        Default recapture ratio.

    Returns
    -------
    float
        Symmetric firm market share on GUPPI boundary, for given margin and
        recapture ratio.

    """

    return gbfn.round_cust(
        (_d0 := critical_share_ratio(_guppi_bound, m_star=m_star, r_bar=r_bar))
        / (1 + _d0)
    )


if __name__ == "__main__":
    print(
        "This module defines classes with methods for generating boundaries for concentration and diversion-ratio screens."
    )
