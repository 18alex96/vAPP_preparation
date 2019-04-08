# testing the preparation tool
from core import Instrument

# test case PZ Tel with MagAO
instrument = "MagAO"
target_ra = 283.2745823348121
target_dec = -50.180895227015526
target_position_angle = 59.51
target_separation = .483
extra_rot = 25.
date = "2018-04-30"
time_start = "10:39:05"
time_end = "10:49:52"
steps = 1

# # test case Theta 1 Ori B with MagAO
# instrument = "MagAO"
# target_ra = 83.8172304825278
# target_dec = -5.385212405087185
# target_position_angle = 254.9
# target_separation = .942
# extra_rot = 40.394
# date = "2017-02-07"
# time_start = "01:04:52"
# time_end = "01:24:52"
# steps = 1
#
# # test case MWC147 B  with CHARIS
# instrument = "CHARIS"
# target_ra = 98.27161713047708
# target_dec = 10.322204804583185
# target_position_angle = 50.
# target_separation = .15
# extra_rot = 0.
# date = "2019-02-26"
# time_start = "06:44:00.0"
# time_end = "07:32:00.0"
# steps = 5
#
# # test case OMI AND  with CHARIS
# instrument = "CHARIS"
# target_ra = 345.4803811016596
# target_dec = 42.32598647381438
# target_position_angle = 180.
# target_separation = .228
# extra_rot = 0.
# date = "2018-06-25"
# time_start = "13:45:40.869"
# time_end = "13:47:40.869"
# steps = 1

instrument = Instrument(instrument_name=instrument,
                        extra_rot=extra_rot)

instrument.add_target(target_ra=target_ra,
                      target_dec=target_dec,
                      target_position_angle=target_position_angle,
                      target_separation=target_separation)

instrument.add_night(date=date,
                     time_start=time_start,
                     time_end=time_end,
                     steps=steps)

instrument.plot_object_position()
