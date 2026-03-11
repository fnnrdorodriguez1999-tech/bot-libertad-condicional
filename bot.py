"""Bot de Libertad Condicional Honduras v2.0"""
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

def fmt(d):
    return f"{d.day} de {MESES_ES[d.month-1]} de {d.year} ({d.strftime('%d/%m/%Y')})"

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
            fraccion = "1/2 (mitad)"
            min_dias = total_dias / 2
        elif pena_decimal < 30:
            fraccion = "2/3 (dos tercios)"
            min_dias = total_dias * 2 / 3
        else:
            fraccion = "30 anos fijos"
            min_dias = 30 * 365
    else:
        if sup82 in ("mayores70", "enfermo"):
            return inicio, "Sin fraccion minima"
        else:
            fraccion = "1/3 (un tercio)"
            min_dias = total_dias / 3
    min_a = int(min_dias // 365)
    resto = min_dias - min_a * 365
    min_m = int(resto // 30)
    min_d = round(resto - min_m * 30)
    return inicio + relativedelta(years=min_a, months=min_m, days=min_d), fraccion

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenido al Bot de Libertad Condicional Honduras\n"
        "Decreto 130-2017 - Arts. 81 y 82\n"
        "Idea: Abg. Brayan Fernando Padilla Rodriguez\n\n"
        "Comandos:\n"
        "/calcular - Iniciar calculo\n"
        "/ayuda - Ver ayuda\n"
        "/acerca - Informacion"
    )

async def ayuda(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ayuda - Libertad Condicional\n\n"
        "Como usar:\n"
        "1. /calcular\n"
        "2. Seleccionar articulo\n"
        "3. Ingresar fecha de sentencia\n"
        "4. Ingresar anos y meses de pena\n"
        "5. Indicar si hay segunda condena\n\n"
        "Articulos:\n"
        "Art. 81: Regla general (1/2, 2/3, 30 anos)\n"
        "Art. 82: Mayores 70, enfermo, primario (1/3)"
    )

async def acerca(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = getattr(update, 'message', None) or update.callback_query.message
    await msg.reply_text(
        "Acerca del Bot\n\n"
        "Base legal: Decreto 130-2017\n"
        "Arts. 81 y 82 del Codigo Penal de Honduras\n"
        "Idea: Abg. Brayan Fernando Padilla Rodriguez\n"
        "Creado: 11 de marzo de 2026\n\n"
        "Herramienta informativa. Consulte siempre a un abogado habilitado en Honduras."
    )

async def calcular_inicio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("Art. 81 - Regimen General",     callback_data="art_81")],
        [InlineKeyboardButton("Art. 82 - Regimen Excepcional", callback_data="art_82")],
    ])
    await update.message.reply_text("Paso 1 - Seleccione el articulo:", reply_markup=teclado)
    return ELEGIR_ART

async def elegir_art(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    art = query.data.split("_")[1]
    ctx.user_data["art"] = art
    if art == "82":
        teclado = InlineKeyboardMarkup([
            [InlineKeyboardButton("Mayores de 70 anos",        callback_data="sup_mayores70")],
            [InlineKeyboardButton("Enfermo grave incurable",    callback_data="sup_enfermo")],
            [InlineKeyboardButton("Delincuente primario (1/3)", callback_data="sup_primario")],
        ])
        await query.edit_message_text("Art. 82 - Seleccione el supuesto:", reply_markup=teclado)
        return ELEGIR_SUP82
    ctx.user_data["sup82"] = None
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("Usar fecha de hoy", callback_data="fecha_hoy")]])
    await query.edit_message_text(
        "Art. 81 seleccionado.\n\nPaso 2 - Fecha de sentencia firme\nIngrese DD/MM/AAAA o use el boton:",
        reply_markup=teclado
    )
    return FECHA_SENTENCIA

async def elegir_sup82(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    sup = query.data.split("_", 1)[1]
    ctx.user_data["sup82"] = sup
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("Usar fecha de hoy", callback_data="fecha_hoy")]])
    await query.edit_message_text(
        f"Supuesto seleccionado.\n\nPaso 2 - Fecha de sentencia firme\nIngrese DD/MM/AAAA o use el boton:",
        reply_markup=teclado
    )
    return FECHA_SENTENCIA

