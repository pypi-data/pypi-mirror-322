import sys
from logging import getLogger

import numpy as np

from pyroll.core import RollPass, root_hooks, Unit
from . import coefficients_lib

_log = getLogger(__name__)


@RollPass.freiberg_spreading_tension_coefficient
def freiberg_spreading_tension_coefficient(self: RollPass):
    return coefficients_lib.tension_coefficient(
        self,
        a=0.76,
        b=0.12
    )


@RollPass.tension_less_velocity
def tension_less_velocity(self: RollPass):
    return self.velocity


@RollPass.OutProfile.width
def width(self: RollPass.OutProfile):
    if not self.has_set_or_cached("width"):
        return self.roll_pass.roll.groove.usable_width

    rp = self.roll_pass
    parts = np.array([
        rp.in_profile.freiberg_spreading_material_coefficient,
        rp.in_profile.freiberg_spreading_temperature_coefficient,
        rp.freiberg_spreading_tension_coefficient,
        rp.freiberg_spreading_roll_gap_ratio_coefficient,
        rp.freiberg_spreading_velocity_coefficient,
        rp.freiberg_spreading_diagonals_ratio_coefficient,
        rp.freiberg_spreading_filling_coefficient,
    ])

    if not np.all(parts):
        _log.warning(f"No Freiberg spreading coefficients available for {rp.label}")
        return None

    spread = np.prod(parts)

    _log.debug(f"Freiberg Spreading Coefficients for {rp.label}: {parts} => Product: {spread}")
    return spread * rp.in_profile.width
