from ibid.plugins import Processor, match, periodic, handler
import ibid.source.irc
import ibid
import subprocess
import os

features = {'discobeep': {
  'description': u'Signals across the tubes.',
  'categories': ('fun',),
}}

beepdisc = {
               "PINGU"   : "beep -f50 -r2 -l200 -n -f40 -r2".split(),
               "FANTASY" : "beep -f49 -l53 -D53 -n -f49 -l53 -D53 -n -f49 -l53 -D53 -n -f49 -l428 -n -f39 -l428 -n -f44 -l428 -n -f49 -l107 -D214 -n -f44 -l107 -n -f49 -l857".split(),
               "EMPIRE"  : "beep -l350 -f39.2 -D100 -n -l350 -f39.2 -D100 -n -l350 -f39.2 -D100 -n -l250 -f31.1 -D100 -n -l25 -f46.6 -D100 -n -l350 -f39.2 -D100 -n -l250 -f31.1 -D100 -n -l25 -f46.6 -D100 -n -l700 -f39.2 -D100".split(),
               "OCARINA" : "beep -l500 -f44 -n -l1000 -f29.5 -n -l500 -f35 -n -l500 -f44 -n -l1000 -f29.5 -n -l500 -f35 -n -l250 -f44 -n -l250 -f52 -n -l500 -f49 -n -l500 -f39 -n -l250 -f35.5 -n -l250 -f39 -n -l500 -f44 -n -l500 -f29 -n -l250 -f26 -n -l250 -f32.5 -n -l750 -f29".split(),
           }

class Disco( Processor ):

  usage = u'!disco <message>'

  feature = ('disco',)

  addressed = False

  def __beep( self, disc ):
    try:
      p = subprocess.Popen( disc, close_fds=True, 
                            stdout=None,
                            stderr=None,
                            stdin=None )
      p.wait()
    except Exception:
      pass

  @match(r'^!disco+\s(.*)$')
  def disco( self, event, disc ):
    self.__beep( beepdisc[ str(disc.capitalize()) ] )
    event.addresponse( True )
  
  @match(r'^!pingu$')
  def pingu( self, event ):
    self.__beep( beepdisc["PINGU"] )
    event.addresponse( True )

  @match(r'^!fantasy$')
  def fantasy( self, event ):
    self.__beep( beepdisc["FANTASY"] )
    event.addresponse( True )
  
  @match(r'^!empire$')
  def empire( self, event ):
    self.__beep( beepdisc["EMPIRE"] )
    event.addresponse( True )

  @match(r'^!ocarina$')
  def ocarina(self, event):
    self.__beep( beepdisc["OCARINA"] )
    event.addresponse( True )
