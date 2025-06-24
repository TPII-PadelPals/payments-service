#!/bin/bash

# Mata procesos previos de ngrok (opcional)
killall ngrok > /dev/null 2>&1

# Inicia ngrok en segundo plano (ajusta el puerto según tu servicio)
nohup ngrok http http://localhost:8005 > /dev/null 2>&1 &

# Espera a que ngrok levante
sleep 4

# Obtiene la URL HTTPS desde el API local de ngrok
NGROK_URL=$(curl -s http://127.0.0.1:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [ -z "$NGROK_URL" ]; then
  echo "No se pudo obtener la URL de ngrok"
  killall ngrok > /dev/null 2>&1
  exit 1
fi

echo "Url de Ngrok obtenida correctamente: $NGROK_URL"
