"""
╔══════════════════════════════════════════════════════════╗
║   ⚖️  Bot de Libertad Condicional — Honduras  ⚖️   ║
║       Decreto 130-2017 · Arts. 81 y 82                  ║
║   💡 Idea: Abg. Brayan Fernando Padilla Rodríguez        ║
╚══════════════════════════════════════════════════════════╝
"""

import os, logging
from datetime import date
from dateutil.relativedelta import relativedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters, ContextTypes
)

logging.basicConfig(format="%(asctime)s — %(levelname)s — %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

(ELEGIR_ART, ELEGIR_SUP82, FECHA_SENTENCIA, PENA_ANIOS, PENA_MESES,
 SEGUNDA_PREGUNTA, PENA2_ANIOS, PENA2_MESES, FECHA_INICIO2) = range(9)

MESES_ES = ["enero","febrero","marzo","abril","mayo","junio",
            "julio","agosto","septiembre","octubre","noviembre","diciembre"]

# ══════════════════════════════════════════════════════════
# ✦ DECORACIONES Y UTILIDADES
# ══════════════════════════════════════════════════════════

SEP  = "┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄"
SEP2 = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
SEP3 = "▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸▸"

def fmt(d):
    return f"{d.day} de {MESES_ES[d.month-1]} de {d.year}  📅 {d.strftime('%d/%m/%Y')}"

def barra_progreso(pct):
    lleno = round(pct / 10)
    return "🟩" * lleno + "⬜" * (10 - lleno)

def parse_fecha(txt):
    from datetime import datetime
    for f in ("%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y"):
        try:
            return datetime.strptime(txt.strip(), f).date()
        except ValueError:
            continue
    return None

def calcular_lc(art, sup82, pena_a, pena_m, inicio):
    pena_decimal = pena_a + pena_m / 12
    total_dias   = pena_a * 365 + pena_m * 30
    if art == "81":
        if pena_decimal <= 15:
            fraccion, emoji = "½  —  Mitad de la pena", "⚖️"
            min_dias = total_dias / 2
        elif pena_decimal < 30:
            fraccion, emoji = "⅔  —  Dos tercios de la pena", "⚖️"
            min_dias = total_dias * 2 / 3
        else:
            fraccion, emoji = "30 años fijos (pena máxima)", "🔒"
            min_dias = 30 * 365
    else:
        if sup82 in ("mayores70", "enfermo"):
            return inicio, "Sin fracción mínima requerida", "🩺"
        else:
            fraccion, emoji = "⅓  —  Un tercio de la pena", "⚖️"
            min_dias = total_dias / 3

    min_a = int(min_dias // 365)
    resto = min_dias - min_a * 365
    min_m = int(resto // 30)
    min_d = round(resto - min_m * 30)
    return inicio + relativedelta(years=min_a, months=min_m, days=min_d), fraccion, emoji

def pct_cumplido(pena_a, pena_m, art, sup82):
    total = pena_a * 12 + pena_m
    if total == 0:
        return 0
    if art == "81":
        pena_d = pena_a + pena_m / 12
        if pena_d <= 15:
            return 50
        elif pena_d < 30:
            return 67
        else:
            return round(30 * 12 / total * 100)
    else:
        if sup82 in ("mayores70", "enfermo"):
            return 0
        return 33

# ══════════════════════════════════════════════════════════
# ✦ COMANDOS BÁSICOS
# ══════════════════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    texto = (
        f"🏛️  *BIENVENIDO AL BOT OFICIAL*\n"
        f"{SEP2}\n"
        f"⚖️  *Libertad Condicional — Honduras*\n"
        f"{SEP2}\n\n"
        f"📜  *Base legal:*\n"
        f"     Decreto N.º 130-2017\n"
        f"     Artículos *81* y *82* del Código Penal\n\n"
        f"💡  *Creado por:*\n"
        f"     Abg. Brayan Fernando Padilla Rodríguez\n\n"
        f"{SEP}\n\n"
        f"📌  *¿Qué puedo calcular?*\n\n"
        f"  🔹 Fecha mínima de Libertad Condicional\n"
        f"  🔹 Fecha de excarcelación total\n"
        f"  🔹 Casos con *dos condenas* sucesivas\n"
        f"  🔹 Todos los supuestos del Art. 81 y 82\n\n"
        f"{SEP}\n\n"
        f"📲  *Comandos disponibles:*\n\n"
        f"  /calcular  →  Iniciar nuevo cálculo\n"
        f"  /ayuda     →  Cómo usar el bot\n"
        f"  /acerca    →  Información del bot\n\n"
        f"{SEP2}\n"
        f"_⚠️ Herramienta informativa. No sustituye_\n"
        f"_asesoría legal profesional._"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")

async def ayuda(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    texto = (
        f"📖  *GUÍA DE USO*\n"
        f"{SEP2}\n\n"
        f"*Paso a paso:*\n\n"
        f"  1️⃣  Escriba */calcular*\n"
        f"  2️⃣  Seleccione el artículo aplicable\n"
        f"  3️⃣  Ingrese la fecha de sentencia firme\n"
        f"  4️⃣  Ingrese años y meses de la pena\n"
        f"  5️⃣  Indique si hay segunda condena\n"
        f"  6️⃣  Reciba el resultado completo ✅\n\n"
        f"{SEP}\n\n"
        f"📗  *Artículo 81 — Régimen General:*\n"
        f"  • Pena ≤ 15 años  →  cumple *½*\n"
        f"  • 15 < pena < 30  →  cumple *⅔*\n"
        f"  • Pena ≥ 30 años  →  *30 años* fijos\n\n"
        f"📙  *Artículo 82 — Régimen Excepcional:*\n"
        f"  • Mayor de 70 años  →  sin fracción\n"
        f"  • Enfermo grave  →  sin fracción\n"
        f"  • Delincuente primario  →  cumple *⅓*\n\n"
        f"{SEP}\n\n"
        f"❓  ¿Necesita cancelar un cálculo?\n"
        f"     Escriba */cancelar*"
    )
    await update.message.reply_text(texto, parse_mode="Markdown")

async def acerca(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = getattr(update, 'message', None) or update.callback_query.message
    texto = (
        f"ℹ️  *ACERCA DE ESTE BOT*\n"
        f"{SEP2}\n\n"
        f"⚖️  *Nombre:*\n"
        f"     Bot de Libertad Condicional Honduras\n\n"
        f"🏛️  *Base legal:*\n"
        f"     Decreto N.º 130-2017\n"
        f"     Arts. 81 y 82 — Código Penal\n\n"
        f"💡  *Idea y concepto:*\n"
        f"     Abg. Brayan Fernando Padilla Rodríguez\n\n"
        f"📅  *Fecha de creación:*\n"
        f"     11 de marzo de 2026\n\n"
        f"🔖  *Versión:* 3.0\n\n"
        f"{SEP}\n\n"
        f"⚠️  _Este bot es una herramienta informativa._\n"
        f"_Los cálculos son estimaciones basadas en_\n"
        f"_la ley. Siempre consulte a un abogado_\n"
        f"_penalista habilitado en Honduras._\n\n"
        f"{SEP2}"
    )
    await msg.reply_text(texto, parse_mode="Markdown")

# ══════════════════════════════════════════════════════════
# ✦ CONVERSACIÓN — PASO A PASO
# ══════════════════════════════════════════════════════════

async def calcular_inicio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("📗  Art. 81 — Régimen General",     callback_data="art_81")],
        [InlineKeyboardButton("📙  Art. 82 — Régimen Excepcional", callback_data="art_82")],
    ])
    await update.message.reply_text(
        f"🧮  *NUEVO CÁLCULO*\n"
        f"{SEP2}\n\n"
        f"  1️⃣ ▸ *Artículo*  ←  aquí\n"
        f"  2️⃣ ▸ Fecha de sentencia\n"
        f"  3️⃣ ▸ Años de la pena\n"
        f"  4️⃣ ▸ Meses de la pena\n"
        f"  5️⃣ ▸ Segunda condena\n\n"
        f"{SEP}\n\n"
        f"⚖️  *Seleccione el artículo aplicable:*",
        reply_markup=teclado,
        parse_mode="Markdown"
    )
    return ELEGIR_ART

async def elegir_art(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    art = query.data.split("_")[1]
    ctx.user_data["art"] = art

    if art == "82":
        teclado = InlineKeyboardMarkup([
            [InlineKeyboardButton("👴  Mayores de 70 años",            callback_data="sup_mayores70")],
            [InlineKeyboardButton("🏥  Enfermo grave incurable",        callback_data="sup_enfermo")],
            [InlineKeyboardButton("📋  Delincuente primario  ( ⅓ )",   callback_data="sup_primario")],
        ])
        await query.edit_message_text(
            f"📙  *ARTÍCULO 82 — Régimen Excepcional*\n"
            f"{SEP2}\n\n"
            f"  1️⃣ ▸ Artículo  ✅\n"
            f"  1️⃣b ▸ *Supuesto*  ←  aquí\n"
            f"  2️⃣ ▸ Fecha de sentencia\n"
            f"  3️⃣ ▸ Años / Meses\n\n"
            f"{SEP}\n\n"
            f"🔍  *Seleccione el supuesto:*",
            reply_markup=teclado,
            parse_mode="Markdown"
        )
        return ELEGIR_SUP82

    ctx.user_data["sup82"] = None
    await query.edit_message_text(
        f"📗  *ARTÍCULO 81 — Régimen General*  ✅\n"
        f"{SEP2}\n\n"
        f"  1️⃣ ▸ Artículo  ✅\n"
        f"  2️⃣ ▸ *Fecha de sentencia*  ←  aquí\n"
        f"  3️⃣ ▸ Años / Meses\n\n"
        f"{SEP}\n\n"
        f"📅  *Fecha de sentencia firme*\n\n"
        f"Ingrese la fecha en formato *DD/MM/AAAA*\n"
        f"_Ejemplo: 29/03/2023_",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📅  Usar fecha de hoy", callback_data="fecha_hoy")
        ]]),
        parse_mode="Markdown"
    )
    return FECHA_SENTENCIA

