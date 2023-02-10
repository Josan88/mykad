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

def trim_string(out, in_, count):
    out[:] = in_[:count].strip()
    return out
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
    print(hex(sw1))
except CardServiceStoppedException as e:
    print(f"Error sending the SELECT_JPN command: {e}")
    
# check response
if sw1 != 0x61:
    print("Not MyKad")
    

# app response
CMD_APP_RESPONSE = [0x00, 0xC0, 0x00, 0x00, sw2]
try:
    data, sw1, sw2 = connection.transmit(CMD_APP_RESPONSE)
    print(toHexString(data))
except CardServiceStoppedException as e:
    print(f"Error sending the GET_RESPONSE command: {e}")

def split(split_offset, split_length):
            TxBuffer = CMD_SET_LENGTH
            TxBuffer += split_length.to_bytes(2, byteorder='little')
            TxBuffer = toHexString(TxBuffer)
            TxBuffer = toBytes(TxBuffer)
            # set length
            try:
                data, sw1, sw2 = connection.transmit(TxBuffer[:10])
                print(hex(sw1))
            except CardServiceStoppedException as e:
                print(f"Error sending the SET_LENGTH command: {e}")

            one = 1
            TxBuffer = CMD_SELECT_FILE
            TxBuffer += FileNum.to_bytes(2, byteorder='little')
            TxBuffer += one.to_bytes(2, byteorder='little')
            TxBuffer += split_offset.to_bytes(2, byteorder='little')
            TxBuffer += split_length.to_bytes(2, byteorder='little')
            # select file
            try:
                data, sw1, sw2 = connection.transmit(TxBuffer[:13])
                print(hex(sw1))
            except CardServiceStoppedException as e:
                print(f"Error sending the SELECT_FILE command: {e}")
            ##################
            TxBuffer = CMD_GET_DATA + list(split_length.to_bytes(1, byteorder='little'))
            print(toHexString(TxBuffer))

            try:
                data, sw1, sw2 = connection.transmit(TxBuffer)
                print(toASCIIString(data))
            except CardServiceStoppedException as e:
                print(f"Error sending the GET_DATA command: {e}")
                
################################################################
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
            i = 0
            TxBuffer = bytearray(CMD_SET_LENGTH[:8])
            TxBuffer += split_length.to_bytes(2, byteorder='big')
            print(list(TxBuffer))
            data, sw1, sw2 = connection.transmit(list(TxBuffer))
################################ here
            i = 0
            for j in range(5):
                TxBuffer[i] = CMD_SELECT_FILE[j]
                i += 1
            TxBuffer[i:i+2] = struct.pack("<h", FileNum)
            i += 2
            TxBuffer[i:i+2] = struct.pack("<h", 1)
            i += 2
            TxBuffer[i:i+2] = struct.pack("<h", split_offset)
            i += 2
            TxBuffer[i:i+2] = struct.pack("<h", split_length)
            i += 2
            data, sw1, sw2 = connection.transmit(list(TxBuffer))

            i = 0
            for j in range(4):
                TxBuffer[i] = CMD_GET_DATA[j]
                i += 1
            TxBuffer[i] = split_length & 0xff
            i += 1
            data, sw1, sw2 = connection.transmit(list(TxBuffer))
            
            outfile.write(data[0:dLength-2])
            if FileNum == 2:
                if split_offset == 0:
                    out2file.write(data[3:dLength-5])
                else:
                    out2file.write(data[0:dLength-2])
                    
            if FileNum == 1 and split_offset == 0:
                TxBuffer = trim_string(RxBuffer[0x03:0x03+0x28])
                print("\nName:           %s" % TxBuffer)
            
                    
                    
        