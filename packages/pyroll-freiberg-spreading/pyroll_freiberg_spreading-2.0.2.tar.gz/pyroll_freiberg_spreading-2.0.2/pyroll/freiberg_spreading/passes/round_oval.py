from pyroll.core import RollPass
from .. import coefficients_lib


@RollPass.freiberg_spreading_velocity_coefficient
def freiberg_spreading_velocity_coefficient(self: RollPass):
    if "oval" in self.classifiers and "round" in self.in_profile.classifiers:
        return coefficients_lib.velocity_coefficient(
            self,
            a=0.02,
            b=0.985,
            n=-0.46,
            c=0.001,
            v_min=0.01,
            v_crit=1.5
        )


@RollPass.freiberg_spreading_roll_gap_ratio_coefficient
def freiberg_spreading_roll_gap_ratio_coefficient(self: RollPass):
    if "oval" in self.classifiers and "round" in self.in_profile.classifiers:
        return coefficients_lib.roll_gap_ratio_coefficient(
            self,
            a=0.8279,
            n=0.082
        )


@RollPass.freiberg_spreading_filling_coefficient
def freiberg_spreading_filling_coefficient(self: RollPass):
    if "oval" in self.classifiers and "round" in self.in_profile.classifiers:
        return coefficients_lib.filling_coefficient(
            self,
            a1=0.18444996,
            b1=0.83755,
            n1=5.6739714,
            a2=0,
            b2=1,
            n2=0,
        )


@RollPass.freiberg_spreading_diagonals_ratio_coefficient
def freiberg_spreading_diagonals_ratio_coefficient(self: RollPass):
    if "oval" in self.classifiers and "round" in self.in_profile.classifiers:
        return coefficients_lib.diagonals_ratio_coefficient(
            self,
            a=0.996,
            n=0.319
        )
