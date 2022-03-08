import matplotlib.font_manager as fm
from astroquery.simbad import Simbad
from astropy.coordinates import get_moon
from astropy.coordinates import get_sun
import re
import configparser
import matplotlib.dates as mdates
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy.time import Time, TimeISO
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt
from astropy.visualization import astropy_mpl_style, quantity_support
plt.style.use(astropy_mpl_style)
quantity_support()

font_path = './fonts/Libertinus-7.040/static/OTF/'
font_files = fm.findSystemFonts(fontpaths=font_path)
for font_file in font_files:
    fm.fontManager.addfont(font_file)
plt.rcParams['font.family'] = 'Libertinus Sans'
plt.rcParams['font.size'] = 13
plt.rcParams["font.weight"] = "bold"
plt.rcParams["axes.labelweight"] = "bold"
plt.rcParams["axes.titleweight"] = "bold"
plt.rcParams['savefig.bbox'] = 'tight'
plt.rcParams['savefig.pad_inches'] = 0.05

config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

class ISOCustom(TimeISO):
    name = 'iso_custom'
    subfmts = (('date_hms',
                '%Y-%m-%d %H:%M:%S',
                '{year:d}-{mon:02d}-{day:02d} {hour:02d}:{min:02d}:{sec:02d}'),
               ('date',
                '%Y-%m-%d',
                '{year:d}-{mon:02d}-{day:02d}'),
               ('midnight',
                '%Y-%m-%d 00:00:00',
                '{year:d}-{mon:02d}-{day:02d} 00:00:00'),
               ('h',
                '%H',
                '{hour:02d}'))


yunling = EarthLocation(lat=25.62*u.deg, lon=101.13*u.deg, height=2223*u.m)
utcoffset = 8*u.hour
web_root = '/var/www'
url_path = '/obs/yunling/'
folder_path = web_root+url_path
# folder_path = './test/'
website = config['WEBSITE']['WEBSITE_URL']

c_sky = '#dceaff'  # 220 234 255
c_civ = '#88a5d4'  # 136 165 212
c_nau = '#4673bc'  # 70 115 188
c_ast = '#213c66'  # 33 60 102
# 25 32 41 (platte comes from https://en.wikipedia.org/wiki/Twilight#/media/File:Twilight-dawn_subcategories.svg)
c_night = '#192029'


def ephemeris(obj_name, day_offset_str=None):
    points = 20*60+1
    try:
        obj = SkyCoord.from_name(obj_name)
    except:
        return '无法找到天体'
    result_table = Simbad.query_object(obj_name)
    time_loc = Time.now() + utcoffset  # local time (It is +8 zone here)
    # hour in local time
    h_loc = int(time_loc.to_value('iso_custom', subfmt='h'))
    midnight_loc = Time(time_loc.to_value('iso_custom', subfmt='midnight'))
    # calculate the midnight we wanted (in UTC)
    if day_offset_str != None:
        try:
            # get the midnigt of day_offset later
            day_offset = int(day_offset_str)
        except:
            return '请输入数字作为参数'
        time_loc = time_loc + day_offset*u.day
        if h_loc > 8:  # before 8am, get the midnight of previous day
            midnight = midnight_loc+(day_offset+1)*u.day-utcoffset
        else:
            midnight = midnight_loc+day_offset*u.day-utcoffset
    else:
        if h_loc > 8:
            midnight = midnight_loc+1*u.day-utcoffset
        else:
            midnight = midnight_loc-utcoffset

    delta_midnight = np.linspace(-10, 10, points)*u.hour
    times = midnight+delta_midnight
    times_loc = times+utcoffset
    frame = AltAz(obstime=times,
                  location=yunling)
    obj_altazs = obj.transform_to(frame)
    sun_altazs = get_sun(times).transform_to(frame)
    moon_altazs = get_moon(times).transform_to(frame)
    x_axis = np.array(times_loc.to_value('isot'), dtype='datetime64')

    fig, ax = plt.subplots(1, figsize=(6, 3))
    ax.plot(x_axis, moon_altazs.alt, color=[0.85]*3, ls='--', lw=1.5)
    ax.plot(x_axis, obj_altazs.alt, color='#C80815', lw=2)
    plt.fill_between(x_axis, 0*u.deg, 90*u.deg, color=c_sky, zorder=0)
    plt.fill_between(x_axis, 0*u.deg, 90*u.deg,
                     sun_altazs.alt < -0*u.deg, color=c_civ, zorder=0)
    plt.fill_between(x_axis, 0*u.deg, 90*u.deg,
                     sun_altazs.alt < -6*u.deg, color=c_nau, zorder=0)
    plt.fill_between(x_axis, 0*u.deg, 90*u.deg,
                     sun_altazs.alt < -12*u.deg, color=c_ast, zorder=0)
    plt.fill_between(x_axis, 0*u.deg, 90*u.deg,
                     sun_altazs.alt < -18*u.deg, color=c_night, zorder=0)

    ax.set_ylim(0, 90)
    ax.set_ylabel('')

    # the index of night period in time list
    night = np.where(sun_altazs.alt < -0*u.deg)[0]
    # 1.5hr before and after the night
    ax.set_xlim(x_axis[(night[0]-90)], x_axis[(night[-1]+90)])
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))
    ax.set_xlabel(time_loc.to_value('iso_custom', subfmt='date'))

    obj_simbad_str = re.sub(' +', ' ', result_table['MAIN_ID'][0])
    ax.set_title(obj_simbad_str+' (%s)' % (obj_name))

    # plt.tight_layout()
    save_path = folder_path+ '{}_{}.png'.format(obj_name, time_loc.to_value('iso_custom', subfmt='date'))
    fig.savefig(save_path,dpi=300)
    re_url = '[{} {}]({}{}{}_{}.png)'.format(obj_name, time_loc.to_value('iso_custom', subfmt='date'), website, url_path, obj_name, time_loc.to_value('iso_custom', subfmt='date'))
    return re_url


if __name__ == '__main__':
    print(ephemeris('M31'))
