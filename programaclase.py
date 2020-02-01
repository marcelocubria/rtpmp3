import simplertp
import socket
import sys



if __name__== "__main__":
    cabeceraRTP = simplertp.RtpHeader()
    csrc = [2000, 3000, 4000, 5000]
    cabeceraRTP.set_header(version=2, pad_flag=0, ext_flag=0, cc=4, marker=0, payload_type=14, ssrc=1000)
    cabeceraRTP.setCSRC(csrc)
    audio = simplertp.RtpPayloadMp3('prueba2.mp3')
    numeroPaquetesRTP = 0
    paquetesMP3porRTP = 2
    ip = '127.0.0.1'
    port = 33332
    simplertp.send_rtp_packet(cabeceraRTP, audio, ip, port, paquetesMP3porRTP, numeroPaquetesRTP)






# if __name__== "__main__":
#     csrc = [2000, 3000, 4000, 5000]
#     cabeceraRTP = simplertp.RtpHeader(cc=len(csrc))
#     cabeceraRTP.setCSRC(csrc)
#
#     audio = simplertp.RtpPayloadMp3('prueba2.mp3')
#
#     numeroPaquetesRTP = 0
#     paquetesMP3porRTP = 2
#
#     ip = '127.0.0.1'
#     port = 33332
#
#     simplertp.send_rtp_packet(cabeceraRTP, audio, ip, port, paquetesMP3porRTP, numeroPaquetesRTP)







#
# if __name__== "__main__":
#
#     cabeceraRTP = simplertp.RtpHeader()
#     audio = simplertp.RtpPayloadMp3('prueba2.mp3')
#
#     ip = '127.0.0.1'
#     port = 33332
#
#     simplertp.send_rtp_packet(cabeceraRTP, audio, ip, port)
