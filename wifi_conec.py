from machine import Pin
import os,time

def web_page(): 
	html = """
	<html>
		<head>
			<meta name="viewport" content="width=device-width, initial-scale=1">
		</head> 
		<body>
			<h1>Hello, World!</h1>
			<h1>Ana y Anthonella</h1>
			<button id="mostrarTexto">Muestra el archivo de texto</button>
            <div id="contenido"></div> 
		</body>
	</html>
	""" 
	return html 
# FUNCIÓN PARA ESTABLECER LA CONEXIÓN WIFI (STATION)

def conf_red(SSID, PASSWORD):
    import network                            # importa el módulo network
    global sta_if
    sta_if = network.WLAN(network.STA_IF)     # instancia el objeto -sta_if- para controlar la interfaz STA
    if not sta_if.isconnected():              # si no existe conexión...
        sta_if.active(True)                       # activa el interfaz STA del ESP32
        sta_if.connect(SSID, PASSWORD)            # inicia la conexión con el AP
        print('Conectando a la red', SSID +"...")
        while not sta_if.isconnected():           # ...si no se ha establecido la conexión...
            pass                                  # ...repite el bucle...
    print('Configuración de red (IP/netmask/gw/DNS):', sta_if.ifconfig())

def conf_socket():
    try:
        # ************************
        # Configure the socket connection
        # over TCP/IP
        import socket
        global s,direc
        # AF_INET - use Internet Protocol v4 addresses
        # SOCK_STREAM means that it is a TCP socket.
        # SOCK_DGRAM means that it is a UDP socket.
        #addr = socket.getaddrinfo('192.168.4.1', 2020)[0][-1]
        direc=sta_if.ifconfig()[0] #obtener la direccion ip de la tupla
        print("Aqui",direc)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("sss",s)
        s.bind(('', 80)) 
        s.listen(5) 
    except OSError as e:
         print('Faild to socket conf')
         s.close()


conf_red("Briante","Simba?#802")    # DESCOMENTAR Y PONER nombre/clave_de_red RED PARA EJECUTAR
conf_socket()

while True:
    print("estoy")                    
    # Socket accept()        
    conn, addr = s.accept()
    # Socket receive()
    print("1: ",conn)
    print("2: ",addr)
    request=conn.recv(1024)
    conn.settimeout(None)
    response = web_page()
    #Create a socket reply
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
        
    conn.close()
    
    time.sleep(0.1)

