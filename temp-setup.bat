docker build --file /standalone-command/Dockerfile --tag standalone-command .
start powershell cd "standalone-command" ; docker-compose up -d ; cd ".."