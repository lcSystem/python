import subprocess

def listar_dispositivos():
    try:
        # Ejecutar el comando arp-scan y capturar la salida
        output = subprocess.check_output(["sudo", "arp-scan", "--localnet"])
        # Decodificar la salida y dividirla en líneas
        output_lines = output.decode("utf-8").split("\n")
        # Filtrar solo las líneas que contienen direcciones IP y direcciones MAC
        dispositivos = [line for line in output_lines if "." in line and ":" in line]
        return dispositivos
    except Exception as e:
        raise RuntimeError("Error al listar dispositivos: " + str(e))

def desconectar_dispositivo(ip):
    try:
        # Ejecutar el comando iptables para bloquear el dispositivo
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"])
        subprocess.run(["sudo", "iptables", "-A", "FORWARD", "-s", ip, "-j", "DROP"])
    except Exception as e:
        raise RuntimeError(f"No se pudo desconectar el dispositivo: {str(e)}")

