# rtpmp3

## Dependencies

bitstring (pip3 install bitstring)

## Simple RTP
El objetivo de este programa es facilitar el uso del protocolo RTP y la comprensión del mismo a través de poner a disposición una manera fácil de manipular la cabecera RTP.

Actualmente, el protocolo de audio soportado es el de MP3 o MPEG-1 Layer III.

Para acceder a sus funcionalidades basta con hacer `import simplertp`

El primer paso es crear un objeto de la clase **RtpHeader**. Este objeto es el que contendrá los diferentes campos de la cabecera RTP que compondrá los paquetes enviados. Al crearse el objeto, se asignaran por defecto unos valores de timestamp y número de secuencia aleatorios.

`cabeceraRtp = simplertp.RtpHeader()`

Con la función **set_header** del objeto RtpHeader se especifican los campos de la cabecera. Llamar a la función sin argumentos dejará la cabecera con los campos por defecto. A continuación se listan los argumentos que pueden acompañar a la función:

-*version*: versión del protocolo RTP. La versión actual es la 2 y es el valor por defecto. Los valores que puede tomar van de 0 a 3.

-*pad_flag*: 0 o 1 que indica si hay bits de padding al final del paquete. El valor por defecto es 0.

-*ext_flag*: 0 o 1 que indica que hay una extensión de la cabecera RTP después de los campos fijos. El valor por defecto es 0.

-*cc*: Número de identificadores CSRC que acompañan al SSRC, pueden ser de 0 a 16. El valor por defecto es 0.

-*marker*: Indicador que vale 0 o 1 para indicar a nivel de aplicación prioridad del paquete. 0 por defecto.

-*payload_type*: En el protocolo RTP, los diferentes protocolos de audio pueden tener un número de payload asignado. Debido a la escasez de valores disponibles en este campo, hay un rango de valores no asignados que se pueden usar libremente. Los valores posibles van de 0 a 127. El valor por defecto es 90.

-*SSRC*: Identificador de la fuente de sincronización, que identifica la fuente del flujo de datos. El valor por defecto es 1000, pero puede tomar cualquier valor en el rango de 0 a 4294967296.

Un ejemplo de llamada a esta función es:

`cabeceraRTP.set_header(version=2, pad_flag=0, ext_flag=0, cc=4, marker=0, payload_type=90, ssrc=1000)`

Si un campo no se especifica al llamar la función, tomará el valor por defecto indicado.

Si hemos asignado un valor de cc mayor a 0, deberemos indicar con la función **setCSRC** la misma cantidad de identificadores de fuentes. La función toma como entrada un array:

`cabeceraRTP.setCSRC([2000, 3000, 4000, 5000])`

## Audio MP3

El siguiente paso es establecer el payload que se transportará por RTP, en este caso MP3. Primero, creamos un objeto de payload para MP3 con el constructor **RtpPayloadMp3**:

`audio = simplertp.RtpPayloadMp3()`

Tenemos que pasarle el path de un fichero de este protocolo mediante la función **set_audio** del objeto:

`audio.set_audio('archivo.mp3')`

## Envío de paquetes RTP

Una vez hecho todo lo anterior, ya podemos enviar paquetes RTP con la cabecera que hayamos establecido y el payload correspondiente.

La transmisión se hace sobre UDP, por lo que tenemos que indicar una IP y puerto destino. A su vez, podemos indicar cuantos paquetes RTP queremos enviar (0 indica enviar el archivo mp3 entero) y el número de paquetes MP3 que habrá en cada paquete RTP.

De tal manera, un ejemplo en envío de paquetes RTP es el siguiente gracias a la función **send_rtp_packet**:

`simplertp.send_rtp_packet(numeroPaquetesRTP, cabeceraRTP, audio, ip, port, paquetesMP3porRTP)`

## Wireshark

Para poder ver el flujo RTP en Wireshark es necesario hacer el siguiente paso: Ir a *Analyze -> Enabled Protocols -> RTP* y activar la casilla *rtp_udp* 
