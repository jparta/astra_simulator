"""
example_forecast.py
ASTRA High Altitude Balloon Flight Planner

DESCRIPTION
--------------

Example: Forecast based Simulation

University of Southampton
Niccolo' Zapponi, nz1g10@soton.ac.uk, 22/04/2013
"""
import logging
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from astra.simulator import flight, forecastEnvironment

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    np.random.seed(62)

    # Environment parameters
    # Launch site: Prime Meridian landmark in London
    #        time: tomorrow, this time
    launch_datetime = datetime.now() + timedelta(days=1)
    simEnvironment = forecastEnvironment(launchSiteLat=51.4779,      # deg
                                         launchSiteLon=0.0014,     # deg
                                         launchSiteElev=4,           # m
                                         launchTime=launch_datetime,
                                         forceNonHD=True,
                                         debugging=True)

    output_path = Path(__file__).parent / 'outputs'
    outputPath = output_path / 'astra_output_GM'

    # Launch setup
    simFlight = flight(environment=simEnvironment,
                       balloonGasType='Helium',
                       balloonModel='TA800',
                       nozzleLift=1,                                # kg
                       payloadTrainWeight=0.433,                    # kg
                       parachuteModel='SPH36',
                       numberOfSimRuns=10,
                       trainEquivSphereDiam=0.1,                    # m
                       floatingFlight=False,
                       excessPressureCoeff=1,
                       outputPath=outputPath,
                       debugging=True,
                       log_to_file=True)


    # simFlight.maxFlightTime = 5*60*60

    # Run the simulation
    simFlight.run()
