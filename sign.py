from ibid.plugins import Processor, match, periodic, handler
import ibid.source.irc
import ibid
from ledsign import LEDSign
import subprocess
import datetime

features = {'sign': {
  'description': u'Displays messages on the Foulab LED sign.',
  'categories': ('message',),
}}

lab_channel = u"##foulab"

#Monkey patch topic tracking into the ibid Ircbot library
ibid.source.irc.Ircbot.topics = {}

def topicUpdated( self, user, channel, topic ):
  self.topics[ channel ] = topic
  print "Topic for %s is %s, set by %s" % ( channel, topic, user )

def get_topic( self, channel ):
  return self.topics[ channel ]

ibid.source.irc.Ircbot.topicUpdated = topicUpdated
ibid.source.irc.Ircbot.get_topic = get_topic

beepdisc = {
               "SIGN"    : "beep -f1 -l150 -r10 -d250".split(),
               "SECRET"  : "beep -l145 -f14.75 -n -l130 -f13.96 -n -l135 -f11.74 -n -l135 -f9.89 -n -l130 -f7.87 -n -l135 -f12.55 -n -l135 -f15.63 -n -l265 -f19.90".split(),
               "OCARINA" : "beep -l500 -f44 -n -l1000 -f29.5 -n -l500 -f35 -n -l500 -f44 -n -l1000 -f29.5 -n -l500 -f35 -n -l250 -f44 -n -l250 -f52 -n -l500 -f49 -n -l500 -f39 -n -l250 -f35.5 -n -l250 -f39 -n -l500 -f44 -n -l500 -f29 -n -l250 -f26 -n -l250 -f32.5 -n -l750 -f29".split(),
           }

class Sign( Processor ):

  usage = u'!sign <message>'

  feature = ('sign',)

  addressed = False

  old_status = 0

  def __init__( self, name ):
    Processor.__init__( self, name )
    self.s = LEDSign()

  @handler
  def handle( self, event ):
    print "I am handling this event: " + repr(event)

  @match(r'^!sign\s(.*)$', version='deaddressed')
  def sign( self, event, message ):
    try:
      p = subprocess.Popen( beepdisc["SIGN"] )
      p.wait()
      self.s.print_message( 0, ''.join(["From: ", event.sender['nick'], datetime.datetime.today().strftime(" %d%b %H:%m") ] ) )
      self.s.print_message( 1, message )
      event.addresponse( True )
    except Exception:
      event.addresponse( "I can't see the sign. Are you sure it's plugged in? Have you tried turning it off and on again?" )

  @match(r'^!status$')
  def status( self, event ):
    try:
      status = self.s.get_status()
      if status:
        event.addresponse("open")
      else:
        event.addresponse("closed")
    except Exception:
      event.addresponse( "I can't see the sign. Are you sure it's plugged in? Have you tried turning it off and on again?" )

  @periodic( interval = 1, initial_delay = 1 )
  def update_status( self, event ):
    
    status = self.s.get_status()

    if( status != self.old_status ):
      topic = ibid.sources['freenode'].proto.get_topic( lab_channel )
      topic_parts = topic.split( u"//" )
      topiclen = len( topic_parts )
      if topiclen >= 3 :
        pos = -2
      elif topiclen == 2 or topiclen == 1:
        pos = -1
      else:
        pos = 0
        topic_parts.append("")

      topic_parts[ pos ] = " Lab status: OPEN " if status else " Lab status: CLOSED "
        
      event.addresponse( u"//".join( topic_parts ), topic = True, target = lab_channel, address = False, source = u"freenode" )

      self.old_status = status
      
      alert = "SECRET" if status else "OCARINA" 

      p = subprocess.Popen(beepdisc[alert])
      p.wait()
