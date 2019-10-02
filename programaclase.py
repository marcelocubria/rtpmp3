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
    cabeceraRTP.setHeader(version, paddingFlag, extFlag, numeroCSRC, marker, payloadType, ssrc)
    cabeceraRTP.setCSRC(csrc)
    audio = simplertp.RtpPayloadMp3()
    audio.setAudio('archivo.mp3')
    numeroPaquetesRTP = 2
    paquetesMP3porRTP = 2
    ip = '127.0.0.1'
    port = 33332
    simplertp.SendRtpPacket(numeroPaquetesRTP, cabeceraRTP, audio, ip, port, paquetesMP3porRTP)
