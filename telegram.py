"""Envío de mensajes de texto mediante Telegram Bot API."""

import requests


def enviar_mensaje(token: str, chat_id: str, mensaje: str) -> None:
    if not token or not chat_id:
        raise ValueError("Configura TELEGRAM_BOT_TOKEN y TELEGRAM_CHAT_ID en .env.")

    try:
        respuesta = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": mensaje},
            timeout=(10, 30),
        )
        respuesta.raise_for_status()
    except requests.Timeout as error:
        raise ValueError("Telegram agotó el tiempo de espera.") from error
    except requests.HTTPError as error:
        raise ValueError(
            f"Telegram devolvió HTTP {respuesta.status_code}. "
            "Revisa el token, el chat_id y que hayas iniciado el bot."
        ) from error
    except requests.RequestException as error:
        # La URL contiene el token: no mostrar la excepción original.
        raise ValueError("No se pudo completar la conexión con Telegram.") from error

    try:
        contenido = respuesta.json()
    except ValueError as error:
        raise ValueError("Telegram devolvió JSON inválido o vacío.") from error
    if not isinstance(contenido, dict) or contenido.get("ok") is not True:
        raise ValueError("Telegram no confirmó el envío del mensaje.")
