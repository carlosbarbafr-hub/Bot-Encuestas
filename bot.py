import discord
from discord.ext import commands, tasks
import os
import datetime
from flask import Flask
from threading import Thread

# --- SERVIDOR WEB PARA RENDER ---
app = Flask('')

@app.route('/')
def home():
    return "Bot esta vivo!"

def run():
    # Render asigna un puerto dinámico, usamos la variable PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.setDaemon(True) # Para que el hilo no bloquee el cierre del programa
    t.start()

# --- CONFIGURACIÓN DEL BOT ---
# Asegúrate de que este ID sea un número (int), no un texto
CHANNEL_ID = 1237432307120603227 
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # Necesario para leer contenido si usas comandos
intents.guilds = True           # Necesario para encontrar canales

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot conectado como: {bot.user.name}')
    # Verificamos si el canal existe al iniciar
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print(f"⚠️ Advertencia: No se encontró el canal con ID {CHANNEL_ID}")
    
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

@tasks.loop(hours=168.0) # Ajustado: ¡Cuidado! En tu código estaba a 1 minuto
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            # Creamos la encuesta
            # Nota: discord.Poll es para versiones muy recientes de discord.py
            encuesta = discord.Poll(
                question="¿Qué días puedes jugar (ROL)?",
                duration=datetime.timedelta(days=7),
                multiple=True
            )
            
            opciones = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo", "Ninguno"]
            for opc in opciones:
                encuesta.add_answer(text=opc)
            
            await channel.send(poll=encuesta)
            print(f"📊 Encuesta enviada a las {datetime.datetime.now()}")
        except Exception as e:
            print(f"❌ Error al enviar encuesta: {e}")
    else:
        print("❌ No pude encontrar el canal para enviar la encuesta.")

# --- INICIO ---
if TOKEN:
    print("🚀 Iniciando servidor web y Bot...")
    keep_alive()
    try:
        bot.run(TOKEN.strip())
    except discord.errors.LoginFailure:
        print("❌ Error: El TOKEN de Discord es inválido.")
    except Exception as e:
        print(f"❌ Error al iniciar el bot: {e}")
else:
    print("❌ Falta el TOKEN en Environment Variables")
