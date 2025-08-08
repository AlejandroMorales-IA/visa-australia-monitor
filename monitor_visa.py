import os
import requests
from bs4 import BeautifulSoup
import time

# ===========================
# CONFIGURACIÓN
# ===========================

URL = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"

# Tu bot de Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Intervalo de comprobación en segundos
INTERVALO = 60  # 1 minuto

# Número de mensajes de alerta
REPETICIONES_ALERTA = 5

# ===========================
# FUNCIONES
# ===========================

def enviar_alerta(mensaje, repeticiones=1, pausa=2):
    """Envía un mensaje por Telegram varias veces."""
    for i in range(repeticiones):
        try:
            requests.post(
                f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
            )
            print(f"✅ Alerta enviada ({i+1}/{repeticiones}):", mensaje)
        except Exception as e:
            print("❌ Error enviando alerta:", e)
        time.sleep(pausa)  # espera entre mensajes

def obtener_estado_spain():
    """Obtiene el estado de Spain en la tabla de la página oficial."""
    headers = {"User-Agent": "Mozilla/5.0"}
    respuesta = requests.get(URL, headers=headers, timeout=10)
    if respuesta.status_code != 200:
        print("❌ Error al acceder a la página")
        return None
    
    soup = BeautifulSoup(respuesta.text, "html.parser")
    
    # Buscar la celda con "Spain"
    fila_spain = soup.find("td", string=lambda t: t and "Spain" in t)
    if not fila_spain:
        print("⚠ No se encontró Spain en la página.")
        return None

    # El estado está en la siguiente columna
    estado = fila_spain.find_next("td").get_text(strip=True)
    return estado

# ===========================
# EJECUCIÓN PRINCIPAL
# ===========================

estado_anterior = None

while True:
    try:
        estado_actual = obtener_estado_spain()
        print(f"📌 Estado actual Spain: {estado_actual}")
        # 🚨 PRUEBA FORZADA
        estado_actual = "OPEN"
        estado_anterior = "PAUSED"

        
        if estado_actual == "OPEN" and estado_anterior != "OPEN":
            enviar_alerta("🚨 ¡ATENCIÓN! La visa para Spain está ABIERTA 🚀", repeticiones=REPETICIONES_ALERTA, pausa=3)
        
        estado_anterior = estado_actual
    except Exception as e:
        print("❌ Error general:", e)
    
    time.sleep(INTERVALO)