async def elegir_sup82(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sup = query.data.split("_", 1)[1]
    ctx.user_data["sup82"] = sup

    info = {
        "mayores70": ("👴  Mayor de 70 años", "Sin fracción mínima — Pena máx. 20 años"),
        "enfermo":   ("🏥  Enfermo grave incurable", "Sin fracción mínima — Pena máx. 20 años\nRequiere informe médico del Sistema Público"),
        "primario":  ("📋  Delincuente primario", "Debe cumplir ⅓ de la pena — Pena máx. 10 años"),
    }
    nom, desc = info[sup]

    await query.edit_message_text(
        f"📙  *{nom}*  ✅\n"
        f"_{desc}_\n"
        f"{SEP2}\n\n"
        f"  1️⃣ ▸ Artículo + Supuesto  ✅\n"
        f"  2️⃣ ▸ *Fecha de sentencia*  ←  aquí\n"
        f"  3️⃣ ▸ Años / Meses\n\n"
        f"{SEP}\n\n"
        f"📅  *Fecha de sentencia firme*\n\n"
        f"Ingrese la fecha en formato *DD/MM/AAAA*\n"
        f"_Ejemplo: 01/02/2022_",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("📅  Usar fecha de hoy", callback_data="fecha_hoy")
        ]]),
        parse_mode="Markdown"
    )
    return FECHA_SENTENCIA

