import discord
from discord.ext import commands, tasks
import os
import datetime
import asyncio
from flask import Flask
from threading import Thread

# --- 1. CONFIGURACIÓN DEL SERVIDOR WEB ---
app = Flask('')

@app.route('/')
def home():
    return "Servidor del Bot activo"

def run():
    try:
        # Render requiere que escuchemos en un puerto
        port = int(os.environ.get("PORT", 10000))
        print(f"🌐 Iniciando Flask en el puerto {port}...")
        app.run(host='0.0.0.0', port=port)
    except Exception as e:
        print(f"❌ Error en el servidor Flask: {e}")

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("🚀 Hilo de Keep_Alive iniciado.")

# --- 2. CONFIGURACIÓN DEL BOT ---
CHANNEL_ID = 1237432307120603227 
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. TAREA DE ENCUESTA ---
@tasks.loop(hours=168.0) # Una vez a la semana
async def enviar_encuesta():
    print("📡 Intentando enviar encuesta programada...")
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            encuesta = discord.Poll(
                question="¿Qué días puedes jugar (ROL)?",
                duration=datetime.timedelta(days=7),
                multiple=True
            )
            for opc in ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo", "Ninguno"]:
                encuesta.add_answer(text=opc)
            
            await channel.send(poll=encuesta)
            print("📊 Encuesta enviada correctamente.")
        except Exception as e:
            print(f"❌ Error enviando encuesta: {e}")
    else:
        print(f"❌ No se encontró el canal {CHANNEL_ID}")

# --- 4. EVENTOS ---
@bot.event
async def on_ready():
    print(f'✅ LOGUEADO: {bot.user.name} (ID: {bot.user.id})')
    await asyncio.sleep(5)
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()
        print("⏰ Loop de encuestas iniciado.")

# --- 5. ARRANQUE ---
if __name__ == "__main__":
    if not TOKEN:
        print("❌ ERROR CRÍTICO: No se encontró la variable DISCORD_TOKEN.")
    else:
        print("1️⃣ Iniciando servidor web...")
        keep_alive()
        
        print("2️⃣ Iniciando conexión con Discord...")
        try:
            # strip() elimina espacios o saltos de línea invisibles
            bot.run(TOKEN.strip())
        except discord.errors.LoginFailure:
            print("❌ ERROR: El Token es incorrecto o ha sido reseteado.")
        except Exception as e:
            print(f"❌ ERROR AL EJECUTAR EL BOT: {e}")
