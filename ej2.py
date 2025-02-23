import time
import machine

led = machine.Pin(16,machine.Pin.OUT)
led.off()

# ************************
# Configure the ESP32 wifi
# as STAtion mode.
import network
import wifi_credentials

#Creamos la interfaz
sta = network.WLAN(network.STA_IF)

if not sta.isconnected():
    print('connecting to network...')
    sta.active(True)    
    sta.connect(wifi_credentials.ssid, wifi_credentials.password)
    while not sta.isconnected():
        pass
print('network config:', sta.ifconfig())

# ************************
# Configure the socket connection
# over TCP/IP
import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable 
#                 by any address the machine happens to have
s.listen(5)     # max of 5 socket connections

def web_page():    
  html = """<!DOCTYPE html>
<html lang = "en">
    <head>
        <meta charset="UTF-8">
        <title>Configuracion</title>
    
        
    </head>
    <title>Configuracion</title>
    <body>
        Nombre: <input type = "text" id="nombre" ><br/><br/>
        Apellido: <input type = "text" id="apellido"><br/><br/>

        <input type="submit" value="Enviar" onclick="datosNomApe()"> 

        <div id="info"></div>
        
        
        <script>
            console.log("Entrando")
            var xhttp = new XMLHttpRequest();
                        
            var a = document.getElementById("nombre").value;
            var b = document.getElementById("apellido").value;
            var informacionDelUsuario = "nombre=" + a + "&apellido=" + b;
            
            xhttp.onreadystatechange = function(){
                if(this.readyState == 4){
                    if(this.status == 200){
                        document.getElementById('info').innerHTML = this.responseText;
                    }
                    else{
                        document.getElementById('info').innerHTML = 'Desconectado';
                    }
                }       
            };
            
            

            function datosNomApe(){
                xhttp.open("GET", "/procesar", true);
                xhttp.send();
            }
        </script>
    </body>
</html>""" 
  return html


while True:
  try:    
    conn, addr = s.accept()
    conn.settimeout(3.0)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    conn.settimeout(None)
    request = str(request)
    print('Content = %s' % request)
    
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()
  except OSError as e:
    conn.close()
    print('Connection closed')