async def fecha_hoy_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    ctx.user_data["fecha_sent"] = date.today()
    await query.edit_message_text(
        f"Fecha: {fmt(date.today())}\n\nPaso 3 - Anos de la pena\nIngrese los anos (0 si es solo meses):"
    )
    return PENA_ANIOS

async def recibir_fecha_sentencia(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    d = parse_fecha(update.message.text)
    if not d:
        await update.message.reply_text("Formato incorrecto. Use DD/MM/AAAA (ej: 29/03/2023)")
        return FECHA_SENTENCIA
    ctx.user_data["fecha_sent"] = d
    await update.message.reply_text(
        f"Fecha: {fmt(d)}\n\nPaso 3 - Anos de la pena\nIngrese los anos (0 si es solo meses):"
    )
    return PENA_ANIOS

async def recibir_pena_anios(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit():
        await update.message.reply_text("Ingrese solo un numero. Ej: 5")
        return PENA_ANIOS
    ctx.user_data["pena_a"] = int(txt)
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("0m", callback_data="mes_0"), InlineKeyboardButton("1m", callback_data="mes_1"),
         InlineKeyboardButton("2m", callback_data="mes_2"), InlineKeyboardButton("3m", callback_data="mes_3")],
        [InlineKeyboardButton("4m", callback_data="mes_4"), InlineKeyboardButton("5m", callback_data="mes_5"),
         InlineKeyboardButton("6m", callback_data="mes_6"), InlineKeyboardButton("7m", callback_data="mes_7")],
        [InlineKeyboardButton("8m", callback_data="mes_8"), InlineKeyboardButton("9m", callback_data="mes_9"),
         InlineKeyboardButton("10m", callback_data="mes_10"), InlineKeyboardButton("11m", callback_data="mes_11")],
    ])
    await update.message.reply_text(
        f"Anos: {ctx.user_data['pena_a']}\n\nPaso 4 - Meses de la pena\nSeleccione o escriba (0-11):",
        reply_markup=teclado
    )
    return PENA_MESES

async def mes_rapido_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    meses = int(query.data.split("_")[1])
    ctx.user_data["pena_m"] = meses
    return await _preguntar_segunda(query.message, ctx, editar=False)

async def recibir_pena_meses(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit() or int(txt) > 11:
        await update.message.reply_text("Ingrese un numero del 0 al 11.")
        return PENA_MESES
    ctx.user_data["pena_m"] = int(txt)
    return await _preguntar_segunda(update.message, ctx, editar=False)

async def _preguntar_segunda(msg, ctx, editar=False):
    art = ctx.user_data["art"]
    sup = ctx.user_data.get("sup82")
    pena_a = ctx.user_data["pena_a"]
    pena_m = ctx.user_data["pena_m"]
    pena = pena_a + pena_m / 12
    if art == "82":
        if sup in ("mayores70", "enfermo") and pena > 20:
            await msg.reply_text("Error: Este supuesto solo aplica para penas de hasta 20 anos.\nUse /calcular para reiniciar.")
            return ConversationHandler.END
        if sup == "primario" and pena > 10:
            await msg.reply_text("Error: Este supuesto solo aplica para penas de hasta 10 anos.\nUse /calcular para reiniciar.")
            return ConversationHandler.END
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("Si, hay segunda condena", callback_data="seg_si")],
        [InlineKeyboardButton("No, solo una condena",    callback_data="seg_no")],
    ])
    texto = f"Pena: {pena_a} ano(s) y {pena_m} mes(es)\n\nPaso 5 - Existe una segunda sentencia pendiente de cumplir?"
    await msg.reply_text(texto, reply_markup=teclado)
    return SEGUNDA_PREGUNTA

async def segunda_pregunta_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "seg_no":
        ctx.user_data["segunda"] = False
        return await generar_resultado(query.message, ctx)
    ctx.user_data["segunda"] = True
    await query.edit_message_text(
        "Segunda condena - Tiempo pendiente\n\nIngrese los anos pendientes (0 si es solo meses):"
    )
    return PENA2_ANIOS

