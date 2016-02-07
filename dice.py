from random import randint

from ibid.plugins import Processor, match
from ibid.utils import human_join

features = {}

features['dice'] = {
    'description': u'Throws multiple dice, or a single variable sided dice.',
    'categories': ('fun',),
}

class Dice(Processor):
    usage = u'roll <number> dice / !roll <number>'
    
    features = ('dice',)
    
    addressed = False
    
    @match(r'^!roll\s+(\d+)\s+dic?e$')
    def multithrow(self, event, number):
        number = int(number)
        throws = [unicode(randint(1, 6)) for i in range(number)]
        event.addresponse(u'I threw %s. Huzzah!', human_join(throws))

    @match(r'^!roll\s+(\d+)$', version='deaddressed')
    def combothrow(self, event, number):
        number = int(number)
        throw = unicode(randint(1, number))
        event.addresponse(u'GM says you gonna die...roll a D%(NUMBER)s! Rolled a %(THROW)s!', { 'NUMBER': unicode(number), 'THROW': throw,})
