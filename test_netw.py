import subprocess
import platform
import os

ip_dns = '8.8.8.8' #IP del DNS
ip_host1 = '192.168.1.1' #IP de DMP

dns_nombres={
    '1.1.1.1':'CloudFlare',
    '8.8.8.8':'Google',
    '94.140.14.14':'AdGuard'
}
nombre_dns=dns_nombres.get(ip_dns, 'Desconocido')

def limpiar_pantalla():
    if platform.system().lower() == 'windows':
        os.system('cls')
    else:
        os.system('clear')

def realizar_ping(ip, nombre='host'):
    try:
        if platform.system().lower() == 'windows':
            comando = ['ping', '-n', '4', ip]
        else:
            comando = ['ping', '-c', '4', ip]

        resultado = subprocess.run(
            comando,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if resultado.returncode == 0:
            print(f'    Ping exitoso, hay conexión con {nombre}\n')
            #print(resultado.stdout)
        else:
            print(f'    No se pudo hacer ping a {nombre}\n')
            #print(resultado.stderr)

    except Exception as e:
        print(f'Ocurrió un error: {e}')

def ejecutar_comando(comando):
    try:
        result = subprocess.run(comando, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f'    Error al ejecutar el comando: {result.stderr}')
    except Exception as e:
        print(f'Ocurrió un error: {e}')

def ping_dns():
    realizar_ping(ip_dns, nombre_dns)

def ping_host_1():
    realizar_ping(ip_host1, "host 1")

def tracert_dns():
    comando=['tracert',ip_dns] if platform.system().lower() == 'windows' else ['traceroute', ip_dns]
    ejecutar_comando(comando)

def diagnostico_automatico():
    hosts = [
        (ip_host1,'host 1'),
        (ip_dns, nombre_dns)
    ]
    for ip, nombre in hosts:
        print(f'Verificando conexión con {nombre}')
        realizar_ping(ip, nombre)

def menu():
    opciones={
        1:lambda:ping_dns(),
        2:lambda:tracert_dns(),
        3:lambda:diagnostico_automatico(),
        4:lambda:ping_host_1(),
        0:lambda:exit()
    }

    while True:
        print(f'1: Verificar conexión a internet')
        print(f'2: Trazar ruta hacia {nombre_dns}')
        print(f'3: Diagnóstico automático')
        print(f'4: Verificar conexion con el host {ip_host1}')
        print(f'0: Salir\n')
        
        try:
            opcion = int(input(f'Ingrese el número de la acción correspondiente: '))
            limpiar_pantalla()
            if opcion in opciones:
                opciones[opcion]()
                input('Presione Enter para volver al menú ')
                limpiar_pantalla()
            else:
                print(f'La opción no es válida')
        except ValueError:
            print(f'Por favor, ingrese un número válido.')

menu()