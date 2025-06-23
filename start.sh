GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[1;33m"
NC="\033[0m" 

echo -e "${YELLOW}Starting Docker containers...${NC}"
if docker compose up -d; then
    echo -e "${GREEN}Docker containers started successfully.${NC}"
else
    echo -e "${RED}Failed to start Docker containers.${NC}"
    exit 1
fi

echo -e "${YELLOW}Changing directory to 'ui'...${NC}"
if cd ui; then
    echo -e "${GREEN}Inside 'ui' directory.${NC}"
else
    echo -e "${RED}Directory 'ui' not found. Aborting.${NC}"
    exit 1
fi

echo -e "${YELLOW}Starting frontend development server with yarn dev...${NC}"
if yarn dev; then
    echo -e "${GREEN}Frontend server stopped.${NC}"
else
    echo -e "${RED}Failed to start frontend server.${NC}"
    exit 1
fi