async def fecha_hoy_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ctx.user_data["fecha_sent"] = date.today()
    await query.edit_message_text(
        f"📅  *Fecha registrada:*\n"
        f"     {fmt(date.today())}  ✅\n\n"
        f"{SEP}\n\n"
        f"  2️⃣ ▸ Fecha  ✅\n"
        f"  3️⃣ ▸ *Años de la pena*  ←  aquí\n\n"
        f"⏳  *¿Cuántos AÑOS de prisión?*\n"
        f"_Escriba `0` si la pena es solo en meses_",
        parse_mode="Markdown"
    )
    return PENA_ANIOS

async def recibir_fecha_sentencia(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    d = parse_fecha(update.message.text)
    if not d:
        await update.message.reply_text(
            f"⚠️  *Formato incorrecto*\n\n"
            f"Use el formato *DD/MM/AAAA*\n"
            f"_Ejemplo: 29/03/2023_",
            parse_mode="Markdown"
        )
        return FECHA_SENTENCIA
    ctx.user_data["fecha_sent"] = d
    await update.message.reply_text(
        f"📅  *Fecha registrada:*\n"
        f"     {fmt(d)}  ✅\n\n"
        f"{SEP}\n\n"
        f"  2️⃣ ▸ Fecha  ✅\n"
        f"  3️⃣ ▸ *Años de la pena*  ←  aquí\n\n"
        f"⏳  *¿Cuántos AÑOS de prisión?*\n"
        f"_Escriba `0` si la pena es solo en meses_",
        parse_mode="Markdown"
    )
    return PENA_ANIOS

async def recibir_pena_anios(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit():
        await update.message.reply_text(
            f"⚠️  Solo ingrese un número. _Ej: `5`_",
            parse_mode="Markdown"
        )
        return PENA_ANIOS
    ctx.user_data["pena_a"] = int(txt)

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("0️⃣", callback_data="mes_0"),
         InlineKeyboardButton("1️⃣", callback_data="mes_1"),
         InlineKeyboardButton("2️⃣", callback_data="mes_2"),
         InlineKeyboardButton("3️⃣", callback_data="mes_3")],
        [InlineKeyboardButton("4️⃣", callback_data="mes_4"),
         InlineKeyboardButton("5️⃣", callback_data="mes_5"),
         InlineKeyboardButton("6️⃣", callback_data="mes_6"),
         InlineKeyboardButton("7️⃣", callback_data="mes_7")],
        [InlineKeyboardButton("8️⃣", callback_data="mes_8"),
         InlineKeyboardButton("9️⃣", callback_data="mes_9"),
         InlineKeyboardButton("🔟", callback_data="mes_10"),
         InlineKeyboardButton("1️⃣1️⃣", callback_data="mes_11")],
    ])
    await update.message.reply_text(
        f"✅  *Años registrados: {ctx.user_data['pena_a']}*\n\n"
        f"{SEP}\n\n"
        f"  3️⃣ ▸ Años  ✅\n"
        f"  4️⃣ ▸ *Meses de la pena*  ←  aquí\n\n"
        f"📆  *¿Cuántos MESES adicionales?*\n"
        f"_Toque el número o escríbalo:_",
        reply_markup=teclado,
        parse_mode="Markdown"
    )
    return PENA_MESES

