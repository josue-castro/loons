import argparse
import numpy as np
from itur.models import itu838 as rain
from itur.models import itu840 as cloud
from itur.models import itu676 as gases
from modeling import free_space_loss, cloudfog_loss, precipitation_loss

parser = argparse.ArgumentParser(
    prog="rf-signals",
    description="This program is used to calculate specific attenuation of radio frequency signals due to "
                "FSPL, Precipitation, Fog/Cloud and Atmospheric Gases",
    epilog="Add epilog here",
    usage='Add usage here'
)
parser.add_argument('-f', '--frequency', type=float, help='Frequency of signal (GHz)')
parser.add_argument('-he', '--height', type=float, help='Transmitter height (Km)')
parser.add_argument('-ht', '--tropopause', type=float, help='Tropopause height at equator (Km)')
parser.add_argument('-dl', '--distance', type=float, help='Land distance from receiver to transmitter base (Km)')
parser.add_argument('-rr', '--rainrate', type=float, help='Rate of precipitation in (mm/h)')
parser.add_argument('-T', '--temperature', type=float, help='Average surface ambient temperature (K)')
parser.add_argument('-P', '--pressure', type=float, help='Average surface pressure (hPa) at the site')
parser.add_argument('-el', '--elevation', type=float, help='Elevation angle (degrees)')
parser.add_argument('-vwd', '--vdensity', type=float, help='Vapor water density (g/m3)')
parser.add_argument('-lwd', '--ldensity', type=float, help='Liquid water density (g/m3)')
parser.add_argument('-spw', '--signalpower', type=float, help='Signal power (dBm)')

args = parser.parse_args()

h = args.height  # Loon height, in km.
dl = args.distance  # Land distance from receiver to loon base
ht = args.tropopause  # Tropopause height at equator

hs = h-ht  # How high into the stratosphere is the loon
D = np.sqrt(h**2 + dl**2)  # Linear distance between loon and receiver
theta = np.arctan(dl/h)  # Angle between loon and receiver

# Linear distance the signal must propagate through the stratosphere
# Through this path, signal is only affected by FSPL
ds = hs/np.cos(theta)
print(ds)

# Linear distance the signal must propagate through the troposphere
# Through this path, signal is affected by:
#   1. FSPL
#   2. Rain attenuation
#   3. Atmospheric gas attenuation
#   4. Fog attenuation, etc
dt = D-ds
print(dt)

# FSPL
fspl_strat = free_space_loss(ds, args.frequency)
fspl_tropo = free_space_loss(dt, args.frequency)


# Propagation Loss Due to Rain
rain_att = precipitation_loss(args.rainrate, args.frequency, dt)
# rain.rain_specific_attenuation(args.rainrate, args.frequency, 0, 0))  # rain rate, frequency, elevation, polarization tilt angle relative to the horizontal


# Fog/Cloud loss
fog_att = cloudfog_loss(args.frequency, args.ldensity, args.temperature, dt)

# Atmospheric Gases
gas_att = gases.gaseous_attenuation_terrestrial_path(dt, args.frequency, 0, args.vdensity, args.pressure, args.temperature, 'exact')
# gases.gaseous_attenuation_slant_path()  # frequency, elevation, water vapor density, surface pressure (hPa), temperature


print(f"\nStratosphere Attenuation:\n"
      f"\tFSPL = {fspl_strat} dB")
print(f"Troposphere Attenuation:\n"
      f"\tFSPL = {fspl_tropo} dB\n"
      f"\tRain attenuation = {rain_att} dB\n"
      f"\tAtmospheric gas attenuation = {gas_att} \n"
      f"\tFog attenuation = {fog_att} dB")

