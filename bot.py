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

CHANNEL_ID = 843615420417835049

# Hora española (Madrid)
SPAIN_TZ = datetime.timezone(datetime.timedelta(hours=2))

# Domingo 17:00
ENCUESTA_HORA = datetime.time(hour=17, minute=0, tzinfo=SPAIN_TZ)

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

    if not enviar_recordatorio.is_running():
        enviar_recordatorio.start()
        print("📅 Sistema de recordatorios iniciado.")

# =========================================================
# ENCUESTA
# =========================================================

@tasks.loop(time=ENCUESTA_HORA)
async def enviar_encuesta():

    ahora = datetime.datetime.now(SPAIN_TZ)

    # Solo domingos
    if ahora.weekday() != 6:
        return

    print("⏳ Enviando encuesta semanal...")

    try:
        channel = bot.get_channel(CHANNEL_ID)

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
# RECORDATORIO SEMANAL (Martes, Viernes, Domingo)
# =========================================================

RECORDATORIO_HORA = datetime.time(hour=16, minute=59, tzinfo=SPAIN_TZ)

@tasks.loop(time=RECORDATORIO_HORA)
async def enviar_recordatorio():

    ahora = datetime.datetime.now(SPAIN_TZ)

    # Solo martes (1), viernes (4) y domingo (6)
    if ahora.weekday() not in (1, 4, 6):
        return

    print("⏳ Enviando recordatorio...")

    try:
        channel = bot.get_channel(CHANNEL_ID)

        if channel is None:
            channel = await bot.fetch_channel(CHANNEL_ID)

        await channel.send("¡Recordatorio! No olvidéis confirmar vuestra disponibilidad.")

        print("✅ Recordatorio enviado correctamente.")

    except Exception as e:
        print(f"❌ Error enviando recordatorio: {e}")

# =========================================================
# COMANDO TEST
# =========================================================

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# =========================================================
# COMANDO MANUAL PARA PROBAR
# =========================================================

@bot.command()
async def encuesta(ctx):

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

    await ctx.send(poll=encuesta)

# =========================================================
# INICIO
# =========================================================

print("🤖 Iniciando bot...")

bot.run(TOKEN.strip())
