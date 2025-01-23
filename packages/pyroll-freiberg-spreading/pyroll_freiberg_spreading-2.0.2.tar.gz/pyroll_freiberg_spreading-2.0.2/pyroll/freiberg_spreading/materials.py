from pyroll.core import Profile

from .coefficients_lib import temperature_coefficient_high_alloyed


def is_material(profile: Profile, materials: set[str]):
    if isinstance(profile.material, str):
        return profile.material.lower() in materials
    return materials.intersection([m.lower() for m in profile.material])


@Profile.freiberg_spreading_material_coefficient
def m_backup(self):
    return 1


@Profile.freiberg_spreading_temperature_coefficient
def t_backup(self):
    return 1


@Profile.freiberg_spreading_material_coefficient
def m_c20(self: Profile):
    if is_material(self, {"c20", "c22"}):
        return 1


@Profile.freiberg_spreading_temperature_coefficient
def t_c20(self: Profile):
    if is_material(self, {"c20", "c22"}):
        return temperature_coefficient_high_alloyed(self, a=-1.47e-5, b=7.108e-3, c=1.0216)


@Profile.freiberg_spreading_material_coefficient
def m_c45(self: Profile):
    if is_material(self, {"c45"}):
        return 1


@Profile.freiberg_spreading_temperature_coefficient
def t_c45(self: Profile):
    if is_material(self, {"c45"}):
        return temperature_coefficient_high_alloyed(self, a=-1.47e-5, b=7.108e-3, c=1.0216)


@Profile.freiberg_spreading_material_coefficient
def m_s355j2(self: Profile):
    if is_material(self, {"s355j2"}):
        return 1


@Profile.freiberg_spreading_temperature_coefficient
def t_s355j2(self: Profile):
    if is_material(self, {"s355j2"}):
        return temperature_coefficient_high_alloyed(self, a=-1.47e-5, b=7.108e-3, c=1.0216)
