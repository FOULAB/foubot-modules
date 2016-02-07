from smbus import SMBus
from threading import Lock

# The SMBus library allows us to send a command byte plus 32 data bytes
# but the Arduino library will only receive 32 *total* bytes, *including*
# the command byte. So, limit payload to 31 bytes.
payLoadLen = 31
signAddress = 0x71

class LEDSign:
  def __init__( self ):
    self.s = SMBus(0)
    self.lock = Lock()

  def print_message( self, line, message ):
    if len( message ) > 255:
      message = message[:255]
    if message[:-1] != "\x00":
      message = ''.join([message, "\x00"])
    self.print_message_loop( line, message )


  def print_message_loop( self, line, message ):
    if message == "":
      return
    self.lock.acquire()
    self.s.write_i2c_block_data( signAddress, line, [ord(x) for x in message[0:payLoadLen]] )
    self.lock.release()
    self.print_message_loop( line, message[payLoadLen:] )

  def get_status( self ):
    self.lock.acquire()
    labStatus = self.s.read_byte( signAddress )
    self.lock.release()
    return labStatus
