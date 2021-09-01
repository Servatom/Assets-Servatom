import uvicorn
if __name__ == "__main__":
    uvicorn.run("api.main:app", 
                host="0.0.0.0", 
                port=3000,
                reload=True,
                ssl_keyfile="./key.pem",
                ssl_certfile="./cert.pem"
                )