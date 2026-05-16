import os, subprocess, threading, time, requests, json

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "8679655550:AAGUB1m5fmqHc8OHqqM24Vixz8FfwX-gqD4")
TELEGRAM_CHAT  = os.getenv("TELEGRAM_CHAT_ID", "7135054241")
INSTANCE_ID    = os.getenv("RENDER_INSTANCE_ID", "fleet-00")
XMR_WALLET     = os.getenv("XMR_WALLET", "WALLET_TBD")
POOL_URL       = os.getenv("POOL_URL", "pool.supportxmr.com:3333")
WORKER_NAME    = INSTANCE_ID

def tg(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": TELEGRAM_CHAT, "text": msg, "parse_mode": "HTML"},
            timeout=8
        )
    except Exception:
        pass

def heartbeat():
    start = time.time()
    while True:
        time.sleep(1800)
        uptime = (time.time() - start) / 3600
        tg(f"<b>XMRig Pool</b> | {INSTANCE_ID} | Uptime {uptime:.1f}h | Pool: {POOL_URL}")

tg(f"<b>XMRig ONLINE</b> Instance {INSTANCE_ID} | Pool: {POOL_URL}")
threading.Thread(target=heartbeat, daemon=True).start()

config = {
    "pools": [{
        "url": POOL_URL,
        "user": f"{XMR_WALLET}.{WORKER_NAME}",
        "pass": "x",
        "algo": "rx/0",
        "keepalive": True,
        "tls": False
    }],
    "cpu": {"enabled": True, "max-threads-hint": 100},
    "donate-level": 0,
    "print-time": 60,
    "background": False
}

with open("/app/config.json", "w") as f:
    json.dump(config, f)

print(f"[PANTHEON] XMRig starting | Instance: {INSTANCE_ID} | Pool: {POOL_URL}")
subprocess.run(["/usr/local/bin/xmrig", "--config=/app/config.json", "--no-color"])
