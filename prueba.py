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
        frameDataStarts = sideInfoIndex + 136;
    else: # Si no es mono, 32 bytes de side information
        sideInfo = bits[sideInfoIndex:sideInfoIndex+256];
        mainDataBegins = sideInfo[0:9];
        frameDataStarts = sideInfoIndex + 256;

    frameLength = int(144 * 8 * (224000/32000)) # 144 * bit rate / sample rate * 8 (el 144 es en bytes)
    #sale 8064

    # Mi backpointer indica desde donde van mis datos, y el siguiente backpointer
    # indica hasta donde llegan mis datos y empiezan el del siguiente

    intBackpointer = int(mainDataBegins, 2);
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

    if ((intBackpointer == 0) and (intNextBackpointer == 0)): #donde empiezan y acaban los datos de una trama ADU
        ADUDataStart = frameDataStarts
        ADUDataEnd = nextHeaderIndex
    elif ((intBackpointer == 0) and (intNextBackpointer != 0)):
        ADUDataStart = frameDataStarts
        ADUDataEnd = nextHeaderIndex - intNextBackpointer
    elif ((intBackpointer != 0) and (intNextBackpointer == 0)):
        ADUDataStart_1 = headerIndex - intBackpointer
        ADUDataEnd_1 = headerIndex
        ADUDataStart_2 = frameDataStarts
        ADUDataEnd_2 = nextHeaderIndex
    elif ((intBackpointer != 0) and (intNextBackpointer != 0)):
        ADUDataStart_1 = headerIndex - intBackpointer
        ADUDataEnd_1 = headerIndex
        ADUDataStart_2 = frameDataStarts
        ADUDataEnd_2 = nextHeaderIndex - intNextBackpointer

    AduData = bits[ADUDataStart:ADUDataEnd]
    #print(str(ADUDataStart) + '---' + str(ADUDataEnd))
    #print(bits[1200:8660])

    AduFrame = bits[headerIndex:frameDataStarts] #Combino cabeceras con datos de la ADU
    print(len(AduFrame)) #Debería ser 304 la cabecera
    AduFrame += AduData
    print(len(AduFrame))
    print(headerIndex)
    print("frame data starts " + str(frameDataStarts))


class RtpPayloadMp3: # En principio para MP3

    def setAudio(self, filePath):
        with open (filePath, "rb") as file:
            bytes = file.read();
            self.bits = BitArray(bytes).bin;
            riff = BitArray(hex='0x52494646').bin
            self.headerIndex = self.bits.find(riff)

    def takeMp3Frame(self):

        frameSize = self.bits[self.headerIndex+32:self.headerIndex+64]
        

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