async def mes_rapido_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    meses = int(query.data.split("_")[1])
    ctx.user_data["pena_m"] = meses
    return await _preguntar_segunda(query.message, ctx)

async def recibir_pena_meses(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit() or int(txt) > 11:
        await update.message.reply_text(
            f"⚠️  Ingrese un número del *0 al 11*.",
            parse_mode="Markdown"
        )
        return PENA_MESES
    ctx.user_data["pena_m"] = int(txt)
    return await _preguntar_segunda(update.message, ctx)

async def _preguntar_segunda(msg, ctx):
    art   = ctx.user_data["art"]
    sup   = ctx.user_data.get("sup82")
    pena_a = ctx.user_data["pena_a"]
    pena_m = ctx.user_data["pena_m"]
    pena  = pena_a + pena_m / 12

    if art == "82":
        if sup in ("mayores70", "enfermo") and pena > 20:
            await msg.reply_text(
                f"❌  *Límite superado*\n\n"
                f"Este supuesto solo aplica para penas\n"
                f"de *hasta 20 años*.\n\n"
                f"Use /calcular para reiniciar.",
                parse_mode="Markdown"
            )
            return ConversationHandler.END
        if sup == "primario" and pena > 10:
            await msg.reply_text(
                f"❌  *Límite superado*\n\n"
                f"El supuesto de delincuente primario\n"
                f"solo aplica para penas de *hasta 10 años*.\n\n"
                f"Use /calcular para reiniciar.",
                parse_mode="Markdown"
            )
            return ConversationHandler.END

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅  Sí — Hay segunda condena",  callback_data="seg_si")],
        [InlineKeyboardButton("❌  No — Solo una condena",     callback_data="seg_no")],
    ])
    await msg.reply_text(
        f"✅  *Meses registrados: {pena_m}*\n\n"
        f"{SEP}\n\n"
        f"  4️⃣ ▸ Meses  ✅\n"
        f"  5️⃣ ▸ *Segunda condena*  ←  aquí\n\n"
        f"📁  *¿Existe una segunda sentencia*\n"
        f"*pendiente de cumplir?*\n\n"
        f"_Ej: suspensión condicional revocada,_\n"
        f"_condena anterior pendiente, etc._",
        reply_markup=teclado,
        parse_mode="Markdown"
    )
    return SEGUNDA_PREGUNTA

