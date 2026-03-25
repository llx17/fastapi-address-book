from fastapi import FastAPI

app = FastAPI(
    title="Address Book API",
    version="1.0.0",
    description="A minimal FastAPI address book application."
)


@app.get("/health")
def health_check():
    return {"status": "ok"}