async def recibir_pena2_anios(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit():
        await update.message.reply_text("Ingrese solo un numero. Ej: 1")
        return PENA2_ANIOS
    ctx.user_data["pena2_a"] = int(txt)
    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("0m", callback_data="mes2_0"), InlineKeyboardButton("1m", callback_data="mes2_1"),
         InlineKeyboardButton("2m", callback_data="mes2_2"), InlineKeyboardButton("3m", callback_data="mes2_3")],
        [InlineKeyboardButton("4m", callback_data="mes2_4"), InlineKeyboardButton("5m", callback_data="mes2_5"),
         InlineKeyboardButton("6m", callback_data="mes2_6"), InlineKeyboardButton("7m", callback_data="mes2_7")],
        [InlineKeyboardButton("8m", callback_data="mes2_8"), InlineKeyboardButton("9m", callback_data="mes2_9"),
         InlineKeyboardButton("10m", callback_data="mes2_10"), InlineKeyboardButton("11m", callback_data="mes2_11")],
    ])
    await update.message.reply_text(
        f"Anos segunda condena: {ctx.user_data['pena2_a']}\n\nSeleccione los meses pendientes:",
        reply_markup=teclado
    )
    return PENA2_MESES

async def mes2_rapido_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    meses = int(query.data.split("_")[1])
    ctx.user_data["pena2_m"] = meses
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("Calcular automaticamente (recomendado)", callback_data="fecha2_auto")]])
    await query.edit_message_text(
        f"Segunda condena: {ctx.user_data['pena2_a']} ano(s) y {meses} mes(es)\n\n"
        "Fecha de inicio de la segunda condena\n"
        "Normalmente es el dia siguiente al fin de la primera.\n"
        "Use el boton o ingrese DD/MM/AAAA:",
        reply_markup=teclado
    )
    return FECHA_INICIO2

