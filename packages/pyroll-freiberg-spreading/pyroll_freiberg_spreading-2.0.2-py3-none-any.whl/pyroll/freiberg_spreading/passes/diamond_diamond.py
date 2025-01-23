from pyroll.core import RollPass
from .. import coefficients_lib


@RollPass.freiberg_spreading_velocity_coefficient
def freiberg_spreading_velocity_coefficient(self: RollPass):
    if "diamond" in self.classifiers and "diamond" in self.in_profile.classifiers:
        return coefficients_lib.velocity_coefficient(
            self,
            a=-0.014,
            b=1.018,
            n=0.69,
            c=0.0024,
            v_min=0.09,
            v_crit=1.5
        )


@RollPass.freiberg_spreading_roll_gap_ratio_coefficient
def freiberg_spreading_roll_gap_ratio_coefficient(self: RollPass):
    if "diamond" in self.classifiers and "diamond" in self.in_profile.classifiers:
        return coefficients_lib.roll_gap_ratio_coefficient(
            self,
            a=0.911,
            n=0.058
        )


@RollPass.freiberg_spreading_filling_coefficient
def freiberg_spreading_filling_coefficient(self: RollPass):
    if "diamond" in self.classifiers and "diamond" in self.in_profile.classifiers:
        return coefficients_lib.filling_coefficient(
            self,
            a1=0.352,
            b1=0.662,
            n1=0.998,
            a2=0,
            b2=1,
            n2=0,
        )


@RollPass.freiberg_spreading_diagonals_ratio_coefficient
def freiberg_spreading_diagonals_ratio_coefficient(self: RollPass):
    if "diamond" in self.classifiers and "diamond" in self.in_profile.classifiers:
        return coefficients_lib.diagonals_ratio_coefficient(
            self,
            a=1.028,
            n=0.24
        )
