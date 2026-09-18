<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
[![Python][python-shield]][python-url]
[![Platform][platform-shield]][ubuntu-url]
[![Telegram][telegram-shield]][telegram-url]

<!-- PROJECT LOGO -->
<br />
<div align="center">

<img width="100" height="100" alt="cnel-ep-bot" src="https://github.com/user-attachments/assets/a7627a08-915f-403e-ab94-fa92062b150b" />
  <h3 align="center">CNEL Monitor ⚡</h3>

  <p align="center">
    Consulta el estado de tu cuenta de CNEL Ecuador y recibe el resultado en Telegram.
    <br />
    Sin frameworks, sin base de datos, sin Docker: solo Python.
  </p>
</div>

<!-- ABOUT THE PROJECT -->
## Acerca del proyecto

Este proyecto consulta el portal de servicios en línea de CNEL con una petición POST, valida la respuesta y te envía por Telegram la cuenta, los meses pendientes y la deuda actual.

Por qué este proyecto:

* Cada ejecución envía la información actual, la revisas visualmente y decides qué hacer.
* Si la consulta falla, muestra el error y no envía datos incorrectos.
* Es pequeño y mantenible: tres módulos (`cnel.py`, `telegram.py`, `main.py`) y dos dependencias externas.
* Lo ejecutas manualmente cuando quieras o lo automatizas con `cron` en Ubuntu.

<!-- GETTING STARTED -->
## Primeros pasos

Para tener una copia local funcionando sigue estos pasos.

### Prerrequisitos

* Ubuntu con Python 3.12+ y el paquete `python3-venv`.
  ```sh
  sudo apt install python3-venv
  ```
  > Si tu Python pide su paquete `venv` específico, instala el que indique (por ejemplo `python3.14-venv`).
* Tu número de cuenta CNEL y el tipo de consulta. Tipos permitidos por CNEL:
  | Valor | Significado |
  |---|---|
  | `CED_RUC` | Cédula o RUC |
  | `CTA` | Cuenta contrato |
  | `CUEN` | Código Único Eléctrico Nacional |
* Un bot de Telegram.

### Instalación

1. Entra a la carpeta del proyecto
   ```sh
   cd cnel-monitor
   ```
2. Crea el entorno virtual e instala las dependencias
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```
3. Crea tu archivo de configuración a partir de la plantilla
   ```sh
   cp .env.example .env
   ```
4. Edita `.env` con tus valores reales
   ```dotenv
   CNEL_CUENTA=tu_numero_de_cuenta
   CNEL_TIPO_CONSULTA=valor_exacto_utilizado_por_CNEL
   TELEGRAM_BOT_TOKEN=token_entregado_por_BotFather
   TELEGRAM_CHAT_ID=id_del_chat
   ```

### Configurar Telegram

1. Abre **@BotFather** en Telegram, envía `/newbot` y sigue sus instrucciones.
2. Abre el chat con tu bot, pulsa **Iniciar** y envíale un mensaje (`Hola`).
3. En tu navegador abre esta dirección, sustituyendo `<TOKEN>` por el token completo del bot:
   ```text
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
4. Copia el valor de `message.chat.id` → ese es tu `TELEGRAM_CHAT_ID` (no uses `update_id` ni los números iniciales del token).
5. Si `result` sale vacío (`[]`), envía otro mensaje al bot y recarga la página.

> 🔒 No compartas tu `.env` con nadie: contiene tu token. Si un token se filtra, revócalo con `@BotFather` → `/revoke`.

<!-- USAGE EXAMPLES -->
## Uso

Con el entorno virtual activado:

Verificar que Telegram funciona (no consulta CNEL):

```sh
python main.py --probar-telegram
```

Deberías recibir: `Prueba CNEL Monitor: Telegram funciona.`

Consulta real + envío a Telegram:

```sh
python main.py
```

Mensaje que recibirás en cada ejecución:

```text
Estado actual CNEL

Cuenta: 123456789012
Meses pendientes: 7
Deuda actual: $103.47
```

**Automatización opcional con `cron`:** si quieres que se ejecute solo (por ejemplo, una vez al mes, el día 1 a las 9:00 a. m. hora Ecuador), agrega una entrada como esta, ajustando rutas y fecha a tu gusto:

```cron
TZ=America/Guayaquil
0 9 1 * * /ruta/al/proyecto/.venv/bin/python /ruta/al/proyecto/main.py >> /ruta/al/proyecto/cron.log 2>&1
```

```sh
(crontab -l 2>/dev/null | grep -v "cnel-monitor/main.py"; echo "TZ=America/Guayaquil"; echo "0 9 1 * * $PWD/.venv/bin/python $PWD/main.py >> $PWD/cron.log 2>&1") | crontab -
crontab -l
```

> Si la PC está apagada o suspendida a la hora programada, esa ejecución se pierde (cron no reintenta). Revisa `cron.log` si alguna vez no llega el mensaje.

<!-- LICENSE -->
## Licencia

Este proyecto es de código abierto bajo la licencia [MIT](https://github.com/7R0N1X/cnel-monitor/blob/main/LICENSE)

<!-- MARKDOWN LINKS & IMAGES -->
[python-shield]: https://img.shields.io/badge/python-3.12%2B-blue?style=for-the-badge&logo=python&logoColor=white
[python-url]: https://www.python.org/
[platform-shield]: https://img.shields.io/badge/platform-ubuntu-orange?style=for-the-badge&logo=ubuntu&logoColor=white
[ubuntu-url]: https://ubuntu.com/
[telegram-shield]: https://img.shields.io/badge/telegram-bot_api-blue?style=for-the-badge&logo=telegram&logoColor=white
[telegram-url]: https://core.telegram.org/bots/api
