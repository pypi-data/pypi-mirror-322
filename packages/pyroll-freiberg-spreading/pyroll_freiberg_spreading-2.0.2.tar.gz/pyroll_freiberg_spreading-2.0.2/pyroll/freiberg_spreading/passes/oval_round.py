from pyroll.core import RollPass
from .. import coefficients_lib


@RollPass.freiberg_spreading_velocity_coefficient
def freiberg_spreading_velocity_coefficient(self: RollPass):
    if "round" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.velocity_coefficient(
            self,
            a=0.016,
            b=0.986,
            n=-0.35,
            c=0.001,
            v_min=0.01,
            v_crit=1.5
        )


@RollPass.freiberg_spreading_roll_gap_ratio_coefficient
def freiberg_spreading_roll_gap_ratio_coefficient(self: RollPass):
    if "round" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.roll_gap_ratio_coefficient(
            self,
            a=0.8317,
            n=0.08
        )


@RollPass.freiberg_spreading_filling_coefficient
def freiberg_spreading_filling_coefficient(self: RollPass):
    if "round" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.filling_coefficient(
            self,
            a1=0.19579019,
            b1=0.82420981,
            n1=5.1507655,
            a2=0,
            b2=1,
            n2=0,
        )


@RollPass.freiberg_spreading_diagonals_ratio_coefficient
def freiberg_spreading_diagonals_ratio_coefficient(self: RollPass):
    if "round" in self.classifiers and "oval" in self.in_profile.classifiers:
        return coefficients_lib.diagonals_ratio_coefficient(
            self,
            a=1.03,
            n=0.28
        )
