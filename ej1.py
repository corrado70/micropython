# Complete project details at https://RandomNerdTutorials.com
import socket
def web_page():    
  html = """<!DOCTYPE html>
<html lang = "en">
    <head>
        <meta charset="UTF-8">
        <title>Configuracion</title>
    
        <script>
            var xhttp = new XMLHttpRequest();
                        
            #var a = document.getElementById("nombre").value;
            #var b = document.getElementById("apellido").value;
            #var informacionDelUsuario = "nombre=" + a + "&apellido=" + b;
            
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
                xhttp.open("POST", "/procesar", true);
                xhttp.send();
            }
        </script>
    </head>
    <title>Configuracion</title>
    <body>
        Nombre: <input type = "text" id="nombre" ><br/><br/>
        Apellido: <input type = "text" id="apellido"><br/><br/>

        <input type="submit" value="Enviar" onclick="datosNomApe"> 

        <div id="info"></div>
    </body>
</html>""" 
  return html

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


conf_red("Briante","Simba?#802")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


while True:
  try:
    if gc.mem_free() < 102000:
      gc.collect()
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


