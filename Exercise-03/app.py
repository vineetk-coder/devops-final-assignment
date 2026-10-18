# app.py — Flash Sale order service
import random
import socket
import time

from flask import Flask, request

app = Flask(__name__)


@app.get("/")
def homepage():
    # Welcome page; "pod" shows which replica answered
    return {
        "message": "Welcome to Big Sale!",
        "pod": socket.gethostname(),
        "ts": time.time()
    }


@app.get("/buy")
def buy():
    # simulate a flash sale checkout
    item = random.choice(["Smartphone", "Shoes", "Headphones", "Laptop"])
    user = request.args.get("user", f"user{random.randint(1,1000)}")
    return {
        "status": "success",
        "item": item,
        "user": user,
        "served_by_pod": socket.gethostname(),
        "time": time.strftime("%H:%M:%S")
    }


@app.get("/health")
def health():
    # used by readiness / liveness probes
    return {"status": "healthy", "pod": socket.gethostname()}
