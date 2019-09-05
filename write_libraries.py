from core import Instrument, Target
from astropy.coordinates import EarthLocation

pds70 = Target.from_simbad('PDS70', 170, 0.180, 0)
pds70.write_to_library()

psd70_copy = Target.from_library('pdS70')
print(EarthLocation.get_site_names())

magao = Instrument('MagAO', 'las campanas observatory', ['MagAO_vAPP'], 0.0016, 180 + 1.8, 0)
magao.write_to_library()

magao_copy = Instrument.from_library('magao')
print(magao_copy.location.lat)
