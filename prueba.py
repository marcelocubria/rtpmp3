from bitstring import BitArray
import re

def takeFrame(bits, headerIndex):
    header = bits[headerIndex:headerIndex+32];
    print(header);
    frameSync = header[0:11];
    version = header[11:13];
    layer = header[13:15];
    protection = header[15];
    bitrate = header[16:20];
    sampling = header[20:22];
    padding = header[22];
    private = header[23];
    channel = header[24:26];
    modeext = header[26:28];
    copyright = header[28];
    original = header[29];
    emphasis = header[30:];

    print('proteccion: ' + protection);
    if (protection == 0): # Si hay CRC tras la cabecera, este ocupa 16 bits
        sideInfoIndex = headerIndex + 32;
    else:
        sideInfoIndex = headerIndex + 48;


    print("canales: " + channel);
    if (channel == 11): # Si el canal es mono, 17 bytes de side information
        sideInfo = bits[sideInfoIndex:sideInfoIndex+136];
        mainDataBegins = sideInfo[0:9];
    else: # Si no es mono, 32 bytes de side information
        sideInfo = bits[sideInfoIndex:sideInfoIndex+256];
        mainDataBegins = sideInfo[0:9];

    frameLength = int(144 * 8 * (224000/32000)) # 144 * bit rate / sample rate * 8 (el 144 es en bytes)

    # Mi backpointer indica desde donde van mis datos, y el siguiente backpointer
    # indica hasta donde llegan mis datos y empiezan el del siguiente

    print("backpointer: " + mainDataBegins)

    nextHeaderIndex = headerIndex + frameLength;
    print("nextheader: " + str(nextHeaderIndex))
    nextHeader = bits[nextHeaderIndex:nextHeaderIndex+32];
    nextProtection = nextHeader[15];
    nextChannel = nextHeader[24:26];
    if (nextProtection == 0): # Si hay CRC tras la cabecera, este ocupa 16 bits
        nextSideInfoIndex = nextHeaderIndex + 32;
    else:
        nextSideInfoIndex = nextHeaderIndex + 48;
    if (nextChannel == 11): # Si el canal es mono, 17 bytes de side information
        nextSideInfo = bits[nextSideInfoIndex:nextSideInfoIndex+136];
        nextMainDataBegins = nextSideInfo[0:9];
    else: # Si no es mono, 32 bytes de side information
        nextSideInfo = bits[nextSideInfoIndex:nextSideInfoIndex+256];
        nextMainDataBegins = nextSideInfo[0:9];

    intNextBackpointer = int(nextMainDataBegins, 2);
    print("next backpointer :" + str(intNextBackpointer))

    """deltaHeaders = nextHeaderIndex - headerIndex
    teoriaHeaderIndex = headerIndex + frameLength;
    teoriaHeader = bits[teoriaHeaderIndex:teoriaHeaderIndex+32]
    print("header 1 :" + header);
    print("header 2 :" + teoriaHeader);"""


if __name__== "__main__":
    with open ("archivo.mp3", "rb") as file: # Abro archivo en modo lectura y binario

        bytes = file.read();
        bits = BitArray(bytes).bin;
        headerIndex = bits.find('11111111111'); #buscamos la cabecera
        takeFrame(bits, headerIndex);

        #while byte: #byte = '' es false
            #hago algo con el byte
        #numero = int.from_bytes(byte, byteorder='big');
        #its = f'{numero:08b}' #convierte el numero a 8 bits
        #print(bits);
            #byte = file.read(1)
