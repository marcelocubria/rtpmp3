from bitstring import BitArray
import socket
import random


def send_rtp_packet(number, header, payload, ip, port, packets_in_payload):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
        my_socket.connect((ip, port))
        if (number == 0):
            number = 1000000
        try:
            for i in range(number):
                packet = BitArray()
                packet.append(header.version)
                packet.append(header.pad_flag)
                packet.append(header.ext_flag)
                packet.append(header.cc)
                packet.append(header.marker)
                packet.append(header.payload_type)
                packet.append(BitArray(uint = header.seq_number, length = 16))
                packet.append(BitArray(uint = header.timestamp, length = 32))
                packet.append(header.ssrc)
                packet.append(header.csrc)
                if header.ext_flag.bin == '1':
                    print('aqui va la extension')
                print('Tamaño de la cabecera RTP: ' + str(len(packet.bin)))
                for j in range(packets_in_payload):  # Cuantos paquetes mp3 metemos en el mismo paquete RTP
                    payload._take_mp3_frame()
                    packet.append(BitArray(bin = payload.frame))
                print(len(packet.bin))
                packetBytes = packet.tobytes()
                my_socket.send(packetBytes)  # parece enviar todo correctamente comparados primeros 92 bits y ok
                print(packet[0:92].bin)
                header.next(payload.frameTimeMs)
        except IndexError:
            pass


class RtpPayloadMp3:  # En principio para MP3

    def set_audio(self, file_path):
        with open(file_path, "rb") as file:
            bytes = file.read()
            self.bits = BitArray(bytes).bin
            self.header_index = self.bits.find('11111111111')

    def _take_mp3_frame(self):

        header = self.bits[self.header_index:self.header_index+32]
        frame_sync = header[0:11]
        version = header[11:13]
        layer = header[13:15]
        protection = header[15]
        bitrate = header[16:20]
        sampling = header[20:22]
        padding = header[22]
        private = header[23]
        channel = header[24:26]
        modeext = header[26:28]
        copyright = header[28]
        original = header[29]
        emphasis = header[30:]

        if (version == '11') and (layer == '01'):
            if (bitrate == '1100'):
                bps = 224000

            if (sampling == '10'):
                sample_rate = 32000
            elif sampling == '00':
                sample_rate = 44100
            elif sampling == '01':
                sample_rate = 48000

        frame_length = int(144 * 8 * (bps/sample_rate))  # 144 * bit rate / sample rate * 8 (el 144 es en bytes)
        self.frameTimeMs = int(144/sample_rate * 1000 * 8)  # tiempo por frame en milisegundos
        next_mp3_header_index = self.header_index + frame_length
        self.frame = self.bits[self.header_index:next_mp3_header_index]
        self.header_index = next_mp3_header_index


class RtpHeader:

    def set_header(self, version, pad_flag, ext_flag, cc, marker, payload_type, ssrc):
        self.version = BitArray(uint = version, length = 2)
        self.pad_flag = BitArray(uint = pad_flag, length = 1)
        self.ext_flag = BitArray(uint = ext_flag, length = 1)
        self.cc = BitArray(uint = cc, length = 4)
        self.marker = BitArray(uint = marker, length = 1)
        self.payload_type = BitArray(uint = payload_type, length = 7)
        self.ssrc = BitArray(uint = ssrc, length = 32)
        self.csrc = BitArray()
        self.extension = BitArray()

    def __init__(self):
        self.seq_number = random.randint(1, 10000)  # Aleatorio
        self.timestamp = random.randint(1, 10000)  # Aleatorio

    def setVersion(self, version):
        self.version = BitArray(uint = version, length = 2)

    def setPaddingFlag(self, pad_flag):
        self.pad_flag = BitArray(uint = pad_flag, length = 1)

    def setExtensionFlag(self, ext_flag):
        self.ext_flag = BitArray(uint = ext_flag, length = 1)

    def setCsrcCount(self, cc):
        self.cc = BitArray(uint = cc, length = 4)

    def setMarker(self, marker):
        self.marker = BitArray(uint = marker, length = 1)

    def setPayloadType(self, payload_type):
        self.payload_type = BitArray(uint = marker, length = 7)

    def setSequenceNumber(self, seq_number):
        self.seq_number = seq_number

    def setTimestamp(self, timestamp):
        self.timestamp = timestamp

    def setSSRC(self, ssrc):
        self.ssrc = BitArray(uint = ssrc, length = 32)

    def setCSRC(self, csrcValues):
        for i in range(len(csrcValues)):
            self.csrc.append(BitArray(uint = csrcValues[i], length = 32))

    def next(self, frameTimeMs):
        self.seq_number += 1
        # he leido en wikipedia que en vez de 8k podria ser 90k???
        self.timestamp += int(8000 * (frameTimeMs/1000))  # Calcular siguiente timestamp


if __name__ == "__main__":
    a = RtpHeader()
    a.setVersion(2)
    a.setPaddingFlag(1)
