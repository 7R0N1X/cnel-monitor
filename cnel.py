"""Consulta y validación de los datos publicados por CNEL."""

import math

import requests


URL_CONSULTA = (
    "https://serviciosenlinea.cnelep.gob.ec"
    "/services/consulta-cuen-api/cuentas/consultar"
)

HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json",
    "Origin": "https://serviciosenlinea.cnelep.gob.ec",
    "Referer": "https://serviciosenlinea.cnelep.gob.ec/consulta-cuen/",
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
}


def consultar_cuenta(numero_cuenta: str, tipo_consulta: str) -> dict:
    """Devuelve cuenta, deuda y meses; los errores nunca representan deuda cero."""
    try:
        respuesta_http = requests.post(
            URL_CONSULTA,
            json={"consulta": numero_cuenta, "tipo": tipo_consulta},
            headers=HEADERS,
            timeout=(10, 30),  # Tiempo de conexión y de lectura, en segundos.
        )
    except requests.Timeout as error:
        raise ValueError("CNEL agotó el tiempo de espera.") from error
    except requests.RequestException as error:
        raise ValueError("No se pudo completar la conexión con CNEL.") from error

    print(f"CNEL: HTTP {respuesta_http.status_code}", flush=True)
    try:
        respuesta_http.raise_for_status()
    except requests.HTTPError as error:
        raise ValueError(
            f"CNEL devolvió un error HTTP {respuesta_http.status_code}."
        ) from error

    if not respuesta_http.text.strip():
        raise ValueError("CNEL devolvió una respuesta vacía.")

    try:
        contenido = respuesta_http.json()
    except ValueError as error:
        raise ValueError("CNEL devolvió JSON inválido.") from error

    if not isinstance(contenido, dict):
        raise ValueError("La respuesta de CNEL debe ser un objeto JSON.")

    respuesta = contenido.get("respuesta")
    if not isinstance(respuesta, dict) or respuesta.get("tipo") != "OK":
        raise ValueError("CNEL no devolvió respuesta.tipo igual a OK.")

    datos = respuesta.get("data")
    if not isinstance(datos, list) or not datos:
        raise ValueError("CNEL devolvió respuesta.data vacío o inválido.")

    # En esta prueba se utiliza el primer elemento del listado de CNEL.
    cuenta = datos[0]
    if not isinstance(cuenta, dict):
        raise ValueError("El primer elemento de respuesta.data es inválido.")

    numero = cuenta.get("cuentaContrato")
    deuda = cuenta.get("deuda")
    meses = cuenta.get("meses")

    if not isinstance(numero, str) or not numero.strip():
        raise ValueError("CNEL devolvió cuentaContrato ausente o inválida.")
    if type(deuda) not in (int, float) or not math.isfinite(deuda):
        raise ValueError("CNEL devolvió deuda ausente o inválida.")
    if type(meses) is not int or meses < 0:
        raise ValueError("CNEL devolvió meses ausente o inválido.")

    return {"cuenta": numero, "deuda": deuda, "meses": meses}
