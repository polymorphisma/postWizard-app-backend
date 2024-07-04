import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        app="server:app",
        loop="asyncio",
        host="0.0.0.0",
        port=8000,
        reload=True,
        env_file="../.env",
    )
