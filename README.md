# ⚖️ Bot de Libertad Condicional — Honduras
## Decreto 130-2017 · Artículos 81 y 82

**Idea:** Abg. Brayan Fernando Padilla Rodríguez  
**Fecha:** 11 de marzo de 2026

---

## 📋 Comandos del Bot

| Comando | Descripción |
|---|---|
| `/start` | Mensaje de bienvenida |
| `/calcular` | Iniciar un nuevo cálculo |
| `/ayuda` | Ver todos los comandos |
| `/acerca` | Información del bot |
| `/cancelar` | Cancelar el cálculo actual |

---

## 🚀 Cómo desplegar en Railway

### Paso 1 — Crear el Bot en Telegram
1. Abra Telegram → busque **@BotFather**
2. Escriba `/newbot`
3. Nombre: `Libertad Condicional Honduras`
4. Usuario: `LibCondHondurasBot` (o el que elija)
5. Guarde el TOKEN que le entrega BotFather

### Paso 2 — Subir a GitHub
1. Cree cuenta en github.com
2. Cree repositorio nuevo llamado `bot-libertad-condicional`
3. Suba estos 3 archivos: `bot.py`, `requirements.txt`, `Procfile`

### Paso 3 — Desplegar en Railway
1. Entre a railway.app
2. New Project → Deploy from GitHub repo
3. Seleccione su repositorio
4. En **Variables** agregue:
   - Nombre: `TELEGRAM_TOKEN`
   - Valor: el token de BotFather
5. Railway desplegará automáticamente

---

## ⚙️ Variables de entorno necesarias

| Variable | Descripción |
|---|---|
| `TELEGRAM_TOKEN` | Token obtenido de @BotFather |

---

## ⚠️ Aviso Legal
Este bot es una herramienta informativa. Los resultados son estimaciones.
Siempre consulte a un abogado penalista habilitado en Honduras.
