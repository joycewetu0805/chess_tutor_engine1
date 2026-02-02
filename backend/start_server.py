#!/usr/bin/env python3
import uvicorn

if __name__ == "__main__":
    print("Starting Chess Tutor Engine Backend...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
