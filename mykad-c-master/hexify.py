import binascii

def read():
    with open('jpn1', 'rb') as f:
        chunks = iter(lambda: f.read(32), b'')
        hexlines = map(binascii.hexlify, chunks)
        yield hexlines
    
    
for value in read():
    List = list(value)
    for num in range(len(List)):
        quote_h = List[num]
        quote = quote_h.decode()
        quote = binascii.a2b_hex("%s" % (quote.strip())).decode("ASCII").replace(';', '\n- ')
        print(quote.replace('  ', '')+'\n')
    
    
