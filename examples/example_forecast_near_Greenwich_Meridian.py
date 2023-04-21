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
from pathlib import Path
import numpy as np
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    from datetime import datetime, timedelta
    from astra.simulator import forecastEnvironment, flight

    np.random.seed(62)

    # Environment parameters
    # Launch site: Prime Meridian landmark in London
    #        time: tomorrow, this time
    launch_datetime = datetime.now() + timedelta(days=1)
    simEnvironment = forecastEnvironment(launchSiteLat=51.4779,      # deg
                                         launchSiteLon=0.0014,     # deg
                                         launchSiteElev=4,           # m
                                         dateAndTime=launch_datetime,
                                         UTC_offset=0,
                                         forceNonHD=True,
                                         debugging=True)

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
                       debugging=True,
                       log_to_file=True)

    output_path = Path(__file__).parent
    simFlight.outputFile = output_path / 'astra_output_GM'

    # simFlight.maxFlightTime = 5*60*60

    # Run the simulation
    simFlight.run()
