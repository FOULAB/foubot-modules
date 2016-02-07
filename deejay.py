from ibid.plugins import Processor, match
from ibid.utils import human_join

try:
    import json
except ImportError:
    import simplejson as json 

import urllib2


features = {}

features['deejay'] = {
    'description': u'Get current playing song on the foulab music player.',
    'categories': ('fun',),
}

class Deejay(Processor):
    usage = u'!dj'
    
    features = ('deejay',)
    
    addressed = False
    
    def get_title(self):
        stream_data = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_stream_title"}
        track_data = {"jsonrpc": "2.0", "id": 1, "method": "core.playback.get_current_track"}
        
        req = urllib2.Request('http://melody.lan:6680/mopidy/rpc')
        req.add_header('Content-Type', 'application/json')
        
        #Try first requesting for stream song info
        try:
            response = urllib2.urlopen(req, json.dumps(stream_data))
        except urllib2.URLError, e:
            return u'Melody is currently not available.'
        result = response.read()
        response.close()
        
        result = json.loads(result)

        #Check for track title if stream info empty
        if result['result'] == None:
            del(req)
            del(response)
        
            req = urllib2.Request('http://melody.lan:6680/mopidy/rpc')
            req.add_header('Content-Type', 'application/json')

            try:
                response = urllib2.urlopen(req, json.dumps(track_data))
            except urllib2.URLError, e:
                return u'Melody is currently not available.'
            result = response.read()
            response.close()
        
            result = json.loads(result)

            if result['result'] == None:
                return u'Nothing is currently playing.' 
    
            result = result['result']['name']
            return u'Curently playing: %s' % result
        else: 
            result = result['result']
            return u'Curently playing: %s' % result

        return u'Well this is embarassing...'

    @match(r'^!dj$')
    def dj_playing(self, event):
        response = self.get_title()
        event.addresponse(response)