async def segunda_pregunta_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "seg_no":
        ctx.user_data["segunda"] = False
        return await generar_resultado(query.message, ctx)

    ctx.user_data["segunda"] = True
    await query.edit_message_text(
        f"✅  *Segunda condena confirmada*\n\n"
        f"{SEP}\n\n"
        f"📌  *Tiempo pendiente de cumplir*\n"
        f"_de la segunda sentencia:_\n\n"
        f"⏳  *¿Cuántos AÑOS pendientes?*\n"
        f"_Escriba `0` si es solo en meses_",
        parse_mode="Markdown"
    )
    return PENA2_ANIOS

async def recibir_pena2_anios(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit():
        await update.message.reply_text(f"⚠️  Solo ingrese un número. _Ej: `1`_", parse_mode="Markdown")
        return PENA2_ANIOS
    ctx.user_data["pena2_a"] = int(txt)

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("0️⃣", callback_data="mes2_0"),
         InlineKeyboardButton("1️⃣", callback_data="mes2_1"),
         InlineKeyboardButton("2️⃣", callback_data="mes2_2"),
         InlineKeyboardButton("3️⃣", callback_data="mes2_3")],
        [InlineKeyboardButton("4️⃣", callback_data="mes2_4"),
         InlineKeyboardButton("5️⃣", callback_data="mes2_5"),
         InlineKeyboardButton("6️⃣", callback_data="mes2_6"),
         InlineKeyboardButton("7️⃣", callback_data="mes2_7")],
        [InlineKeyboardButton("8️⃣", callback_data="mes2_8"),
         InlineKeyboardButton("9️⃣", callback_data="mes2_9"),
         InlineKeyboardButton("🔟", callback_data="mes2_10"),
         InlineKeyboardButton("1️⃣1️⃣", callback_data="mes2_11")],
    ])
    await update.message.reply_text(
        f"✅  *Años 2da condena: {ctx.user_data['pena2_a']}*\n\n"
        f"📆  *¿Cuántos MESES adicionales?*",
        reply_markup=teclado,
        parse_mode="Markdown"
    )
    return PENA2_MESES

async def mes2_rapido_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    meses = int(query.data.split("_")[1])
    ctx.user_data["pena2_m"] = meses
    await query.edit_message_text(
        f"✅  *2da condena: {ctx.user_data['pena2_a']} año(s) y {meses} mes(es)*\n\n"
        f"{SEP}\n\n"
        f"📅  *¿Cuándo inicia la 2da condena?*\n\n"
        f"_Normalmente es el día siguiente al_\n"
        f"_fin de la primera condena._\n\n"
        f"Use el botón o ingrese *DD/MM/AAAA*:",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔄  Calcular automáticamente", callback_data="fecha2_auto")
        ]]),
        parse_mode="Markdown"
    )
    return FECHA_INICIO2

async def recibir_pena2_meses(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit() or int(txt) > 11:
        await update.message.reply_text(f"⚠️  Ingrese un número del *0 al 11*.", parse_mode="Markdown")
        return PENA2_MESES
    ctx.user_data["pena2_m"] = int(txt)
    await update.message.reply_text(
        f"✅  *2da condena: {ctx.user_data['pena2_a']} año(s) y {ctx.user_data['pena2_m']} mes(es)*\n\n"
        f"📅  *¿Cuándo inicia la 2da condena?*\n"
        f"_Use el botón o ingrese DD/MM/AAAA:_",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("🔄  Calcular automáticamente", callback_data="fecha2_auto")
        ]]),
        parse_mode="Markdown"
    )
    return FECHA_INICIO2

async def fecha2_auto_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    fecha_sent = ctx.user_data["fecha_sent"]
    pena_a = ctx.user_data["pena_a"]
    pena_m = ctx.user_data["pena_m"]
    fin_primera = fecha_sent + relativedelta(years=pena_a, months=pena_m)
    inicio2 = fin_primera + relativedelta(days=1)
    ctx.user_data["inicio2"] = inicio2
    await query.edit_message_text(
        f"🔄  *Inicio 2da condena calculado:*\n"
        f"     {fmt(inicio2)}  ✅\n"
        f"_Día siguiente al fin de la primera condena_",
        parse_mode="Markdown"
    )
    return await generar_resultado(query.message, ctx)

