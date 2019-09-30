from bitstring import BitArray
import socket

def SendRtpPacket(number, header, payload, ip, port, packetsInPayload):
    for i in range(number):
        packet = header.version
        packet.append(header.padFlag)
        packet.append(header.extFlag)
        packet.append(header.cc)
        packet.append(header.marker)
        packet.append(header.payloadType)
        packet.append(BitArray(uint = header.seqNumber, length = 16))
        packet.append(BitArray(uint = header.timestamp, length = 32))
        packet.append(header.ssrc)
        print('Tamaño de la cabecera RTP: ' + str(len(packet.bin)))
        header.next()
        for j in range(packetsInPayload): # Cuantos paquetes mp3 metemos en el mismo paquete RTP
            payload.takeMp3Frame()
            packet.append(BitArray(bin = payload.frame))
        print(len(packet.bin))
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        my_socket.connect((ip, port))
        prueba = packet.tobytes()
        my_socket.send(prueba) #parece enviar todo correctamente comparados primeros 92 bits y ok
        print(packet[0:92].bin)

class RtpPayloadMp3: # En principio para MP3

    def setAudio(self, filePath):
        with open (filePath, "rb") as file:
            bytes = file.read();
            self.bits = BitArray(bytes).bin;
            self.headerIndex = self.bits.find('11111111111')

    def takeMp3Frame(self):

        header = self.bits[self.headerIndex:self.headerIndex+32];
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

        frameLength = int(144 * 8 * (224000/32000)) # 144 * bit rate / sample rate * 8 (el 144 es en bytes)
        nextmp3HeaderIndex = self.headerIndex + frameLength;
        self.frame = self.bits[self.headerIndex:nextmp3HeaderIndex]
        self.headerIndex = nextmp3HeaderIndex
        print(len(self.frame))


class RtpHeader:

    def setHeader(self, version, padFlag, extFlag, cc, marker, payloadType, ssrc):
        self.version = BitArray(uint = version, length = 2)
        self.padFlag = BitArray(uint = padFlag, length = 1)
        self.extFlag = BitArray(uint = extFlag, length = 1)
        self.cc = BitArray(uint = cc, length = 4)
        self.marker = BitArray(uint = marker, length = 1)
        self.payloadType = BitArray(uint = payloadType, length = 7)
        self.ssrc = BitArray(uint = ssrc, length = 32)

    def __init__(self):
        self.seqNumber = 1000 # Aleatorio
        self.timestamp = 200 # Aleatorio

    def setVersion(self, version):
        self.version = BitArray(uint = version, length = 2)

    def setPaddingFlag(self, padFlag):
        self.padFlag = BitArray(uint = padFlag, length = 1)

    def setExtensionFlag(self, extFlag):
        self.extFlag = BitArray(uint = extFlag, length = 1)

    def setCsrcCount(self, cc):
        self.cc = BitArray(uint = cc, length = 4)

    def setMarker(self, marker):
        self.marker = BitArray(uint = marker, length = 1)

    def setPayloadType(self, payloadType):
        self.payloadType = BitArray(uint = marker, length = 7)

    def setSequenceNumber(self, seqNumber):
        self.seqNumber = seqNumber

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def setSSRC(self, ssrc):
        self.ssrc = BitArray(uint = ssrc, length = 32)

    def next(self):
        self.seqNumber += 1;
        self.timestamp += 100; # Calcular siguiente timestamp

if __name__== "__main__":
    a = RtpHeader()
    a.setVersion(2)
    a.setPaddingFlag(1)
