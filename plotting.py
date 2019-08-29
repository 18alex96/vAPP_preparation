import numpy as np
from matplotlib import pyplot as plt
from photutils import CircularAperture


def plot_observation(observation):
    # Calculate position angle on detector
    pa_on_detector = observation.target.position_anlge + observation.instrument.derotator_offset - (
            observation.instrument.manual_offset + observation.parallactic_angle)

    aperture_1 = CircularAperture(positions=observation.vAPP.psf_pos_1,
                                  r=observation.target.separation / observation.instrument.plate_scale)

    aperture_2 = CircularAperture(positions=observation.vAPP.psf_pos_2,
                                  r=observation.target.separation / observation.instrument.plate_scale)

    aperture_positions_1 = observation.vAPP.psf_pos_1 + observation.target.separation / observation.instrument.plate_scale * \
                           np.array([-np.sin(np.deg2rad(pa_on_detector)),
                                     np.cos(np.deg2rad(pa_on_detector))]).T

    aperture_positions_2 = observation.vAPP.psf_pos_2 + observation.target.separation / observation.instrument.plate_scale * \
                           np.array([-np.sin(np.deg2rad(pa_on_detector)),
                                     np.cos(np.deg2rad(pa_on_detector))]).T

    # TODO replace by vAPP model
    path = "./data/%s_model.npy" % (observation.instrument.name)
    model_psf = np.abs(np.load(path)[11,])

    # Plot
    fig, ax = plt.subplots()

    ax.imshow(np.log(model_psf), origin="lower")

    aperture_1.plot(color="white")
    aperture_2.plot(color="white")
    plt.plot(aperture_positions_1[0], aperture_positions_1[1], "r.")
    plt.plot(aperture_positions_2[0], aperture_positions_2[1], "r.")
    # ax.annotate(i,
    #             xy=tmp_pos,
    #             xytext=(10 * -np.sin(np.deg2rad(pa_on_detector[i])),
    #                     np.cos(np.deg2rad(pa_on_detector[i]))),
    #             textcoords='offset points',
    #             fontsize=8,
    #             color="red",
    #             zorder=5)
    #
    # ax.annotate(i,
    #             xy=(aperture_positions_2[i, 0], aperture_positions_2[i, 1]),
    #             xytext=(10 * -np.sin(np.deg2rad(pa_on_detector[i])),
    #                     np.cos(np.deg2rad(pa_on_detector[i]))),
    #             textcoords='offset points',
    #             fontsize=8,
    #             color="red",
    #             zorder=5)

    # ax.plot([], [], label=str(i) + ": " + str(dates[i])[-5:], linestyle="", color="r")

    # ax.set_title("%s, " % self.m_instrument_name + str(self.m_target_name) + ", " + str(dates[0])[:10])
    ax.set_title(f"{observation.instrument.name}, {observation.target.name}, {observation.time}")
    # leg = ax.legend(loc=0, frameon=True, labelspacing=1, title='Time [UT]', bbox_to_anchor=(1., 1.))
    # for text in leg.get_texts():
    #     plt.setp(text, color='red')

    plt.show()

# Plot several objects
#     def plot_object_position(self):
#
#         # get aperture angles for all times
#         step = int(np.round((Time(self.m_time_end) - Time(self.m_time_start)).value * 24 * 60 / self.m_steps))
#
#         dates = np.arange(start=self.m_time_start,
#                           stop=self.m_time_end,
#                           step=step,
#                           dtype="datetime64[m]")
#
#         print(dates)
#
#         self.m_parangs = np.array([])
#
#         for date in dates:
#             self.m_parangs = np.append(self.m_parangs,
#                                        self._get_parang(date))
#
#         # Apply telescope specific corrections and add position angle of source
#         self.m_parangs = self.m_target_position_angle + self.m_rot_off - (self.m_extra_rot + self.m_parangs)
#
#         aperture_1 = CircularAperture(positions=self.m_psf_pos_1,
#                                       r=self.m_target_separation / self.m_platescale)
#
#         aperture_2 = CircularAperture(positions=self.m_psf_pos_2,
#                                       r=self.m_target_separation / self.m_platescale)
#
#         aperture_positions_1 = self.m_psf_pos_1 + self.m_target_separation / self.m_platescale * \
#                                np.array([-np.sin(np.deg2rad(self.m_parangs)),
#                                          np.cos(np.deg2rad(self.m_parangs))]).T
#
#         aperture_positions_2 = self.m_psf_pos_2 + self.m_target_separation / self.m_platescale * \
#                                np.array([-np.sin(np.deg2rad(self.m_parangs)),
#                                          np.cos(np.deg2rad(self.m_parangs))]).T
#
#         fig, ax = plt.subplots()
#
#         if self.m_instrument_name == "LBT":
#             ax.imshow(np.sqrt(self.m_model_psf),
#                       origin="lower")
#         else:
#             ax.imshow(np.log(self.m_model_psf),
#                       origin="lower")
#         aperture_1.plot(color="white")
#         aperture_2.plot(color="white")
#         plt.plot(aperture_positions_1[:, 0], aperture_positions_1[:, 1], "r.")
#         plt.plot(aperture_positions_2[:, 0], aperture_positions_2[:, 1], "r.")
#         for i, tmp_pos in enumerate(aperture_positions_1):
#             ax.annotate(i,
#                         xy=tmp_pos,
#                         xytext=(10 * -np.sin(np.deg2rad(self.m_parangs[i])),
#                                 np.cos(np.deg2rad(self.m_parangs[i]))),
#                         textcoords='offset points',
#                         fontsize=8,
#                         color="red",
#                         zorder=5)
#
#             ax.annotate(i,
#                         xy=(aperture_positions_2[i, 0], aperture_positions_2[i, 1]),
#                         xytext=(10 * -np.sin(np.deg2rad(self.m_parangs[i])),
#                                 np.cos(np.deg2rad(self.m_parangs[i]))),
#                         textcoords='offset points',
#                         fontsize=8,
#                         color="red",
#                         zorder=5)
#
#             ax.plot([], [], label=str(i) + ": " + str(dates[i])[-5:], linestyle="", color="r")
#
#         ax.set_title("%s, " % self.m_instrument_name + str(self.m_target_name) + ", " + str(dates[0])[:10])
#         leg = ax.legend(loc=0, frameon=True, labelspacing=1, title='Time [UT]', bbox_to_anchor=(1., 1.))
#         for text in leg.get_texts():
#             plt.setp(text, color='red')
#
#         plt.show()
