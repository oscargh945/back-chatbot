echo "Deploying server..."

git pull origin main

docker compose -f docker-compose.yml up --build -d

echo "Server deployed successfully!"