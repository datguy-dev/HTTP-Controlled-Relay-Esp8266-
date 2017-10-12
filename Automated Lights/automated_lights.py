import datetime
import logging
import requests
import time
import os
import pyowm


logging.basicConfig(filename='/tmp/lights.log', level=logging.INFO)


def get_mode():
    # returns False for automatic and True for manual
    tmp_file = '/tmp/lights.state'
    if not os.path.isfile(tmp_file):
        with open(tmp_file, 'w') as f:
            f.write('automatic\n')
            logging.info('{0},{1}'.format(datetime.date.today(), 'created state file'))
        f.close()
        return False

    with open(tmp_file, 'r') as f:
        command = f.readline().strip()
        if len(command) > 0:
            if command == 'manual' or command == 'Manual':
                return True
            else:
                return False
        else:
            logging.info('{0},error,command:{1}'.format(datetime.date.today(), command))
            return False


def relay_control(switch):
    for i in range(10):
        req_state = requests.get('http://192.168.1.49?state')
        if req_state.status_code == 200:
            if len(req_state.text):
                try:
                    int(req_state.text)
                except:
                    return False
                break
        else:
            time.sleep(5)
    #
    if int(req_state.text) != switch:
        for i in range(10):
            req_state = requests.get('http://192.168.1.49?relay')
            if req_state.status_code == 200:
                if len(req_state.text):
                    try:
                        int(req_state.text)
                    except:
                        return False
                    if int(req_state.text) == switch:
                        return True
                    else:
                        return False
            else:
                time.sleep(5)
        return False
    else:
        return True


if not get_mode():
    owm_api_key = '000000000000000000000000000000000000' # Enter your open weather map api key
    omw_geo_cords = (0.0, 0.0) # Go to open weather map to find a locations geograhics latitude & longitude
    owm = pyowm.OWM(owm_api_key, subscription_type='free')
    if owm:
        obs = owm.weather_at_coords(omw_geo_cords[0], omw_geo_cords[1])
        w = obs.get_weather()

        sunset_time = int(w.get_sunset_time('iso')[11:13].replace('0', ''))
        sunrise_time = int(w.get_sunrise_time('iso')[11:13].replace('0', ''))

        hour = datetime.datetime.now().hour
        time_on1 = range(sunrise_time-3, 12) # Leeway time added to activate early
        time_on2 = range(sunset_time-5, 24)

        call = None
        if hour in time_on1 or hour in time_on2:
            call = relay_control(1)
        elif sunrise_time-3 <= hour <= sunset_time-5:
            condition = w.get_weather_icon_name()
            poor_conditions = ['04d', '04n', '09d', '09n', '10d', '10n', '11d', '11n']
            if condition in poor_conditions:
                call = relay_control(1)
        else:
            call = relay_control(0)

        if call:
            logging.info('automatic,{0},{1}'.format(datetime.date.today(), 'True'))
        else:
            logging.info('automatic,{0},{1}'.format(datetime.date.today(), 'False'))
else:
    logging.info('manual,{0},{1}'.format(datetime.date.today(), 'False'))
