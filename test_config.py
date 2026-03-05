#!/usr/bin/env python3
"""
Script para verificar a configuração do Google Login no backend
Sem precisar de token real
"""

import os
from datetime import datetime

GOOGLE_DEFAULT_CLIENT_ID = "690521786732-6rh6blrhbu1ndqrpc2513mlv3mvrdacg.apps.googleusercontent.com"

print("\n" + "="*70)
print("VERIFICAÇÃO DE CONFIGURAÇÃO - Google Login Backend")
print("="*70)

print("\n1. Client ID Configurado:")
print(f"   {GOOGLE_DEFAULT_CLIENT_ID}")

print("\n2. Variável de Ambiente GOOGLE_CLIENT_IDS:")
allowed = os.getenv("GOOGLE_CLIENT_IDS")
if allowed:
    allowed_ids = {item.strip() for item in allowed.split(",") if item.strip()}
    print(f"   ✓ Configurada:")
    for cid in allowed_ids:
        print(f"     - {cid}")
else:
    print(f"   ✗ NÃO CONFIGURADA!")
    print(f"   → Será usada a padrão: {GOOGLE_DEFAULT_CLIENT_ID}")

print("\n3. Verificação de Match:")
if allowed:
    allowed_ids = {item.strip() for item in allowed.split(",") if item.strip()}
    if GOOGLE_DEFAULT_CLIENT_ID in allowed_ids:
        print(f"   ✓ O Client ID padrão ESTÁ na lista de permitidos")
    else:
        print(f"   ✗ O Client ID padrão NÃO está na lista!")
        print(f"   → ERRO: Tokens serão rejeitados!")
else:
    print(f"   ✓ Usando Client ID padrão")

print("\n4. Logs de Debug Habilitados:")
try:
    import logging
    logger = logging.getLogger("routers.user")
    if logger.handlers or logger.level != logging.NOTSET:
        print(f"   ✓ Logging ativo para verificar tokens")
    else:
        print(f"   ⚠ Verificar se logging está configurado no backend")
except:
    print(f"   ⚠ Não foi possível verificar logging")

print("\n5. Verificação de Imports:")
try:
    import requests
    print(f"   ✓ requests disponível")
except:
    print(f"   ✗ requests NÃO INSTALADO - vai falhar!")

try:
    from fastapi import FastAPI
    print(f"   ✓ FastAPI disponível")
except:
    print(f"   ✗ FastAPI NÃO INSTALADO")

print("\n" + "="*70)
print("RESUMO:")
print("="*70)

if not allowed:
    print("⚠️  IMPORTANTE: Você PRECISA configurar a variável de ambiente")
    print("    GOOGLE_CLIENT_IDS no seu backend (Railway)")
    print("    Valor: 690521786732-6rh6blrhbu1ndqrpc2513mlv3mvrdacg.apps.googleusercontent.com")
else:
    print("✓ Configuração parece OK")

print("\n")
