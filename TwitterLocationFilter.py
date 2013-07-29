# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from twython import Twython
APP_KEY = ''
APP_SECRET = ''
OAUTH_TOKEN  =  ''
OAUTH_TOKEN_SECRET = ''    

# <codecell>

#Only the south west and north east coner matter
#Broader scope
#Latitude, Longitude
#51.518918,-0.076518
#Latitude, Longitude
#51.523591,-0.066133


from twython import TwythonStreamer
#io library for streaming data to a file
import io
import json
#twitter stream filter takes a polygon with southwest corner first , coordinates in geoJSON so (long, lat)
brick_lane_polygon ='-0.076518,51.518918,-0.066133,51.523591'

class MyStreamer(TwythonStreamer):
    def __init__(self, *kargs, **kwargs):
        self.f = open('brickLaneStream.log', 'a')
        TwythonStreamer.__init__(self, *kargs, **kwargs)
    def on_success(self, data):
        if 'text' in data:
            txt_val = json.dumps(data)
            self.f.write(txt_val.decode('utf-8') + '\n')
            print "Sending to file:", data['text'].encode('utf-8')
        elif 'warning' in data:
            self.f.write(json.dumps(data).encode('utf-8') + '\n')
            
    def on_error(self, status_code, data):
        self.f.write('ERROR: code: {0} - message: {1}\n'.format(status_code, data))


if __name__ == '__main__':
    stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

    stream.statuses.filter(locations=brick_lane_polygon)

# <codecell>


# <codecell>


