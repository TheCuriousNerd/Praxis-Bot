docker build --file /standalone_command/Dockerfile --tag standalone_command .
start powershell cd "standalone_command" ; docker-compose up -d ; cd ".."