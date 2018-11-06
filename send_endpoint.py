import requests

ENDPOINT = 'http://flask-api-indoor-localization-dev.us-west-2.elasticbeanstalk.com/logtodb/'

def send_endpoint(ts, ap, device_mac, signal_strength, ssid):
    try:
        requests.post(ENDPOINT, data={'ts': ts, 'ap': ap, 'device_mac': device_mac, 'signal_strength': signal_strength, 'ssid': ssid})
    except:
        pass