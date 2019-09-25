import simplertp

if __name__== "__main__":
    a = simplertp.RtpHeader()
    a.setHeader(2, 1, 1, 4, 0, 90, 1000)
    b = simplertp.RtpPayloadMp3()
    b.setAudio('archivo.mp3')
    b.takeMp3Frame()

    simplertp.SendRtpPacket(1, a, b.frame)
