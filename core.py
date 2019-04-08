import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from matplotlib import pyplot as plt
from photutils import CircularAperture
from scipy.ndimage import rotate


class Instrument():

    def __init__(self,
                 instrument_name,
                 extra_rot=0.):

        self.m_instrument_name = instrument_name
        self.m_extra_rot = extra_rot
        self.m_model_psf, self.m_psf_pos_1, self.m_psf_pos_2 = self._load_psf_model()
        self.m_platescale = self._load_platescale()
        self.m_instrument_lon, self.m_instrument_lat = self._load_instrument_location()
        self.m_rot_off = self._load_instrument_offsets()

    def _load_instrument_location(self):

        if self.m_instrument_name == "MagAO":
            instrument_lon = -70.6917
            instrument_lat = -29.015
        elif self.m_instrument_name == "CHARIS":
            instrument_lon = -155.476667
            instrument_lat = 19.825556
        else:
            raise ValueError("Instrument should be either \'MagAO\' or \'CHARIS\'")

        return instrument_lon, instrument_lat

    def _load_psf_model(self):

        path = "./data/%s_model.npy" % (self.m_instrument_name)
        model_psf = np.load(path)

        if self.m_instrument_name == "MagAO":
            model_psf = rotate(model_psf, angle=-26, reshape=False)
            psf_pos_1 = (110, 476)
            psf_pos_2 = (262, 160)
        elif self.m_instrument_name == "CHARIS":
            model_psf = model_psf[11,]
            psf_pos_1 = (62, 119)
            psf_pos_2 = (140, 84)
        else:
            raise ValueError("Instrument should be either \'MagAO\' or \'CHARIS\'")

        return model_psf, psf_pos_1, psf_pos_2

    def _load_platescale(self):

        if self.m_instrument_name == "MagAO":
            platescale = 0.016
        elif self.m_instrument_name == "CHARIS":
            platescale = 0.015
        else:
            raise ValueError("Instrument should be either \'MagAO\' or \'CHARIS\'")

        return platescale

    def _load_instrument_offsets(self):

        if self.m_instrument_name == "MagAO":
            rot_off = 180. + 1.8
        elif self.m_instrument_name == "CHARIS":
            rot_off = -113
        else:
            raise ValueError("Instrument should be either \'MagAO\' or \'CHARIS\'")

        return rot_off

    def add_target(self,
                   target_ra,
                   target_dec,
                   target_position_angle,
                   target_separation):

        self.m_target_ra = target_ra
        self.m_target_dec = target_dec
        self.m_target_position_angle = target_position_angle
        self.m_target_separation = target_separation

    def add_night(self,
                  date,
                  time_start,
                  time_end,
                  steps=10):

        self.m_date = date
        self.m_time_start = time_start
        self.m_time_end = time_end
        self.m_steps = steps

    def _get_parang(self,
                    time):

        t = Time(str(time).decode('utf-8'),
                 location=EarthLocation(lon=self.m_instrument_lon,
                                        lat=self.m_instrument_lat))

        # Get sideral time in hours
        sid_time = t.sidereal_time("apparent").value

        # Convert to degrees
        sid_time_deg = sid_time * 15.

        # Calculate hour angle in degrees
        hour_angle = sid_time_deg - self.m_target_ra

        # conversion to radians:
        hour_angle_rad = np.deg2rad(hour_angle)
        dec_rad = np.deg2rad(self.m_target_dec)
        lat_rad = np.deg2rad(self.m_instrument_lat)

        p_angle = np.arctan2(np.sin(hour_angle_rad),
                             (np.cos(dec_rad) * np.tan(lat_rad) - np.sin(dec_rad) * np.cos(hour_angle_rad)))

        return np.rad2deg(p_angle)

    def plot_object_position(self):

        # get aperture angles for all times
        date_start = "%sT%s" % (self.m_date, self.m_time_start)
        date_end = "%sT%s" % (self.m_date, self.m_time_end)
        step = int(np.round((Time(date_end) - Time(date_start)).value * 24 * 60 / self.m_steps))

        dates = np.arange(start=date_start,
                          stop=date_end,
                          step=step,
                          dtype="datetime64[m]")

        self.m_parangs = np.array([])

        for date in dates:
            self.m_parangs = np.append(self.m_parangs,
                                       self._get_parang(date))

        # Apply telescope specific corrections and add position angle of source
        self.m_parangs = self.m_target_position_angle + self.m_rot_off - (self.m_extra_rot + self.m_parangs)

        aperture_1 = CircularAperture(positions=self.m_psf_pos_1,
                                      r=self.m_target_separation / self.m_platescale)

        aperture_2 = CircularAperture(positions=self.m_psf_pos_2,
                                      r=self.m_target_separation / self.m_platescale)

        aperture_positions_1 = self.m_psf_pos_1 + self.m_target_separation / self.m_platescale * \
                               np.array([-np.sin(np.deg2rad(self.m_parangs)),
                                         np.cos(np.deg2rad(self.m_parangs))]).T

        aperture_positions_2 = self.m_psf_pos_2 + self.m_target_separation / self.m_platescale * \
                               np.array([-np.sin(np.deg2rad(self.m_parangs)),
                                         np.cos(np.deg2rad(self.m_parangs))]).T

        fig, ax = plt.subplots()

        ax.imshow(np.log(self.m_model_psf),
                  origin="lower")
        aperture_1.plot(color="white")
        aperture_2.plot(color="white")
        plt.plot(aperture_positions_1[:, 0], aperture_positions_1[:, 1], "r.")
        plt.plot(aperture_positions_2[:, 0], aperture_positions_2[:, 1], "r.")
        for i, tmp_pos in enumerate(aperture_positions_1):
            ax.annotate(i,
                        xy=tmp_pos,
                        xytext=(10 * -np.sin(np.deg2rad(self.m_parangs[i])),
                                np.cos(np.deg2rad(self.m_parangs[i]))),
                        textcoords='offset points',
                        fontsize=8,
                        color="red",
                        zorder=5)

            ax.annotate(i,
                        xy=(aperture_positions_2[i, 0], aperture_positions_2[i, 1]),
                        xytext=(10 * -np.sin(np.deg2rad(self.m_parangs[i])),
                                np.cos(np.deg2rad(self.m_parangs[i]))),
                        textcoords='offset points',
                        fontsize=8,
                        color="red",
                        zorder=5)

        ax.legend(loc=0)

        plt.show()
