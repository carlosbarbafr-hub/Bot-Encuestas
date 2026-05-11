import discord
from discord.ext import commands, tasks
import os
import datetime
import asyncio
from flask import Flask
from threading import Thread

# --- 1. SERVIDOR WEB (Para que Render no cierre el bot) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot esta vivo y funcionando!"

def run():
    # Render usa la variable de entorno PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True # Esto permite que el hilo se cierre si el proceso principal muere
    t.start()

# --- 2. CONFIGURACIÓN DEL BOT ---
# Asegúrate de que el ID sea correcto y sea un número (int)
CHANNEL_ID = 1237432307120603227 
TOKEN = os.getenv("DISCORD_TOKEN")

# Configuración de los permisos (Intents)
intents = discord.Intents.default()
intents.message_content = True  # Necesario para bots modernos
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- 3. TAREA AUTOMÁTICA (Encuesta cada semana) ---
# He puesto el intervalo en 168 horas (1 semana) para evitar baneos por spam
@tasks.loop(hours=168.0)
async def enviar_encuesta():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        try:
            # Crear la encuesta (Solo funciona en discord.py 2.4+)
            encuesta = discord.Poll(
                question="¿Qué días puedes jugar (ROL)?",
                duration=datetime.timedelta(days=7),
                multiple=True
            )
            
            opciones = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo", "Ninguno"]
            for opc in opciones:
                encuesta.add_answer(text=opc)
            
            await channel.send(poll=encuesta)
            print(f"📊 Encuesta enviada con éxito: {datetime.datetime.now()}")
        except Exception as e:
            print(f"❌ Error al enviar la encuesta: {e}")
    else:
        print(f"❌ No se encontró el canal con ID {CHANNEL_ID}. Revisa los permisos del bot.")

# --- 4. EVENTOS ---
@bot.event
async def on_ready():
    print(f'✅ Bot conectado con éxito como: {bot.user.name}')
    
    # Pequeña espera para asegurar que la conexión es estable antes de iniciar el loop
    await asyncio.sleep(5)
    
    if not enviar_encuesta.is_running():
        enviar_encuesta.start()

# --- 5. EJECUCIÓN ---
if TOKEN:
    print("🚀 Arrancando servidor de monitoreo...")
    keep_alive()  # Lanzamos Flask primero
    
    print("🤖 Intentando conectar a Discord...")
    try:
        # Usamos strip() para limpiar espacios accidentales del token
        bot.run(TOKEN.strip())
    except discord.errors.LoginFailure:
        print("❌ Error: El Token de Discord es inválido. Revísalo en Render.")
    except Exception as e:
        print(f"❌ Error al iniciar el bot: {e}")
else:
    print("❌ ERROR: No se encontró la variable 'DISCORD_TOKEN' en el panel de Render.")