async def recibir_fecha_inicio2(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    d = parse_fecha(update.message.text)
    if not d:
        await update.message.reply_text(f"⚠️  Formato incorrecto. Use *DD/MM/AAAA*", parse_mode="Markdown")
        return FECHA_INICIO2
    ctx.user_data["inicio2"] = d
    return await generar_resultado(update.message, ctx)

# ══════════════════════════════════════════════════════════
# ✦ RESULTADO FINAL  —  La pieza principal
# ══════════════════════════════════════════════════════════

async def generar_resultado(msg, ctx):
    art        = ctx.user_data["art"]
    sup82      = ctx.user_data.get("sup82")
    pena_a     = ctx.user_data["pena_a"]
    pena_m     = ctx.user_data["pena_m"]
    fecha_sent = ctx.user_data["fecha_sent"]
    segunda    = ctx.user_data.get("segunda", False)

    if pena_a == 0 and pena_m == 0:
        await msg.reply_text(
            f"❌  La pena no puede ser cero.\nUse /calcular para reiniciar.",
            parse_mode="Markdown"
        )
        return ConversationHandler.END

    fin_primera = fecha_sent + relativedelta(years=pena_a, months=pena_m)
    art_txt = "📗 Artículo 81 — Régimen General" if art == "81" else "📙 Artículo 82 — Régimen Excepcional"

    sup_nombres = {
        "mayores70": "👴 Mayores de 70 años",
        "enfermo":   "🏥 Enfermo grave incurable",
        "primario":  "📋 Delincuente primario",
        None:        ""
    }

    if not segunda:
        fecha_lc, fraccion, _ = calcular_lc(art, sup82, pena_a, pena_m, fecha_sent)
        pct = pct_cumplido(pena_a, pena_m, art, sup82)
        barra = barra_progreso(pct)
        periodo_lc = relativedelta(fin_primera, fecha_lc)

        resumen = (
            f"🏆  *RESULTADO OFICIAL*\n"
            f"{SEP2}\n\n"
            f"{art_txt}\n"
            + (f"     {sup_nombres[sup82]}\n" if sup82 else "")
            + f"\n"
            f"📊  *Pena impuesta:*\n"
            f"     {pena_a} año(s) y {pena_m} mes(es)\n\n"
            f"⚖️  *Fracción aplicada:*\n"
            f"     {fraccion}\n\n"
            f"📈  *Fracción cumplida al obtener LC:*\n"
            f"     {barra}  {pct}%\n\n"
            f"{SEP2}\n\n"
            f"🗓️  *LÍNEA DE TIEMPO*\n"
            f"{SEP}\n\n"
            f"🔵  *Sentencia firme:*\n"
            f"     {fmt(fecha_sent)}\n\n"
            f"🟡  *Libertad Condicional — mínima:*\n"
            f"     *{fmt(fecha_lc)}*\n"
            f"     _Fracción: {fraccion}_\n\n"
            f"🔴  *Fin de condena (excarcelación):*\n"
            f"     {fmt(fin_primera)}\n\n"
            f"⏱️  *Período en Libertad Condicional:*\n"
            f"     {periodo_lc.years} año(s), {periodo_lc.months} mes(es), {periodo_lc.days} día(s)\n\n"
            f"{SEP2}\n\n"
            f"⚠️  _Resultado informativo. Sujeto a_\n"
            f"_resolución judicial y cumplimiento de_\n"
            f"_requisitos (Arts. 81-82, Decreto 130-2017)_\n\n"
            f"💡  _Idea: Abg. Brayan Fernando Padilla R._\n"
            f"{SEP2}"
        )

    else:
        pena2_a = ctx.user_data["pena2_a"]
        pena2_m = ctx.user_data["pena2_m"]
        inicio2 = ctx.user_data.get("inicio2", fin_primera + relativedelta(days=1))
        fin2    = inicio2 + relativedelta(years=pena2_a, months=pena2_m)
        fecha_lc, fraccion, _ = calcular_lc(art, sup82, pena2_a, pena2_m, inicio2)
        pct = pct_cumplido(pena2_a, pena2_m, art, sup82)
        barra = barra_progreso(pct)
        periodo_lc = relativedelta(fin2, fecha_lc)

        resumen = (
            f"🏆  *RESULTADO OFICIAL*\n"
            f"{SEP2}\n\n"
            f"{art_txt}\n"
            + (f"     {sup_nombres[sup82]}\n" if sup82 else "")
            + f"\n"
            f"📌  *1ra condena:*  {pena_a} año(s) y {pena_m} mes(es)\n"
            f"📌  *2da condena:*  {pena2_a} año(s) y {pena2_m} mes(es)\n\n"
            f"⚖️  *Fracción LC sobre 2da condena:*\n"
            f"     {fraccion}\n\n"
            f"📈  *Fracción cumplida al obtener LC:*\n"
            f"     {barra}  {pct}%\n\n"
            f"{SEP2}\n\n"
            f"🗓️  *LÍNEA DE TIEMPO COMPLETA*\n"
            f"{SEP}\n\n"
            f"🔵  *Sentencia firme (1ra):*\n"
            f"     {fmt(fecha_sent)}\n\n"
            f"🟠  *Fin 1ra condena ({pena_a}a {pena_m}m):*\n"
            f"     {fmt(fin_primera)}\n\n"
            f"🟣  *Inicio 2da condena:*\n"
            f"     {fmt(inicio2)}\n\n"
            f"🟡  *Libertad Condicional — mínima:*\n"
            f"     *{fmt(fecha_lc)}*\n"
            f"     _Fracción sobre 2da condena: {fraccion}_\n\n"
            f"🔴  *Fin total de condena:*\n"
            f"     {fmt(fin2)}\n\n"
            f"⏱️  *Período en Libertad Condicional:*\n"
            f"     {periodo_lc.years} año(s), {periodo_lc.months} mes(es), {periodo_lc.days} día(s)\n\n"
            f"{SEP2}\n\n"
            f"⚠️  _Resultado informativo. Sujeto a_\n"
            f"_resolución judicial (Arts. 81-82,_\n"
            f"_Decreto 130-2017)._\n\n"
            f"💡  _Idea: Abg. Brayan Fernando Padilla R._\n"
            f"{SEP2}"
        )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄  Nuevo cálculo",  callback_data="nuevo_calculo")],
        [InlineKeyboardButton("ℹ️  Acerca del bot", callback_data="ver_acerca")],
    ])
    await msg.reply_text(resumen, parse_mode="Markdown", reply_markup=teclado)
    ctx.user_data.clear()
    return ConversationHandler.END

