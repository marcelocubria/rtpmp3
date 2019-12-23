import simplertp
import socket
import sys

if __name__== "__main__":
    cabeceraRTP = simplertp.RtpHeader()
    version = 2
    paddingFlag = 0
    extFlag = 0
    numeroCSRC = 4
    marker = 0
    payloadType = 90
    ssrc = 1000
    csrc = [2000, 3000, 4000, 5000]
    cabeceraRTP.set_header(version=2, pad_flag=0, ext_flag=0, cc=4, marker=0, payload_type=90, ssrc=4)
    cabeceraRTP.setCSRC(csrc)
    audio = simplertp.RtpPayloadMp3()
    audio.set_audio('archivo.mp3')
    numeroPaquetesRTP = 0
    paquetesMP3porRTP = 2
    ip = '127.0.0.1'
    port = 33332
    simplertp.send_rtp_packet(numeroPaquetesRTP, cabeceraRTP, audio, ip, port, paquetesMP3porRTP)
