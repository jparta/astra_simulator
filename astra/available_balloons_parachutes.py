# coding=utf-8

"""
This file contains key data of all the balloons currently supported by the
simulator.

Data in the available_baloons_parachutes.balloons dictionary is of the form:
    "BALLOON ID" : (weight in kg, nominal burst diameter in meters,
                    Weibull lambda, Weibull k)
Add new balloons by choosing Weibull lambda so that the mean of the distribution is proportional
to the nominal burst diameter, taking into account the meanToNominalBurstRatio defined below.
Test your equation against existing specifications to make sure it is correct.

Data in the available_balloons_parachutes.parachutes dictionary is of the form:
    {"CHUTE ID" : A_ref}

University of Southampton
"""
balloons = {
    # Totex
    "TA10": (0.01, 0.45, 0.5045, 14.3577),
    "TA20": (0.02, 0.7, 0.7848, 14.3577),
    "TA30": (0.03, 0.88, 0.9866, 14.3577),
    "TA45": (0.045, 1.1, 1.2333, 14.3577),
    "TA100": (0.1, 1.96, 2.1975, 14.3577),
    "TA200": (0.2, 3.0, 3.3636, 14.3577),
    "TA300": (0.3, 3.78, 4.2381, 14.3577),
    "TA350": (0.35, 4.12, 4.6193, 14.3577),
    "TA450": (0.45, 4.72, 5.2920, 14.3577),
    "TA500": (0.5, 4.99, 5.5947, 14.3577),
    "TA600": (0.6, 6.02, 6.7495, 14.3577),
    "TA700": (0.7, 6.53, 7.3213, 14.3577),
    "TA800": (0.8, 7.0, 7.8483, 14.3577),
    "TA1000": (1.0, 7.86, 8.8125, 14.3577),
    "TA1200": (1.2, 8.63, 9.6758, 14.3577),
    "TA1500": (1.5, 9.44, 10.5840, 14.3577),
    "TA2000": (2, 10.54, 11.8173, 14.3577),
    "TA3000": (3, 13.0, 14.5754, 14.3577),
    # Hwoyee
    "HW10": (0.01, 0.60, 0.6727, 14.3577),
    "HW30": (0.03, 1.00, 1.1212, 14.3577),
    "HW50": (0.05, 1.20, 1.3454, 14.3577),
    "HW100": (0.1, 1.80, 2.0181, 14.3577),
    "HW200": (0.2, 3.00, 3.3636, 14.3577),
    "HW300": (0.3, 3.80, 4.2605, 14.3577),
    "HW350": (0.35, 4.1, 4.5969, 14.3577),
    "HW400": (0.4, 4.50, 5.0453, 14.3577),
    "HW500": (0.5, 5.00, 5.6059, 14.3577),
    "HW600": (0.6, 5.80, 6.5029, 14.3577),
    "HW750": (0.75, 6.5, 7.2877, 14.3577),
    "HW800": (0.8, 6.80, 7.6241, 14.3577),
    "HW950": (0.95, 7.2, 8.0725, 14.3577),
    "HW1000": (1.0, 7.5, 8.4089, 14.3577),
    "HW1200": (1.2, 8.5, 9.5301, 14.3577),
    "HW1500": (1.5, 9.5, 10.6513, 14.3577),
    "HW1600": (1.6, 10.5, 11.7725, 14.3577),
    "HW2000": (2.0, 11.0, 12.3330, 14.3577),
    # Stratoflights (StratoFlights Balloon -> SFB, unofficial identifiers)
    "SFB800": (0.8, 7.5, 8.4088, 14.3577),  # article no. 100250
}
"""Balloon data.

Data is in the format: "BALLOON ID" : (weight, nominal burst diameter,
Weibull lambda, Weibull k)
"""

meanToNominalBurstRatio = 1.08116

parachutes = {
    "RCK3": 0.26615,
    "RCK4": 0.47315,
    "RCK5": 0.73930,
    "SPH36": 0.45,
    "SPH48": 0.84,
    "SPH54": 0.59883,
    "SPH60": 1.59,
    "SPH72": 2.14,
    "SPH100": 4.6,
    "TX5012": 0.69398,
    "TX160": 1.91134,
    # Stratoflights (StratoFlights Parachute -> SFP, unofficial identifiers)
    "SFP800": 0.55,  # article no. 100200, calculated for octagon with 0.88 m longest diagonal (constructed diameter)
    None: 0,
    "": 0
}
"""Parachute Data

Data is in the format: "CHUTE ID" : A_ref
A_ref is the projected area of the parachute in m^2.
"""
