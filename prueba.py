from bitstring import BitArray

if __name__== "__main__":
    with open ("archivo.mp3", "rb") as file: # Abro archivo en modo lectura y binario

        bytes = file.read();
        bits = BitArray(bytes).bin;
        headerIndex = bits.find('11111111111'); #buscamos la cabecera
        header = bits[headerIndex:headerIndex+32];
        #byte = file.read(4)
        #header = BitArray(byte).bin; # Cabecera de 4 bytes, en bits.
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

        """print("version: " + version);
        print("layer: " + layer);
        print("bitrate: " + bitrate);
        print("sampling: " + sampling);
        print("padding: " + padding);"""

        print(protection);
        if (protection == 0) { # Si hay CRC tras la cabecera, este ocupa 16 bits
            sideInfoIndex = headerIndex + 32;
        } else {
            sideInfoIndex = headerIndex + 48;
        }

        print("canales: " + channel);
        if (channel == 11) { # Si el canal es mono, 17 bytes de side information
            sideInfo = bits[sideInfoIndex:sideInfoIndex+136];
            mainDataBegins = sideInfo[0:9];
        } else { # Si no es mono, 32 bytes de side information
            sideInfo = bits[sideInfoIndex:sideInfoIndex+256];
            mainDataBegins = sideInfo[0:9];
        }



        #while byte: #byte = '' es false
            #hago algo con el byte
        #numero = int.from_bytes(byte, byteorder='big');
        #its = f'{numero:08b}' #convierte el numero a 8 bits
        #print(bits);
            #byte = file.read(1)
