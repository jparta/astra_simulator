# -*- coding: utf-8 -*-
# @Author: p-chambers
# @Date:   2017-04-21 17:21:23
# @Last Modified by:   p-chambers
# @Last Modified time: 2017-06-22 15:01:12
import os
import pytest
import re
import tempfile
from datetime import datetime, timedelta

from fastkml import kml
from geopy import distance as geopy_distance
from pygeoif.geometry import Point

import astra
from astra import flight
from astra.GFS import GFS_Handler
from astra.weather import forecastEnvironment

# Before importing numpy, disable multi-threading to ensure that the random
# number generator is not accessed from multiple threads. This is necessary
# because the order of random number accessing from different processes/threads
# could be different, which would cause the test to fail.
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
import numpy as np


def kml_close_enough(kml_orig_filepath: str, kml_newer_filepath: str, max_relative_error=5e-4):
    # From each KML file, find features with Name = 'Balloon Launch'
    # and extract the coordinates of each such feature
    # get coordinates from a kml Point object

    def get_sim_coords(kml_object: kml.KML) -> tuple[Point, dict[int, Point]]:
        launch = None
        landings = {}
        level_0_features = list(kml_object.features())
        features_to_check = level_0_features
        while features_to_check:
            feature = features_to_check.pop()
            if isinstance(feature, kml.Document):
                child_features = list(feature.features())
                features_to_check.extend(child_features)
            if isinstance(feature, kml.Placemark):
                if feature.name is None:
                    continue
                if feature.name == 'Balloon Launch':
                    launch = feature.geometry
                    if not isinstance(launch, Point):
                        raise ValueError('Balloon Launch feature is not a Point')
                elif feature.name.startswith('Payload landing (Simulation'):
                    sim_num = int(re.search(r'\d+', feature.name).group())
                    landing = feature.geometry
                    if not isinstance(landing, Point):
                        raise ValueError('Payload landing feature is not a Point')
                    landings[sim_num] = landing
        if launch is None:
            raise ValueError('KML file does not contain a Balloon Launch feature')
        return launch, landings


    with open(kml_orig_filepath, "rb") as f:
        kml_orig = kml.KML()
        kml_orig.from_string(f.read())
    with open(kml_newer_filepath, "rb") as f:
        kml_newer = kml.KML()
        kml_newer.from_string(f.read())

    launch_orig, landings_orig = get_sim_coords(kml_orig)
    launch_newer, landings_newer = get_sim_coords(kml_newer)
    launch_orig_lat_lon = (launch_orig.y, launch_orig.x)
    launch_newer_lat_lon = (launch_newer.y, launch_newer.x)

    # Check that the launch coordinates are the same
    if launch_orig.wkt != launch_newer.wkt:
        return False
    
    # For each flight, calculate the distance from the launch point to the
    # landing point. If the relative error between the two distances is less
    # than max_relative_error, then the two flights are considered to be
    # similar enough.
    for sim_num, landing_orig in landings_orig.items():
        landing_newer = landings_newer[sim_num]
        landing_orig_lat_lon = (landing_orig.y, landing_orig.x)
        landing_newer_lat_lon = (landing_newer.y, landing_newer.x)
        dist_orig = geopy_distance.distance(landing_orig_lat_lon, launch_orig_lat_lon).km
        dist_newer = geopy_distance.distance(landing_newer_lat_lon, launch_newer_lat_lon).km
        relative_error = abs(dist_orig - dist_newer) / dist_orig
        if relative_error > max_relative_error:
            return False
    return True
            

@pytest.fixture(params=[
  # These parameters are designed to break the code - hopefully no one makes
  # balloons with these names, or uses a heavier than air lifting gas (SF6)
    ('balloonModel', 'MYMADEUPBALLOON'),
    ('baloonGasType', 'SF6'),
    ('parachuteModel', 'RandomChuteModelX'),
    ('nozzleLift', 0.01),    # This is much smaller than the Payload weight
    ('simEnvironment', None),

])
def example_inputs(request):
    """Initializes a standard set of inputs to the flight class and injects
    a requested incorrect value input to check that errors are raised
    appropriately"""
    launch_datetime = datetime.now() + timedelta(days=1)
    # simEnvironment = forecastEnvironment(launchSiteLat=29.2108,      # deg
    #                                      launchSiteLon=-81.0228,     # deg
    #                                      launchSiteElev=4,           # m
    #                                      dateAndTime=launch_datetime,
    #                                      forceNonHD=True,
    #                                      debugging=True)
    output_dir = os.path.join(tempfile.gettempdir(), 'astra_output')

    inputs = {'environment': None,
              'balloonGasType': 'Helium',
              'balloonModel': 'TA800',
              'nozzleLift': 1,                            # kg
              'payloadTrainWeight': 0.433,                    # kg
              'parachuteModel': 'SPH36',
              'trainEquivSphereDiam': 0.1,
              'outputFile': output_dir}
    inputs[request.param[0]] = request.param[1] 
    return inputs


def test_forecast_example_inputs():
    """Note: this test is extremely minimal, and only checks if a solution is
    similar to a previous result.

    This test may also fail if parallelisation is used (which may be in the
    case in MKL versions of numpy), since the order of random number accessing
    from different processes/threads could be different.
    """
    np.random.seed(42)     # This should not be changed
    launch_datetime = datetime(2017, 4, 24,hour=12,minute=15)
    simEnvironment = forecastEnvironment(launchSiteLat=29.2108,      # deg
                                         launchSiteLon=-81.0228,     # deg
                                         launchSiteElev=4,           # m
                                         dateAndTime=launch_datetime,
                                         UTC_offset=-4,
                                         forceNonHD=True,
                                         debugging=True)

    # Set up the example input data files (from 24/04/2017, Daytona Beach)
    fileDict = {}
    for paramName in GFS_Handler.weatherParameters.keys():
        fileDict[paramName] = os.path.join(os.path.dirname(astra.__file__),
            '../test/example_data',
            'gfs_0p50_06z.ascii?{}[12:15][0:46][231:245][545:571]'.format(paramName))


    simEnvironment.loadFromNOAAFiles(fileDict)

    output_dir = tempfile.mktemp(suffix='')

    inputs = {'environment': simEnvironment,
              'balloonGasType': 'Helium',
              'balloonModel': 'TA800',
              'nozzleLift': 1,                  # kg
              'payloadTrainWeight': 0.433,      # kg
              'parachuteModel': 'SPH36',
              'trainEquivSphereDiam': 0.1,
              'outputFile': output_dir}
    simFlight = flight(**inputs)
    simFlight.run()

    test_fname = os.path.join(output_dir, 'out.kml')
    assert(os.path.isfile(test_fname))

    # check that the kml is a close match to the reference solution
    reference_fname = os.path.join(os.path.dirname(__file__), 'example_data/expected_output/out.kml')
    assert(kml_close_enough(test_fname, reference_fname))


def test_invalid_inputs(example_inputs):
    inputs = example_inputs
    with pytest.raises(Exception) as e_info:
        simFlight = flight(**inputs)
        simFlight.preflight()
