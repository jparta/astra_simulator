# -*- coding: utf-8 -*-
# @Author: p-chambers
# @Date:   2017-05-18 17:55:28
# @Last Modified by:   p-chambers
# @Last Modified time: 2017-05-18 18:15:48
from pathlib import Path
import shutil

if __name__ == "__main__":
    import os
    import sys
    from datetime import datetime, timedelta
    sys.path.append(os.path.abspath('../astra'))
    from astra.simulator import flight, forecastEnvironment
    from examples.example_utils import rmtree_error_handler_disregard_file_not_found

    # Environment parameters
    # Launch site: Daytona Beach, FL
    #        time: tomorrow, this time
    environment_params = {
        "launchSiteLat": 29.2108,
        "launchSiteLon": -81.0228,
        "launchSiteElev": 4,
        "launchTime": datetime.now() + timedelta(days=1),
        "forceNonHD": True,
        "debugging": True,
    }

    # Output directory in this directory
    output_path = Path(__file__).parent / 'outputs'
    outputPath = output_path / 'astra_output_cutdown'
    shutil.rmtree(outputPath, onerror=rmtree_error_handler_disregard_file_not_found)

    # Flight parameters
    flight_params = {
        'balloonGasType': 'Helium',
        'balloonModel': 'TA100',
        'nozzleLift': 0.6,                                # kg
        'payloadTrainWeight': 0.38,                    # kg
        'parachuteModel': 'SPH36',
        'numberOfSimRuns': 10,
        'trainEquivSphereDiam': 0.1,                    # m
        'cutdown': True,
        'cutdownAltitude': 14000,
        'excessPressureCoeff': 1,
        'outputPath': outputPath,
        'debugging': True,
        'log_to_file': False,
    }

    # Now, let's create a new environment object with the parameters we just read in.
    simEnvironment = forecastEnvironment(**environment_params)

    # Now, let's create a new flight object with the environment we just created.
    simFlight = flight(**flight_params, environment=simEnvironment)

    # The forecast download is automatically called by the flight object below.
    # However, if you'd like to download it in advance, uncomment the following line.
    # The flight object will automatically detect it and won't download the forecast twice.
    # simEnvironment.loadForecast()

    # Run the simulation
    simFlight.run()
