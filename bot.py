"""
╔══════════════════════════════════════════════════════╗
║   Bot de Libertad Condicional — Honduras             ║
║   Decreto 130-2017 · Arts. 81 y 82                  ║
║   Idea: Abg. Brayan Fernando Padilla Rodríguez      ║
╚══════════════════════════════════════════════════════╝
"""

import os
import logging
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, filters, ContextTypes
)

# ── Logging ───────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s — %(name)s — %(levelname)s — %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ── Estados de la conversación ────────────────────────────
ELEGIR_ARTICULO, ELEGIR_SUP82, INGRESAR_ANIOS, INGRESAR_MESES, \
INGRESAR_DIAS, INGRESAR_FECHA = range(6)

# ── Helpers de cálculo ────────────────────────────────────
def calcular_libertad(art, sup82, pena_a, pena_m, pena_d, fecha_sent):
    """Calcula la fecha de libertad condicional según Arts. 81 y 82."""
    pena_decimal = pena_a + pena_m / 12 + pena_d / 365
    total_dias   = pena_a * 365 + pena_m * 30 + pena_d

    if art == "81":
        if pena_decimal <= 15:
            fraccion   = "½ (mitad)"
            min_dias   = total_dias / 2
            tramo      = "Tramo 1 — Pena ≤ 15 años"
        elif pena_decimal < 30:
            fraccion   = "⅔ (dos tercios)"
            min_dias   = total_dias * 2 / 3
            tramo      = "Tramo 2 — Pena entre 15 y 30 años"
        else:
            fraccion   = "30 años fijos"
            min_dias   = 30 * 365
            tramo      = "Tramo 3 — Pena ≥ 30 años"
    else:
        if sup82 in ("mayores70", "enfermo"):
            fraccion   = "Sin fracción mínima"
            min_dias   = 0
            tramo      = "Mayores de 70 años" if sup82 == "mayores70" else "Enfermo grave incurable"
        else:
            fraccion   = "⅓ (un tercio)"
            min_dias   = total_dias / 3
            tramo      = "Delincuente primario"

    # Convertir días mínimos a años/meses/días
    min_a = int(min_dias // 365)
    resto = min_dias - min_a * 365
    min_m = int(resto // 30)
    min_d = round(resto - min_m * 30)

    # Calcular fechas
    fecha_lib = fecha_sent + relativedelta(years=min_a, months=min_m, days=min_d)
    fecha_fin = fecha_sent + relativedelta(years=pena_a, months=pena_m, days=pena_d)

    # Período de libertad condicional
    diff_per = relativedelta(fecha_fin, fecha_lib)

    # Porcentaje
    pct = round((min_dias / total_dias * 100) if total_dias > 0 else 0)

    return {
        "fraccion"  : fraccion,
        "tramo"     : tramo,
        "min_a"     : min_a,
        "min_m"     : min_m,
        "min_d"     : min_d,
        "pct"       : pct,
        "fecha_lib" : fecha_lib,
        "fecha_fin" : fecha_fin,
        "periodo_a" : diff_per.years,
        "periodo_m" : diff_per.months,
        "periodo_d" : diff_per.days,
    }

def fmt_fecha(d):
    meses = ["enero","febrero","marzo","abril","mayo","junio",
             "julio","agosto","septiembre","octubre","noviembre","diciembre"]
    return f"{d.day} de {meses[d.month-1]} de {d.year}"

def barra_progreso(pct):
    filled = round(pct / 10)
    return "█" * filled + "░" * (10 - filled)

# ── /start ────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    texto = (
        "⚖️ *Bienvenido al Bot de Libertad Condicional*\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "📋 *Decreto N.º 130\\-2017 \\— Honduras*\n"
        "📌 Artículos 81 y 82 del Código Penal\n\n"
        "_Idea del Abg\\. Brayan Fernando Padilla Rodríguez_\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        "Use /calcular para iniciar el cálculo\n"
        "Use /ayuda para ver todos los comandos"
    )
    await update.message.reply_text(texto, parse_mode="MarkdownV2")

# ── /ayuda ────────────────────────────────────────────────
async def ayuda(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    texto = (
        "⚖️ *Comandos disponibles*\n\n"
        "• /calcular — Iniciar un nuevo cálculo\n"
        "• /ayuda — Ver esta ayuda\n"
        "• /acerca — Información del bot\n\n"
        "*¿Qué calcula este bot?*\n"
        "Calcula la fecha mínima en la que un penado puede solicitar "
        "la libertad condicional según los Arts\\. 81 y 82 del "
        "Código Penal de Honduras \\(Decreto 130\\-2017\\)\\."
    )
    await update.message.reply_text(texto, parse_mode="MarkdownV2")

# ── /acerca ───────────────────────────────────────────────
async def acerca(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    texto = (
        "⚖️ *Acerca de este Bot*\n\n"
        "🏛️ *Base legal:* Decreto N\\.º 130\\-2017\n"
        "📖 *Artículos:* 81 y 82 del Código Penal de Honduras\n\n"
        "💡 *Idea y concepto:*\n"
        "_Abg\\. Brayan Fernando Padilla Rodríguez_\n\n"
        "📅 *Fecha de creación:* 11 de marzo de 2026\n\n"
        "⚠️ _Este bot es una herramienta informativa\\. "
        "Los resultados son estimaciones\\. Siempre consulte a un "
        "abogado penalista habilitado en Honduras\\._"
    )
    await update.message.reply_text(texto, parse_mode="MarkdownV2")

# ── CONVERSACIÓN: Paso 1 — Elegir artículo ───────────────
async def calcular_inicio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("📗 Artículo 81 — Régimen General",    callback_data="art_81")],
        [InlineKeyboardButton("📙 Artículo 82 — Régimen Excepcional", callback_data="art_82")],
    ])
    await update.message.reply_text(
        "⚖️ *Paso 1 de 5 — Artículo aplicable*\n\n"
        "Seleccione el artículo que corresponde al caso:",
        reply_markup=teclado,
        parse_mode="Markdown"
    )
    return ELEGIR_ARTICULO

