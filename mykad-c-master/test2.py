fileLengths = [0, 459, 4011, 1227, 171, 43, 43, 0]
for FileNum in range(1, len(fileLengths)):
    if fileLengths[FileNum]:
        print("Reading JPN file {}".format(FileNum))
        RxBuffer = "jpn{}".format(FileNum)
        outfile = open(RxBuffer, "wb+")
        if FileNum == 2:
            out2file = open("photo.jpg", "wb+")
        split_length = 252
        for split_offset in range(0, fileLengths[FileNum], split_length):
            print(".", end="")
            if split_offset + split_length > fileLengths[FileNum]:
                split_length = fileLengths[FileNum] - split_offset
            for i in range(8):
                TxBuffer[i] = CmdSetLength[i]
            short_val = split_length
            TxBuffer[i:i+2] = short_val.to_bytes(2, byteorder='little')
            i += 2

https://www.d-logic.com/knowledge_base/search-download-sdk/