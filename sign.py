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
               "SIGN"    : "beep -f1 -l150 -r3 -d250".split(),
               "EMPIRE"  : "beep -l350 -f39.2 -D100 -n -l350 -f39.2 -D100 -n -l350 -f39.2 -D100 -n -l250 -f31.1 -D100 -n -l25 -f46.6 -D100 -n -l350 -f39.2 -D100 -n -l250 -f31.1 -D100 -n -l25 -f46.6 -D100 -n -l700 -f39.2 -D100".split(),
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

      topic_parts[ pos ] = " Lab status: open " if status else " Lab status: closed "
        
      event.addresponse( u"//".join( topic_parts ), topic = True, target = lab_channel, address = False, source = u"freenode" )

      self.old_status = status
      
      if status == 0:
        p = subprocess.Popen(beepdisc["EMPIRE"])
        p.wait()