# ── Paso 1: Respuesta artículo ────────────────────────────
async def elegir_articulo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    art = query.data.split("_")[1]
    ctx.user_data["articulo"] = art

    if art == "82":
        teclado = InlineKeyboardMarkup([
            [InlineKeyboardButton("👴 Mayores de 70 años",          callback_data="sup_mayores70")],
            [InlineKeyboardButton("🏥 Enfermo grave incurable",      callback_data="sup_enfermo")],
            [InlineKeyboardButton("📗 Delincuente primario (1/3)",   callback_data="sup_primario")],
        ])
        await query.edit_message_text(
            "📙 *Artículo 82 — Paso 2 de 5*\n\n"
            "Seleccione el supuesto excepcional:",
            reply_markup=teclado,
            parse_mode="Markdown"
        )
        return ELEGIR_SUP82
    else:
        ctx.user_data["sup82"] = None
        await query.edit_message_text(
            "📗 *Artículo 81 — Paso 2 de 5*\n\n"
            "Ingrese los *años* de la pena de prisión:\n\n"
            "_Escriba solo el número. Ej: `15` o `0` si no hay años_",
            parse_mode="Markdown"
        )
        return INGRESAR_ANIOS

# ── Paso 2: Supuesto Art. 82 ──────────────────────────────
async def elegir_sup82(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sup = query.data.split("_", 1)[1]
    ctx.user_data["sup82"] = sup

    limites = {
        "mayores70": "⚠️ _Recuerde: la pena no debe superar los 20 años_",
        "enfermo":   "⚠️ _Recuerde: la pena no debe superar los 20 años_",
        "primario":  "⚠️ _Recuerde: la pena no debe superar los 10 años_",
    }
    nombres = {
        "mayores70": "👴 Mayores de 70 años",
        "enfermo":   "🏥 Enfermo grave incurable",
        "primario":  "📗 Delincuente primario",
    }

    await query.edit_message_text(
        f"📙 *Art. 82 — {nombres[sup]}*\n"
        f"{limites[sup]}\n\n"
        "➡️ *Paso 3 de 5*\n\n"
        "Ingrese los *años* de la pena de prisión:\n\n"
        "_Escriba solo el número. Ej: `8` o `0` si no hay años_",
        parse_mode="Markdown"
    )
    return INGRESAR_ANIOS

# ── Paso 3: Años ──────────────────────────────────────────
async def ingresar_anios(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit():
        await update.message.reply_text("⚠️ Por favor ingrese solo un número entero. Ej: `10`", parse_mode="Markdown")
        return INGRESAR_ANIOS
    ctx.user_data["pena_a"] = int(txt)
    await update.message.reply_text(
        "✅ Años registrados.\n\n"
        "➡️ *Paso 4 de 5*\n\n"
        "Ingrese los *meses* de la pena \\(0 a 11\\):\n\n"
        "_Ej: `6` o `0` si no hay meses adicionales_",
        parse_mode="MarkdownV2"
    )
    return INGRESAR_MESES

# ── Paso 4: Meses ─────────────────────────────────────────
async def ingresar_meses(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit() or int(txt) > 11:
        await update.message.reply_text("⚠️ Ingrese un número entre 0 y 11.", parse_mode="Markdown")
        return INGRESAR_MESES
    ctx.user_data["pena_m"] = int(txt)
    await update.message.reply_text(
        "✅ Meses registrados.\n\n"
        "➡️ *Paso 4b de 5*\n\n"
        "Ingrese los *días* de la pena \\(0 a 30\\):\n\n"
        "_Ej: `15` o `0` si no hay días adicionales_",
        parse_mode="MarkdownV2"
    )
    return INGRESAR_DIAS

# ── Paso 5: Días ──────────────────────────────────────────
async def ingresar_dias(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit() or int(txt) > 30:
        await update.message.reply_text("⚠️ Ingrese un número entre 0 y 30.", parse_mode="Markdown")
        return INGRESAR_DIAS
    ctx.user_data["pena_d"] = int(txt)

    # Validar límites art. 82
    art  = ctx.user_data["articulo"]
    sup  = ctx.user_data.get("sup82")
    pa   = ctx.user_data["pena_a"]
    pm   = ctx.user_data["pena_m"]
    pd   = int(txt)
    pena = pa + pm/12 + pd/365

    if art == "82":
        if sup in ("mayores70","enfermo") and pena > 20:
            await update.message.reply_text(
                "❌ *Error:* Este supuesto solo aplica para penas de *hasta 20 años*\\.\n\n"
                "Use /calcular para intentar de nuevo\\.",
                parse_mode="MarkdownV2"
            )
            return ConversationHandler.END
        if sup == "primario" and pena > 10:
            await update.message.reply_text(
                "❌ *Error:* El supuesto de delincuente primario solo aplica para penas de *hasta 10 años*\\.\n\n"
                "Use /calcular para intentar de nuevo\\.",
                parse_mode="MarkdownV2"
            )
            return ConversationHandler.END

    await update.message.reply_text(
        "✅ Pena registrada.\n\n"
        "➡️ *Paso 5 de 5 — Fecha de sentencia*\n\n"
        "Ingrese la fecha en que la sentencia adquirió firmeza:\n\n"
        "📅 Formato: `DD/MM/AAAA`\n"
        "_Ej: `15/03/2024`_",
        parse_mode="Markdown"
    )
    return INGRESAR_FECHA

# ── Paso 6: Fecha y resultado final ───────────────────────
async def ingresar_fecha(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    try:
        fecha_sent = datetime.strptime(txt, "%d/%m/%Y").date()
    except ValueError:
        await update.message.reply_text(
            "⚠️ Formato de fecha incorrecto\\. Use `DD/MM/AAAA`\\.\n_Ej: `15/03/2024`_",
            parse_mode="MarkdownV2"
        )
        return INGRESAR_FECHA

    # Recoger datos
    art    = ctx.user_data["articulo"]
    sup    = ctx.user_data.get("sup82")
    pena_a = ctx.user_data["pena_a"]
    pena_m = ctx.user_data["pena_m"]
    pena_d = ctx.user_data["pena_d"]

    if pena_a == 0 and pena_m == 0 and pena_d == 0:
        await update.message.reply_text("❌ La pena no puede ser cero. Use /calcular para reiniciar.")
        return ConversationHandler.END

    # Calcular
    r = calcular_libertad(art, sup, pena_a, pena_m, pena_d, fecha_sent)

    # Nombres legibles
    art_nom = "Artículo 81 — Régimen General" if art=="81" else "Artículo 82 — Régimen Excepcional"
    barra   = barra_progreso(r["pct"])

    # Resumen de pena
    pena_txt = f"{pena_a}a {pena_m}m {pena_d}d"

    # Construir mensaje de resultado
    resultado = (
        f"⚖️ *RESULTADO — LIBERTAD CONDICIONAL*\n"
        f"{'━'*30}\n\n"
        f"📋 *{art_nom}*\n"
        f"📌 *Supuesto:* {r['tramo']}\n"
        f"⚖️ *Fracción aplicada:* {r['fraccion']}\n\n"
        f"{'─'*30}\n"
        f"📊 *PENA IMPUESTA:* `{pena_txt}`\n"
        f"⏳ *Tiempo mínimo a cumplir:*\n"
        f"   `{r['min_a']} años, {r['min_m']} meses y {r['min_d']} días`\n\n"
        f"📈 *Progreso:* {barra} {r['pct']}%\n\n"
        f"{'─'*30}\n"
        f"🗓️ *LÍNEA DE TIEMPO*\n\n"
        f"🔵 *Inicio (sentencia firme):*\n"
        f"   {fmt_fecha(fecha_sent)}\n\n"
        f"🟡 *Fecha mínima — Libertad Condicional:*\n"
        f"   *{fmt_fecha(r['fecha_lib'])}*\n\n"
        f"🔴 *Fin de condena (extinción):*\n"
        f"   {fmt_fecha(r['fecha_fin'])}\n\n"
        f"📅 *Período en lib. condicional:*\n"
        f"   `{r['periodo_a']} año(s), {r['periodo_m']} mes(es) y {r['periodo_d']} día(s)`\n\n"
        f"{'━'*30}\n"
        f"⚠️ _Resultado informativo. Sujeto a resolución judicial "
        f"y cumplimiento de requisitos de conducta, reinserción y "
        f"responsabilidad civil \\(Arts\\. 81\\-82, Decreto 130\\-2017\\)\\._\n\n"
        f"_Idea: Abg\\. Brayan Fernando Padilla Rodríguez_"
    )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Nuevo cálculo", callback_data="nuevo_calculo")],
        [InlineKeyboardButton("ℹ️ Acerca del bot",  callback_data="ver_acerca")],
    ])

    await update.message.reply_text(resultado, parse_mode="MarkdownV2", reply_markup=teclado)
    ctx.user_data.clear()
    return ConversationHandler.END

# ── Botones de resultado ──────────────────────────────────
async def boton_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "nuevo_calculo":
        await query.message.reply_text("Use /calcular para iniciar un nuevo cálculo\\.", parse_mode="MarkdownV2")
    elif query.data == "ver_acerca":
        await acerca(query, ctx)

# ── Cancelar ──────────────────────────────────────────────
async def cancelar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("❌ Cálculo cancelado. Use /calcular para iniciar de nuevo.")
    return ConversationHandler.END

# ── Main ──────────────────────────────────────────────────
def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("❌ Falta la variable de entorno TELEGRAM_TOKEN")

    app = Application.builder().token(TOKEN).build()

    # Conversación principal
    conv = ConversationHandler(
        entry_points=[CommandHandler("calcular", calcular_inicio)],
        states={
            ELEGIR_ARTICULO : [CallbackQueryHandler(elegir_articulo, pattern="^art_")],
            ELEGIR_SUP82    : [CallbackQueryHandler(elegir_sup82,    pattern="^sup_")],
            INGRESAR_ANIOS  : [MessageHandler(filters.TEXT & ~filters.COMMAND, ingresar_anios)],
            INGRESAR_MESES  : [MessageHandler(filters.TEXT & ~filters.COMMAND, ingresar_meses)],
            INGRESAR_DIAS   : [MessageHandler(filters.TEXT & ~filters.COMMAND, ingresar_dias)],
            INGRESAR_FECHA  : [MessageHandler(filters.TEXT & ~filters.COMMAND, ingresar_fecha)],
        },
        fallbacks=[CommandHandler("cancelar", cancelar)],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start",   start))
    app.add_handler(CommandHandler("ayuda",   ayuda))
    app.add_handler(CommandHandler("acerca",  acerca))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(boton_callback))

    logger.info("🤖 Bot iniciado correctamente...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
