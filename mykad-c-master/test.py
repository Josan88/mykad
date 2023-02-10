import smartcard.System
from smartcard.Exceptions import NoCardException, CardRequestTimeoutException, CardConnectionException, CardServiceStoppedException
from smartcard.util import toHexString, toBytes

CMD_SELECT_APP_JPN = [0x00, 0xA4, 0x04, 0x00, 0x0A, 0x0A0, 0x00, 0x00, 0x00, 0x74, 0x4A, 0x50, 0x4E, 0x00, 0x10]
# CMD_APP_RESPONSE = [0x00, 0xC0, 0x00, 0x00, 0x05]
CMD_SET_LENGTH = [0xC8, 0x32, 0x00, 0x00, 0x05, 0x08, 0x00, 0x00]
CMD_SELECT_FILE = [0xCC, 0x00, 0x00, 0x00, 0x08]
CMD_GET_DATA = [0xCC, 0x06, 0x00, 0x00]

def read_mykad_card():
    # connect to the first available smart card reader
    try:
        reader = smartcard.System.readers()[0]
        connection = reader.createConnection()
        connection.connect()
    except IndexError:
        print("No smart card readers found")
        return
    except CardConnectionException as e:
        print(f"Error connecting to the card: {e}")
        return

    # select JPN application
    try:
        data, sw1, sw2 = connection.transmit(CMD_SELECT_APP_JPN)
    except CardServiceStoppedException as e:
        print(f"Error sending the SELECT_JPN command: {e}")
        return

    # check response
    if sw1 != 0x61:
        print("Not MyKad")
        return

    # app response
    CMD_APP_RESPONSE = [0x00, 0xC0, 0x00, 0x00, sw2]
    try:
        data, sw1, sw2 = connection.transmit(CMD_APP_RESPONSE)
    except CardServiceStoppedException as e:
        print(f"Error sending the GET_RESPONSE command: {e}")
        return
    
    # set length
    try:
        data, sw1, sw2 = connection.transmit(CMD_SET_LENGTH)
    except CardServiceStoppedException as e:
        print(f"Error sending the SET_LENGTH command: {e}")
        return
    
    # select file
    try:
        data, sw1, sw2 = connection.transmit(CMD_SELECT_FILE)
    except CardServiceStoppedException as e:
        print(f"Error sending the SELECT_FILE command: {e}")
        return

    # get data
    try:
        data, sw1, sw2 = connection.transmit(CMD_GET_DATA)
    except CardServiceStoppedException as e:
        print(f"Error sending the GET_DATA command: {e}")
        return
    
    # retrieve the data
    result = {}
    result["card_number"] = toHexString(data[0:10])
    result["full_name"] = toHexString(data[10:10+30])
    result["birth_date"] = toHexString(data[40:40+7])
    result["gender"] = toHexString(data[47:47+1])
    result["citizenship"] = toHexString(data[48:48+1])
    result["address"] = toHexString(data[49:49+60])
    result["postcode"] = toHexString(data[109:109+5])
    result["state"] = toHexString(data[114:114+2])

    print(result)

if __name__ == "__main__":
    try:
        read_mykad_card()
    except NoCardException as e:
        print(f"No card found: {e}")
    except CardRequestTimeoutException as e:
        print(f"Timeout while requesting the card: {e}")


try:
    reader = smartcard.System.readers()[0]
    connection = reader.createConnection()
    connection.connect()
    # CMD_GET_DATA = toHexString(CMD_GET_DATA)
    # CMD_GET_DATA = toBytes(CMD_GET_DATA)
    # print(CMD_GET_DATA)
    data, sw1, sw2 = connection.transmit([200, 50, 0, 0, 5, 8, 0, 0, 0, 252, 0, 207, 0, 252])
except IndexError:
    print("No smart card readers found")
except CardConnectionException as e:
    print(f"Error connecting to the card: {e}")
    