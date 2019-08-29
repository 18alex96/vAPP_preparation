import numpy as np
from astropy.coordinates import EarthLocation
from astropy.time import Time
from scipy.ndimage import rotate


class Target(object):
    def __init__(self,
                 name,
                 sky_coords,
                 position_angle,
                 separation,
                 delta_mag):
        self.name = name
        self.sky_coords = sky_coords
        self.position_anlge = position_angle
        self.separation = separation
        self.delta_mag = delta_mag

    @staticmethod
    def from_simbad(simbad_name,
                    position_angle,
                    separation,
                    delta_mag):
        sky_coords = 0.  # TODO add Simbad lookup
        return Target(simbad_name, sky_coords, position_angle, separation, delta_mag)

    @staticmethod
    def from_library(name):
        # TODO add library lookup
        sky_coords = 0.
        position_angle = 0.
        separation = 0.
        delta_mag = 0.
        return Target(name, sky_coords, position_angle, separation, delta_mag)


class Observation(object):
    def __init__(self, instrument, vAPP, target, time, wavelength):
        self.instrument = instrument
        self.vAPP = vAPP
        self.target = target
        self.time = time
        self.wavelength = wavelength

    @property
    def is_in_dark_zone(self):
        pass

    @property
    def elevation(self):
        pass

    @property
    def parallactic_angle(self):
        # Get sideral time in hours
        sid_time = self.sidereal_time

        # Convert to degrees
        sid_time_deg = sid_time * 15.

        # Calculate hour angle in degrees
        hour_angle = sid_time_deg - self.target.sky_coords.ra.value

        # conversion to radians:
        hour_angle_rad = np.deg2rad(hour_angle)
        dec_rad = np.deg2rad(self.target.sky_coords.dec.value)
        lat_rad = np.deg2rad(self.instrument.location.lat.value)

        p_angle = np.arctan2(np.sin(hour_angle_rad),
                             (np.cos(dec_rad) * np.tan(lat_rad) - np.sin(dec_rad) * np.cos(hour_angle_rad)))

        return np.rad2deg(p_angle)

    @property
    def sidereal_time(self):
        t = Time(str(self.time),
                 location=self.instrument.location)

        return t.sidereal_time("apparent").value

    @property
    def azimuth(self):
        pass

    @property
    def airmass(self):
        pass

    def get_simulated_image(self):
        pass


class Instrument(object):
    def __init__(self,
                 name,
                 location=None,
                 vAPPs=None,
                 plate_scale=None,
                 derotator_offset=0,
                 manual_offset=0):
        self.name = name
        self.location = location
        self.vAPPs = vAPPs
        self.plate_scale = plate_scale
        self.derotator_offset = derotator_offset
        self.manual_offset = manual_offset

    @staticmethod
    def from_library(self, name):
        # TODO add library lookup
        location = 0.
        vAPP = 0.
        plate_scale = 0.
        derotator_offset = 0.
        return Instrument(name, location, vAPP, plate_scale, derotator_offset)

    def observe(self, target, vAPP_name, time, wavelength):
        return Observation(self, target, vAPP, time, wavelength)


class vAPP(object):
    def __init__(self,
                 name,
                 pupil,
                 phase_pattern,
                 retardance,
                 wavelength_range,
                 pattern_rotation=0):
        self.name = name
        self.pupil = pupil
        self.phase_pattern = phase_pattern
        self.retardance = retardance
        self.wavelength_range = wavelength_range
        self.pattern_rotation = pattern_rotation

        # TODO calcualte these positions? necessary for plot
        self.psf_pos_1 = (62, 119)
        self.psf_pos_2 = (140, 84)

    def is_in_dark_zone(self, coords):
        # do calculation
        pass


class Instrument_old(object):
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
        elif self.m_instrument_name == "LBT":
            instrument_lon = -109.889064
            instrument_lat = 32.701308
        else:
            raise ValueError("Instrument should be either \'MagAO\', \'CHARIS\', or \'LBT\'")

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
        elif self.m_instrument_name == "LBT":
            model_psf = model_psf
            psf_pos_1 = (140, 232)
            psf_pos_2 = (140, 48)
        else:
            raise ValueError("Instrument should be either \'MagAO\', \'CHARIS\', or \'LBT\'")

        return model_psf, psf_pos_1, psf_pos_2

    def _load_platescale(self):

        if self.m_instrument_name == "MagAO":
            platescale = 0.016
        elif self.m_instrument_name == "CHARIS":
            platescale = 0.015
        elif self.m_instrument_name == "LBT":
            platescale = 0.0107
        else:
            raise ValueError("Instrument should be either \'MagAO\', \'CHARIS\', or \'LBT\'")

        return platescale

    def _load_instrument_offsets(self):

        if self.m_instrument_name == "MagAO":
            rot_off = 180. + 1.8
        elif self.m_instrument_name == "CHARIS":
            rot_off = -113.
        elif self.m_instrument_name == "LBT":
            rot_off = 0.
        else:
            raise ValueError("Instrument should be either \'MagAO\', \'CHARIS\', or \'LBT\'")

        return rot_off

    def add_target(self,
                   target_name,
                   target_ra,
                   target_dec,
                   target_position_angle,
                   target_separation):

        self.m_target_name = target_name
        self.m_target_ra = target_ra
        self.m_target_dec = target_dec
        self.m_target_position_angle = target_position_angle
        self.m_target_separation = target_separation

    def add_night(self,
                  time_start,
                  time_end,
                  steps=10):

        self.m_time_start = time_start
        self.m_time_end = time_end
        self.m_steps = steps

    def _get_parang(self,
                    time):

        t = Time(str(time),
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