# ══════════════════════════════════════════════════════════
# ✦ HANDLERS EXTRA
# ══════════════════════════════════════════════════════════

async def boton_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "nuevo_calculo":
        await query.message.reply_text(
            f"🔄  Escriba */calcular* para iniciar un nuevo cálculo.",
            parse_mode="Markdown"
        )
    elif query.data == "ver_acerca":
        await acerca(update, ctx)

async def cancelar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text(
        f"❌  *Cálculo cancelado.*\n\n"
        f"Use /calcular cuando desee reiniciar.",
        parse_mode="Markdown"
    )
    return ConversationHandler.END

# ══════════════════════════════════════════════════════════
# ✦ MAIN
# ══════════════════════════════════════════════════════════

def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("Falta la variable TELEGRAM_TOKEN")

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("calcular", calcular_inicio)],
        states={
            ELEGIR_ART:       [CallbackQueryHandler(elegir_art,         pattern="^art_")],
            ELEGIR_SUP82:     [CallbackQueryHandler(elegir_sup82,       pattern="^sup_")],
            FECHA_SENTENCIA:  [
                CallbackQueryHandler(fecha_hoy_callback, pattern="^fecha_hoy$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_fecha_sentencia),
            ],
            PENA_ANIOS:       [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_pena_anios)],
            PENA_MESES:       [
                CallbackQueryHandler(mes_rapido_callback, pattern="^mes_\\d+$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_pena_meses),
            ],
            SEGUNDA_PREGUNTA: [CallbackQueryHandler(segunda_pregunta_cb, pattern="^seg_")],
            PENA2_ANIOS:      [MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_pena2_anios)],
            PENA2_MESES:      [
                CallbackQueryHandler(mes2_rapido_callback, pattern="^mes2_\\d+$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_pena2_meses),
            ],
            FECHA_INICIO2:    [
                CallbackQueryHandler(fecha2_auto_callback, pattern="^fecha2_auto$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_fecha_inicio2),
            ],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("ayuda",  ayuda))
    app.add_handler(CommandHandler("acerca", acerca))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(boton_callback))

    logger.info("🤖 Bot v3.0 iniciado correctamente...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
