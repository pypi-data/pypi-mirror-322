from pyroll.core import RollPass
from .. import coefficients_lib


@RollPass.freiberg_spreading_velocity_coefficient
def freiberg_spreading_velocity_coefficient(self: RollPass):
    if "square" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.velocity_coefficient(
            self,
            a=0.016,
            b=0.986,
            n=-0.35,
            c=0.0013,
            v_min=0.01,
            v_crit=1.5
        )


@RollPass.freiberg_spreading_roll_gap_ratio_coefficient
def freiberg_spreading_roll_gap_ratio_coefficient(self: RollPass):
    if "square" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.roll_gap_ratio_coefficient(
            self,
            a=0.813,
            n=0.09
        )


@RollPass.freiberg_spreading_filling_coefficient
def freiberg_spreading_filling_coefficient(self: RollPass):
    if "square" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.filling_coefficient(
            self,
            a1=0.355,
            b1=0.65,
            n1=0.9989,
            a2=0,
            b2=1,
            n2=0,
        )


@RollPass.freiberg_spreading_diagonals_ratio_coefficient
def freiberg_spreading_diagonals_ratio_coefficient(self: RollPass):
    if "square" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.diagonals_ratio_coefficient(
            self,
            a=1.003,
            n=0.42
        )
