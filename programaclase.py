import simplertp

if __name__== "__main__":
    a = pruebaaa.RtpHeader();
    a.setHeader(2, 1, 1, 4, 0, 90, 1000)
    pruebaaa.SendRtpPacket(1, a)
