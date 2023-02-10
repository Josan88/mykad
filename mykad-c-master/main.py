from smartcard.scard import *
from smartcard.pcsc import PCSCExceptions
from smartcard.util import *
import struct
from smartcard.Exceptions import NoCardException, CardRequestTimeoutException, CardConnectionException, CardServiceStoppedException
from smartcard.System import readers


CMD_SELECT_APP_JPN = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0xA0, 0x00, 0x00, 0x00, 0x74, 0x4A, 0x50, 0x4E, 0x00, 0x10]
CMD_APP_RESPONSE = [0x00, 0xC0, 0x00, 0x00, 0x05]
CMD_SET_LENGTH = [0xC8, 0x32, 0x00, 0x00, 0x05, 0x08, 0x00, 0x00]
CMD_SELECT_FILE = [0xCC, 0x00, 0x00, 0x00, 0x08]
CMD_GET_DATA = [0xCC, 0x06, 0x00, 0x00]
fileLengths = [0, 459, 4011, 1227, 171, 43, 43, 0]
RxBuffer = bytearray(256)
TxBuffer = bytearray(64)
HEX = 2
COMMA = 8
dLength=256

def TrimString(out, in_, count):
    i = count - 1
    while i >= 0 and in_[i] == 0x20:
        i -= 1
    j = 0
    while j < i + 1:
        out[j] = in_[j]
        j += 1
    out[j] = 0
    
def date_string(out, in_):
    out[:] = f"{in_[0:2]}/{in_[2:4]}/{in_[4:8]}"
    return out
def postcode_string(out, in_):
    out[:] = f"{in_[0:5]}-{in_[5:8]}"
    return out

try:
    r=readers()
    print(r)
    connection = r[0].createConnection()
    connection.connect()
except IndexError:
    print("No smart card readers found")
    
except CardConnectionException as e:
    print(f"Error connecting to the card: {e}")

except NoCardException:
    print("Smart card not connected")
    


# select JPN application
try:
    data, sw1, sw2 = connection.transmit(CMD_SELECT_APP_JPN)
except CardServiceStoppedException as e:
    print(f"Error sending the SELECT_JPN command: {e}")
    
# check response
if sw1 != 0x61:
    print("Not MyKad")
    

# app response
CMD_APP_RESPONSE = [0x00, 0xC0, 0x00, 0x00, sw2]
try:
    data, sw1, sw2 = connection.transmit(CMD_APP_RESPONSE)
except CardServiceStoppedException as e:
    print(f"Error sending the GET_RESPONSE command: {e}")

# check response
for FileNum in range(1, len(fileLengths)):
    if fileLengths[FileNum]:
        print("Reading JPN file {}".format(FileNum))
        RxBuffer = "jpn{}".format(FileNum)
        outfile = open(RxBuffer, "wb+")
        if (FileNum == 2):
            out2file = open("photo.jpg", "wb+")
        split_length = 252
        split_offset = 0
        for split_offset in range(0, fileLengths[FileNum], split_length):
            print(".", end="")
            if split_offset + split_length > fileLengths[FileNum]:
                split_length = fileLengths[FileNum] - split_offset
            # set length
            TxBuffer = bytearray(CMD_SET_LENGTH[:8])
            TxBuffer += split_length.to_bytes(2, byteorder='little')
            data, sw1, sw2 = connection.transmit(list(TxBuffer))
            
            # select file
            one = 1
            TxBuffer = bytearray(CMD_SELECT_FILE[:5])
            TxBuffer += FileNum.to_bytes(2, byteorder='little')
            TxBuffer += one.to_bytes(2, byteorder='little')
            TxBuffer += split_offset.to_bytes(2, byteorder='little')
            TxBuffer += split_length.to_bytes(2, byteorder='little')
            data, sw1, sw2 = connection.transmit(list(TxBuffer))
            
            # get data
            TxBuffer = bytearray(CMD_GET_DATA[:4])
            TxBuffer += split_length.to_bytes(1, byteorder='little')
            data, sw1, sw2 = connection.transmit(list(TxBuffer))
            data = bytes(data)
            outfile.write(data[:dLength-2])
            if FileNum == 2:
                if split_offset == 0:
                    out2file.write(data[3:dLength-5])
                else:
                    out2file.write(data[:dLength-2])
        print("\n")
        outfile.close()
        if FileNum == 2:
            out2file.close()
            
            