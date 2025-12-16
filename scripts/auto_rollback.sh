#!/usr/bin/env bash
set -e

APP_NAME="intelligent-deploy"
CONTAINER_NAME="intelligent-deploy-canary"
PORT=8000

IMAGE_LATEST="intelligent-deploy:latest"
IMAGE_STABLE="intelligent-deploy:stable"

echo "🟦 Starting Auto-Rollback workflow..."

docker rm -f $CONTAINER_NAME 2>/dev/null || true

echo "▶️ Running latest image..."
docker run -d --rm \
  -p ${PORT}:8000 \
  --name $CONTAINER_NAME \
  $IMAGE_LATEST

echo "⏳ Waiting for warm-up..."
sleep 45

RESPONSE=$(curl -sf http://localhost:${PORT}/health/intelligent || echo FAIL)
echo "Health Response: $RESPONSE"

if [ "$RESPONSE" = "FAIL" ]; then
  echo "❌ Health unreachable → rollback"
  docker stop $CONTAINER_NAME || true
  exit 1
fi

if echo "$RESPONSE" | grep -q '"degraded":false' && \
   echo "$RESPONSE" | grep -q '"decision_ready":true'; then
  echo "✅ Health OK → Promoting latest to stable"
  docker tag $IMAGE_LATEST $IMAGE_STABLE
  docker stop $CONTAINER_NAME
  exit 0
else
  echo "❌ Health degraded → rollback"
  docker stop $CONTAINER_NAME
  exit 1
fi