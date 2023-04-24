"""
Example Sounding based Simulation

ASTRA High Altitude Balloon Flight Planner

University of Southampton
"""
from datetime import datetime
from pathlib import Path
from astra.simulator import flight
from astra.weather import soundingEnvironment


if __name__ == "__main__":
    soundingFile = Path(__file__).parent / 'sp.sounding'

    simEnvironment = soundingEnvironment(launchSiteLat=50.2245,         # deg
                                         launchSiteLon=-5.3069,         # deg
                                         launchSiteElev=60,             # m
                                         distanceFromSounding=0,        # km
                                         timeFromSounding=3,            # hours
                                         inflationTemperature=10.5,     # degC
                                         launchTime=datetime.now(),
                                         soundingFile=soundingFile,
                                         debugging=True)
    # TODO: Add an example sounding file, with description of how to create one
    # simEnvironment.load()

    output_path = Path(__file__).parent / 'outputs'
    outputPath = output_path / 'astra_output_sounding'

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
                       floatingAltitude=30000,                      # m
                       excessPressureCoeff=1,
                       outputPath=outputPath,
                       debugging=True,
                       log_to_file=True)

    # Run the simulation
    simFlight.run()
