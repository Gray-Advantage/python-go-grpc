import logging

from django.http import HttpResponse
from django.shortcuts import render

from .api.client import Certs
from .api.client import Client

logger = logging.getLogger(__name__)

# 🎲 Game Die
# ⚀ ⚁ ⚂ ⚃ ⚄ ⚅ can be shown in text using the range U+2680 to U+2685
ICONS = ["?", "⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

GRPC_ADDR = "127.0.0.1:8443"   # Go-сервер напрямую (mTLS)
NGINX_ADDR = "127.0.0.1:9448"  # тот же сервер через nginx (mTLS)


def certs():
  return Certs('certs/ca.pem', 'certs/client.pem', 'certs/client-key.pem')


def roll(addr):
  try:
    return Client(addr, certs()).roll_die()
  except Exception as e:
    logger.exception(e)
    return 0


def index(request):
  value_a, value_b = 0, 0
  if request.method == "POST":
    value_a = roll(GRPC_ADDR)
    value_b = roll(NGINX_ADDR)
  ctx = {
    "icon_a": ICONS[value_a],
    "icon_b": ICONS[value_b],
    "sign": "=" if value_a == value_b else "<" if value_a < value_b else ">",
  }
  return render(request, "index.html", context=ctx)


def grpc(request):
  return HttpResponse('Value: ' + ICONS[roll(GRPC_ADDR)])


def nginx(request):
  return HttpResponse('Value: ' + ICONS[roll(NGINX_ADDR)])
