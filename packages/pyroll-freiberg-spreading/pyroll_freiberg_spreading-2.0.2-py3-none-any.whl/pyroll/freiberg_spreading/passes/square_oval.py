from pyroll.core import RollPass
from .. import coefficients_lib


@RollPass.freiberg_spreading_velocity_coefficient
def freiberg_spreading_velocity_coefficient(self: RollPass):
    if "oval" in self.classifiers and "square" in self.in_profile.classifiers:
        return coefficients_lib.velocity_coefficient(
            self,
            a=0.025,
            b=0.979,
            n=-0.47,
            c=0.0013,
            v_min=0.01,
            v_crit=1.5
        )


@RollPass.freiberg_spreading_roll_gap_ratio_coefficient
def freiberg_spreading_roll_gap_ratio_coefficient(self: RollPass):
    if "oval" in self.classifiers and "square" in self.in_profile.classifiers:
        return coefficients_lib.roll_gap_ratio_coefficient(
            self,
            a=0.7805,
            n=0.1076
        )


@RollPass.freiberg_spreading_filling_coefficient
def freiberg_spreading_filling_coefficient(self: RollPass):
    if "oval" in self.classifiers and "square" in self.in_profile.classifiers:
        return coefficients_lib.filling_coefficient(
            self,
            a1=0.131,
            b1=0.9001,
            n1=9.42,
            a2=0,
            b2=1,
            n2=0,
        )


@RollPass.freiberg_spreading_diagonals_ratio_coefficient
def freiberg_spreading_diagonals_ratio_coefficient(self: RollPass):
    if "oval" in self.classifiers and "square" in self.in_profile.classifiers:
        return coefficients_lib.diagonals_ratio_coefficient(
            self,
            a=1.03,
            n=0.38
        )
