# -*- coding: utf-8 -*-
"""
Local Tactical Cockpit HTTP Server + Background Zero-Token Guardian
Connects tactical_cockpit.html directly to WarRoomCommander & MT5ExecutionBridge (0 Tokens).
"""

import json
import os
import threading
import time
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

from war_room_commander import WarRoomCommander
from mt5_execution_bridge import MT5ExecutionBridge

COMMANDER = WarRoomCommander("XAUUSD", "M15")
BRIDGE = MT5ExecutionBridge("XAUUSD")


def background_guardian_loop():
    while True:
        try:
            BRIDGE.run_zero_token_local_guardian()
        except Exception:
            pass
        time.sleep(1.5)


class CockpitHandler(SimpleHTTPRequestHandler):
    def _send_json(self, payload: dict, status: int = 200):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/status":
            cycle = COMMANDER.execute_war_room_cycle(force_wake_ai=True)
            guard = BRIDGE.run_zero_token_local_guardian()
            self._send_json({
                "war_room": cycle,
                "guardian": guard,
                "telemetry": BRIDGE.get_telemetry()
            })
            return
        elif parsed.path in ("/", "/index.html"):
            self.path = "/tactical_cockpit.html"
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/auto_sniper":
            res = COMMANDER.execute_war_room_cycle(execute_live_mt5=True, force_wake_ai=True)
            self._send_json(res)
        elif parsed.path == "/api/breakeven":
            res = BRIDGE.run_zero_token_local_guardian()
            self._send_json(res)
        elif parsed.path == "/api/cancel_all":
            res = BRIDGE.cancel_all_pending()
            self._send_json(res)
        elif parsed.path == "/api/panic_close":
            res = BRIDGE.panic_close_all()
            self._send_json(res)
        else:
            self._send_json({"error": "Unknown endpoint"}, 404)


def run_server(port: int = 8765):
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    t = threading.Thread(target=background_guardian_loop, daemon=True)
    t.start()
    server = HTTPServer(("127.0.0.1", port), CockpitHandler)
    print(f"Tactical Cockpit Server running at http://127.0.0.1:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
