"""Consulta CNEL y envía la información actual por Telegram en cada ejecución."""

import argparse
import json
import os
from pathlib import Path
import sys

from dotenv import load_dotenv

from cnel import consultar_cuenta
from telegram import enviar_mensaje


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--probar-telegram", action="store_true",
        help="Envía un mensaje de prueba sin consultar CNEL.",
    )
    argumentos = parser.parse_args()
    load_dotenv(Path(__file__).resolve().parent / ".env")
    token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()

    if argumentos.probar_telegram:
        try:
            enviar_mensaje(token, chat_id, "Prueba CNEL Monitor: Telegram funciona.")
        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
        print("Mensaje de prueba enviado a Telegram.")
        return 0

    numero_cuenta = os.getenv("CNEL_CUENTA", "").strip()
    tipo_consulta = os.getenv("CNEL_TIPO_CONSULTA", "").strip()

    if not numero_cuenta or not tipo_consulta:
        print(
            "Error: configura CNEL_CUENTA y CNEL_TIPO_CONSULTA en .env "
            "o en las variables de entorno.",
            file=sys.stderr,
        )
        return 1

    try:
        estado_actual = consultar_cuenta(numero_cuenta, tipo_consulta)
        print("Respuesta de CNEL validada:")
        print(json.dumps(estado_actual, ensure_ascii=False, indent=4))

        mensaje = (
            "Estado actual CNEL\n\n"
            f"Cuenta: {estado_actual['cuenta']}\n"
            f"Meses pendientes: {estado_actual['meses']}\n"
            f"Deuda actual: ${estado_actual['deuda']:.2f}"
        )
        enviar_mensaje(token, chat_id, mensaje)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    print("Información actual enviada a Telegram.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
