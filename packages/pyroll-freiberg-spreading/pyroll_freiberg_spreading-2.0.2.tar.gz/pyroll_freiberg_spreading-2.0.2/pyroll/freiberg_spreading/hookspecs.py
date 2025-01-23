from pyroll.core import RollPass, Hook, Profile

Profile.freiberg_spreading_material_coefficient = Hook[float]()
"""Material cW coefficient for Freiberg spreading model."""

Profile.freiberg_spreading_temperature_coefficient = Hook[float]()
"""Temperature cθ coefficient for Freiberg spreading model."""

RollPass.freiberg_spreading_tension_coefficient = Hook[float]()

RollPass.freiberg_spreading_filling_coefficient = Hook[float]()

RollPass.freiberg_spreading_diagonals_ratio_coefficient = Hook[float]()

RollPass.freiberg_spreading_roll_gap_ratio_coefficient = Hook[float]()

RollPass.freiberg_spreading_velocity_coefficient = Hook[float]()

RollPass.tension_less_velocity = Hook[float]()
