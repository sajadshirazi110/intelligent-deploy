#!/usr/bin/env bash
set -e

APP_NAME=intelligent-app
PORT=8000
IMAGE_LATEST=intelligent-deploy:latest
IMAGE_STABLE=intelligent-deploy:stable

echo "🟦 Starting Auto-Rollback workflow..."

docker rm -f $APP_NAME 2>/dev/null || true

echo "▶️ Running latest image..."
docker run -d -p ${PORT}:8000 --name $APP_NAME $IMAGE_LATEST

echo "⏳ Waiting for warm-up..."
sleep 45

RESPONSE=$(curl -s http://localhost:${PORT}/health/intelligent || echo FAIL)
echo "Health Response: $RESPONSE"

if [ "$RESPONSE" = "FAIL" ]; then
  echo "❌ Health endpoint unreachable → rollback"
  docker rm -f $APP_NAME
  docker run -d -p ${PORT}:8000 --name $APP_NAME $IMAGE_STABLE
  exit 1
fi

DEGRADED=$(echo $RESPONSE | jq -r '.degraded')
READY=$(echo $RESPONSE | jq -r '.decision_ready')

if [ "$DEGRADED" != "false" ] || [ "$READY" != "true" ]; then
  echo "❌ Health is degraded → rollback to stable"
  docker rm -f $APP_NAME
  docker run -d -p ${PORT}:8000 --name $APP_NAME $IMAGE_STABLE
  exit 1
fi

echo "✅ Health OK → Promoting latest to stable"
docker tag $IMAGE_LATEST $IMAGE_STABLE
