# testing the preparation tool
from astropy.coordinates import SkyCoord, EarthLocation

from core import Instrument, Target, Observation, vAPP
from plotting import plot_observation

# test case PZ Tel with MagAO
instrument = "MagAO"
target_name = "PZ Tel"
target_ra = 283.2745823348121
target_dec = -50.180895227015526
target_position_angle = 59.51
target_separation = .483
extra_rot = 25.
time_start = "2018-04-30T10:39:05"
time_end = "2018-04-30T10:49:52"
steps = 1

# # test case Theta 1 Ori B with MagAO
# instrument = "MagAO"
# target_name = "Theta 1 Ori B"
# target_ra = 83.8172304825278
# target_dec = -5.385212405087185
# target_position_angle = 254.9
# target_separation = .942
# extra_rot = 40.394
# time_start = "2017-02-07T01:04:52"
# time_end = "2017-02-07T01:24:52"
# steps = 1
#
# # test case MWC147 B  with CHARIS
# instrument = "CHARIS"
# target_name = "MWC147 B"
# target_ra = 98.27161713047708
# target_dec = 10.322204804583185
# target_position_angle = 50.
# target_separation = .15
# extra_rot = 0.
# time_start = "2019-02-26T06:44:00.0"
# time_end = "2019-02-26T07:32:00.0"
# steps = 2
#
# # test case OMI AND  with CHARIS
# instrument = "CHARIS"
# target_name = "OMI AND"
# target_ra = 345.4803811016596
# target_dec = 42.32598647381438
# target_position_angle = 180.
# target_separation = .228
# extra_rot = 0.
# time_start = "2018-06-25T13:45:40.869"
# time_end = "2018-06-25T13:47:40.869"
# steps = 1
#
# # test case HD87646
# instrument = "LBT"
# target_name = "HD87646"
# target_ra = 151.66954349925743
# target_dec = 17.894979480419554
# target_position_angle = 70
# target_separation = .400
# extra_rot = 0.
# time_start = "2019-04-18T23:00:00"
# time_end = "2019-04-19T04:01:00"
# steps = 5

# # test case HD164509
# instrument = "LBT"
# target_name = "HD164509"
# target_ra = 270.38008109724024
# target_dec = 0.10446853146386421
# target_position_angle = 202.5
# target_separation = .700
# extra_rot = 0.
# time_start = "2019-05-17T07:40:00"
# time_end = "2019-05-17T09:41:00"
# steps = 6

# # test case Kepler 21
# instrument = "LBT"
# target_name = "Kepler21"
# target_ra = 287.36196731685897
# target_dec = 38.71413838052882
# target_position_angle = 129.74
# target_separation = 0.7671
# extra_rot = 0.
# time_start = "2019-04-21T11:31:25"
# time_end = "2019-04-21T12:20:00"
# steps = 2

# instrument = Instrument(instrument_name=instrument,
#                         extra_rot=extra_rot)
#
# instrument.add_target(target_name=target_name,
#                       target_ra=target_ra,
#                       target_dec=target_dec,
#                       target_position_angle=target_position_angle,
#                       target_separation=target_separation)
#
# instrument.add_night(time_start=time_start,
#                      time_end=time_end,
#                      steps=steps)
#
# instrument.plot_object_position()

# test case HD206893
instrument = "CHARIS"
instrument_lon = -155.476667
instrument_lat = 19.825556
plate_scale = 0.015
vAPPs = ["180"]
rot_off = -113.

target_name = "HD206893"
target_ra = 326.34168735931195
target_dec = -12.783352171281424
target_position_angle = 65
target_separation = 0.257
extra_rot = 0.
time_start = "2019-05-17T10:40:00"
time_end = "2019-05-17T12:10:00"
steps = 5

target = Target(name=target_name,
                sky_coords=SkyCoord(target_ra, target_dec, unit="deg"),
                position_angle=target_position_angle,
                separation=target_separation,
                delta_mag=None)

instrument = Instrument(name=instrument,
                        location=EarthLocation(lon=instrument_lon,
                                               lat=instrument_lat),
                        vAPPs=vAPPs,
                        plate_scale=plate_scale,
                        derotator_offset=rot_off)

vAPP = vAPP(name="180",
            pupil=None,
            phase_pattern=None,
            retardance=None,
            wavelength_range=None,
            pattern_rotation=None)

observation = Observation(instrument=instrument,
                          vAPP=vAPP,
                          target=target,
                          time=time_start,
                          wavelength=None)

print(observation.parallactic_angle)

plot_observation(observation=observation)