async def recibir_pena2_meses(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if not txt.isdigit() or int(txt) > 11:
        await update.message.reply_text("Ingrese un numero del 0 al 11.")
        return PENA2_MESES
    ctx.user_data["pena2_m"] = int(txt)
    teclado = InlineKeyboardMarkup([[InlineKeyboardButton("Calcular automaticamente (recomendado)", callback_data="fecha2_auto")]])
    await update.message.reply_text(
        f"Segunda condena: {ctx.user_data['pena2_a']} ano(s) y {ctx.user_data['pena2_m']} mes(es)\n\n"
        "Fecha inicio segunda condena - Use el boton o ingrese DD/MM/AAAA:",
        reply_markup=teclado
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
    await query.edit_message_text(f"Inicio segunda condena: {fmt(inicio2)} (automatico)")
    return await generar_resultado(query.message, ctx)

async def recibir_fecha_inicio2(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    d = parse_fecha(update.message.text)
    if not d:
        await update.message.reply_text("Formato incorrecto. Use DD/MM/AAAA")
        return FECHA_INICIO2
    ctx.user_data["inicio2"] = d
    return await generar_resultado(update.message, ctx)

async def generar_resultado(msg, ctx):
    art        = ctx.user_data["art"]
    sup82      = ctx.user_data.get("sup82")
    pena_a     = ctx.user_data["pena_a"]
    pena_m     = ctx.user_data["pena_m"]
    fecha_sent = ctx.user_data["fecha_sent"]
    segunda    = ctx.user_data.get("segunda", False)

    if pena_a == 0 and pena_m == 0:
        await msg.reply_text("La pena no puede ser cero. Use /calcular para reiniciar.")
        return ConversationHandler.END

    fin_primera = fecha_sent + relativedelta(years=pena_a, months=pena_m)
    art_txt = "Art. 81 - Regimen General" if art == "81" else "Art. 82 - Regimen Excepcional"

    if not segunda:
        fecha_lc, fraccion = calcular_lc(art, sup82, pena_a, pena_m, fecha_sent)
        periodo_lc = relativedelta(fin_primera, fecha_lc)
        resumen = (
            f"RESULTADO - LIBERTAD CONDICIONAL\n"
            f"{'='*30}\n\n"
            f"{art_txt}\n"
            f"Pena: {pena_a} ano(s) y {pena_m} mes(es)\n"
            f"Fraccion aplicada: {fraccion}\n\n"
            f"LINEA DE TIEMPO\n"
            f"{'─'*30}\n\n"
            f"Sentencia firme:\n   {fmt(fecha_sent)}\n\n"
            f"LIBERTAD CONDICIONAL (minimo):\n   {fmt(fecha_lc)}\n"
            f"   Fraccion: {fraccion}\n\n"
            f"Fin de condena:\n   {fmt(fin_primera)}\n"
            f"   Periodo en LC: {periodo_lc.years}a {periodo_lc.months}m {periodo_lc.days}d\n\n"
            f"{'='*30}\n"
            f"Resultado informativo. Sujeto a resolucion judicial\n"
            f"y cumplimiento de Arts. 81-82, Decreto 130-2017.\n"
            f"Idea: Abg. Brayan Fernando Padilla Rodriguez"
        )
    else:
        pena2_a = ctx.user_data["pena2_a"]
        pena2_m = ctx.user_data["pena2_m"]
        inicio2 = ctx.user_data.get("inicio2", fin_primera + relativedelta(days=1))
        fin2    = inicio2 + relativedelta(years=pena2_a, months=pena2_m)
        fecha_lc, fraccion = calcular_lc(art, sup82, pena2_a, pena2_m, inicio2)
        periodo_lc = relativedelta(fin2, fecha_lc)
        resumen = (
            f"RESULTADO - LIBERTAD CONDICIONAL\n"
            f"{'='*30}\n\n"
            f"{art_txt}\n\n"
            f"1ra condena: {pena_a} ano(s) y {pena_m} mes(es)\n"
            f"2da condena: {pena2_a} ano(s) y {pena2_m} mes(es) pendientes\n"
            f"Fraccion LC: {fraccion} (sobre 2da condena)\n\n"
            f"LINEA DE TIEMPO\n"
            f"{'─'*30}\n\n"
            f"Sentencia firme (1ra condena):\n   {fmt(fecha_sent)}\n\n"
            f"Fin 1ra condena ({pena_a}a {pena_m}m):\n   {fmt(fin_primera)}\n\n"
            f"Inicio 2da condena:\n   {fmt(inicio2)}\n\n"
            f"LIBERTAD CONDICIONAL (minimo):\n   {fmt(fecha_lc)}\n"
            f"   Fraccion sobre 2da condena: {fraccion}\n\n"
            f"Fin total de condena:\n   {fmt(fin2)}\n"
            f"   Periodo en LC: {periodo_lc.years}a {periodo_lc.months}m {periodo_lc.days}d\n\n"
            f"{'='*30}\n"
            f"Resultado informativo. Sujeto a resolucion judicial.\n"
            f"Idea: Abg. Brayan Fernando Padilla Rodriguez"
        )

    teclado = InlineKeyboardMarkup([
        [InlineKeyboardButton("Nuevo calculo", callback_data="nuevo_calculo")],
        [InlineKeyboardButton("Acerca del bot", callback_data="ver_acerca")],
    ])
    await msg.reply_text(resumen, reply_markup=teclado)
    ctx.user_data.clear()
    return ConversationHandler.END

async def boton_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "nuevo_calculo":
        await query.message.reply_text("Use /calcular para iniciar un nuevo calculo.")
    elif query.data == "ver_acerca":
        await acerca(update, ctx)

async def cancelar(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("Calculo cancelado. Use /calcular para reiniciar.")
    return ConversationHandler.END

def main():
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TOKEN:
        raise ValueError("Falta TELEGRAM_TOKEN")
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("calcular", calcular_inicio)],
        states={
            ELEGIR_ART:       [CallbackQueryHandler(elegir_art, pattern="^art_")],
            ELEGIR_SUP82:     [CallbackQueryHandler(elegir_sup82, pattern="^sup_")],
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
    logger.info("Bot v2.0 iniciado correctamente...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
