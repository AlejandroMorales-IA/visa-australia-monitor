import os
import requests
from bs4 import BeautifulSoup

# ===========================
# CONFIGURACIÓN
# ===========================

URL = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# ===========================
# FUNCIONES
# ===========================

def enviar_alerta(mensaje):
    """Envía un mensaje por Telegram."""
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
        )
        print(f"✅ Alerta enviada: {mensaje}")
    except Exception as e:
        print("❌ Error enviando alerta:", e)

def obtener_estado_spain():
    """Obtiene el estado de Spain en la tabla de la página oficial."""
    headers = {"User-Agent": "Mozilla/5.0"}
    respuesta = requests.get(URL, headers=headers, timeout=10)
    if respuesta.status_code != 200:
        print("❌ Error al acceder a la página")
        return None
    
    soup = BeautifulSoup(respuesta.text, "html.parser")
    fila_spain = soup.find("td", string=lambda t: t and "Spain" in t)
    if not fila_spain:
        print("⚠ No se encontró Spain en la página.")
        return None

    estado = fila_spain.find_next("td").get_text(strip=True)
    estado = estado.lower().replace("*", "")  # normalizar
    return estado

# ===========================
# EJECUCIÓN ÚNICA
# ===========================

estado_actual = obtener_estado_spain()
print(f"📌 Estado actual Spain: {estado_actual}")

if estado_actual == "open":
    enviar_alerta("🚨 ¡ATENCIÓN! La visa para Spain está ABIERTA 🚀")
