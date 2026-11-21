#!/usr/bin/env python3
"""Amostras oficiais Azure Speech para Joca Estuda.

Variáveis exigidas:
  AZURE_SPEECH_KEY (guardar em GitHub Actions Secret)
  AZURE_SPEECH_REGION (ex.: brazilsouth, conforme recurso)

Usa a API REST oficial, nunca envia chaves ao navegador.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import os
import sys
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "vozes"
OUT.mkdir(parents=True, exist_ok=True)

VOICES = [
    {
        "who": "joruto",
        "name": "pt-BR-FabioNeural",
        "rate": "+4%",
        "pitch": "+2%",
        "text": ("Sensei, se eu lançar este dado, vai sair o número seis? "
                 "Eu quero descobrir como calcular a chance de acertar!"),
    },
    {
        "who": "sensei",
        "name": "pt-BR-AntonioNeural",
        "rate": "-10%",
        "pitch": "-3%",
        "text": ("Ninguém pode saber o resultado antes de lançar. "
                 "Num dado equilibrado, existem seis resultados possíveis. "
                 "A chance de sair seis é uma em seis."),
    },
]


def speech_request(voice, key, region):
    ssml = (
        '<speak version="1.0" '
        'xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="pt-BR">'
        f'<voice name="{voice["name"]}">'
        f'<prosody rate="{voice["rate"]}" pitch="{voice["pitch"]}">'
        f'{escape(voice["text"])}'
        '</prosody></voice></speak>'
    )
    url = f"https://{region}.tts.speech.microsoft.com/cognitiveservices/v1"
    req = urllib.request.Request(
        url,
        data=ssml.encode("utf-8"),
        method="POST",
        headers={
            "Ocp-Apim-Subscription-Key": key,
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "JocaEstuda/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        audio = resp.read()
    if len(audio) < 500:
        raise RuntimeError("Audio returned unexpectedly short")
    return audio


def main():
    key = os.environ.get("AZURE_SPEECH_KEY", "").strip()
    region = os.environ.get("AZURE_SPEECH_REGION", "").strip().lower()
    if not key or not region:
        sys.exit("Configure AZURE_SPEECH_KEY e AZURE_SPEECH_REGION nos GitHub Actions Secrets.")
    if not all(c.isalnum() or c == "-" for c in region):
        sys.exit("Região do Azure inválida.")
    for voice in VOICES:
        try:
            audio = speech_request(voice, key, region)
        except urllib.error.HTTPError as err:
            sys.exit(f"Azure Speech retornou HTTP {err.code} para {voice['who']}. Confira chave, região e limite do recurso.")
        except urllib.error.URLError:
            sys.exit("Não foi possível conectar ao Azure Speech. Confira a conectividade do runner.")
        out = OUT / f"amostra_{voice['who']}.mp3"
        out.write_bytes(audio)
        print(f"OK: {out.name}, {len(audio)} bytes, voz {voice['name']}")
    print("Amostras prontas para escuta e aprovação antes da troca da voz do vídeo.")


if __name__ == "__main__":
    main()
