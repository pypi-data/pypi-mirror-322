import numpy as np

from pyroll.core import RollPass, Profile


def filling_coefficient(
        roll_pass: RollPass,
        a1: float,
        b1: float,
        n1: float,
        a2: float,
        b2: float,
        n2: float,
):
    filling_ratio = roll_pass.out_profile.filling_ratio

    return min(
        a1 * filling_ratio ** n1 + b1,
        a2 * filling_ratio ** n2 + b2
    )


def roll_gap_ratio_coefficient(
        roll_pass: RollPass,
        a,
        n
):
    return a * (roll_pass.roll.nominal_radius / roll_pass.height) ** n


def tension_coefficient(
        roll_pass: RollPass,
        a,
        b
):
    if roll_pass.velocity < roll_pass.tension_less_velocity:
        c = a
    else:
        c = b
    return 1 - c * (roll_pass.velocity - roll_pass.tension_less_velocity) / roll_pass.tension_less_velocity


def velocity_coefficient(
        roll_pass: RollPass,
        a,
        b,
        c,
        n,
        v_min,
        v_crit,
):
    if roll_pass.velocity < v_crit:
        return a * ((roll_pass.velocity - v_min)) ** n + b

    return 1 - c * (roll_pass.velocity - v_crit)


def diagonals_ratio_coefficient(
        roll_pass: RollPass,
        a,
        n
):
    profile_diagonals_ratio = roll_pass.in_profile.width / roll_pass.in_profile.height
    profile_diagonals_ratio = profile_diagonals_ratio if profile_diagonals_ratio > 1 else 1 / profile_diagonals_ratio
    pass_diagonals_ratio = roll_pass.roll.groove.usable_width / roll_pass.height
    pass_diagonals_ratio = pass_diagonals_ratio if pass_diagonals_ratio > 1 else 1 / pass_diagonals_ratio
    diagonals_ratio = profile_diagonals_ratio if profile_diagonals_ratio > pass_diagonals_ratio else pass_diagonals_ratio
    return a * diagonals_ratio ** n


def temperature_coefficient_low_alloyed(
        profile: Profile,
        a,
        b,
):
    return a + b * (profile.temperature - 273.15)


def temperature_coefficient_high_alloyed(
        profile: Profile,
        a,
        b,
        c,
):
    return a * np.exp(b * (profile.temperature - 273.15)) + c
