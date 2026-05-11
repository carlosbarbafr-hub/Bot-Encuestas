import os
import datetime
import discord
from discord.ext import commands, tasks

# =========================================================
# TOKEN
# =========================================================

TOKEN = os.getenv("DISCORD_TOKEN")

if TOKEN is None:
    raise ValueError("❌ DISCORD_TOKEN no encontrado en Railway Variables")

# =========================================================
# CONFIGURACIÓN
# =========================================================

CHANNEL_ID = 1237432307120603227  # Cambia esto por tu canal

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================================================
# EVENTOS
# =========================================================

@bot.event
async def on_ready():
    print(f"✅ Bot conectado como: {bot.user}")
    print(f"🆔 ID del bot: {bot.user.id}")

    if not enviar_encuesta.is_running():
        enviar_encuesta.start()
        print("📅 Sistema de encuestas iniciado.")

@bot.event
async def on_disconnect():
    print("⚠️ Bot desconectado.")

@bot.event
async def on_resumed():
    print("🔄 Conexión restaurada.")

# =========================================================
# ENCUESTA SEMANAL
# =========================================================

@tasks.loop(hours=168)  # Cada 7 días
async def enviar_encuesta():

    print("⏳ Enviando encuesta semanal...")

    try:
        channel = bot.get_channel(CHANNEL_ID)

        # Si no está cacheado
        if channel is None:
            channel = await bot.fetch_channel(CHANNEL_ID)

        encuesta = discord.Poll(
            question="¿Qué días puedes jugar?",
            duration=datetime.timedelta(days=7),
            multiple=True
        )

        opciones = [
            "Lunes",
            "Martes",
            "Miércoles",
            "Jueves",
            "Viernes",
            "Sábado",
            "Domingo",
            "Ninguno"
        ]

        for opcion in opciones:
            encuesta.add_answer(text=opcion)

        await channel.send(poll=encuesta)

        print("✅ Encuesta enviada correctamente.")

    except Exception as e:
        print(f"❌ Error enviando encuesta: {e}")

# =========================================================
# COMANDO TEST
# =========================================================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# =========================================================
# INICIO
# =========================================================

print("🤖 Iniciando bot...")

bot.run(TOKEN.strip())
