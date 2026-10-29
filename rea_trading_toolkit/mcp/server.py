# -*- coding: utf-8 -*-
"""
Trading REA Model Context Protocol (MCP) Server
Implements standard JSON-RPC 2.0 stdio protocol matching morluto/rea specifications.
Enables any AI Coding Agent (Antigravity, Claude Code, Cursor, Gemini CLI) to connect
and interact directly with local Trading REA engines.
"""

import sys
import json
import logging
from typing import Dict, Any

from .tools import get_tool_definitions, handle_tool_call

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", stream=sys.stderr)
logger = logging.getLogger("TradingREA_MCP")


class TradingREAMCPServer:
    def __init__(self):
        self.running = True

    def run(self):
        logger.info("Trading REA MCP Server started (listening on stdio)...")
        while self.running:
            try:
                line = sys.stdin.readline()
                if not line:
                    break
                
                line = line.strip()
                if not line:
                    continue

                request = json.loads(line)
                response = self._process_request(request)
                if response is not None:
                    sys.stdout.write(json.dumps(response) + "\n")
                    sys.stdout.flush()

            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error: {e}")
            except Exception as e:
                logger.error(f"Server loop error: {e}")

    def _process_request(self, req: Dict[str, Any]) -> Dict[str, Any]:
        req_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})

        if method == "initialize":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "protocolVersion": "2024-11-05",
                    "capabilities": {
                        "tools": {"listChanged": False}
                    },
                    "serverInfo": {
                        "name": "trading-rea-mcp-server",
                        "version": "1.0.0"
                    }
                }
            }

        elif method == "notifications/initialized":
            logger.info("Client initialized notification received.")
            return None

        elif method == "ping":
            return {"jsonrpc": "2.0", "id": req_id, "result": {}}

        elif method == "tools/list":
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "tools": get_tool_definitions()
                }
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            try:
                result_data = handle_tool_call(tool_name, tool_args)
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(result_data, indent=2, ensure_ascii=False)
                            }
                        ]
                    }
                }
            except Exception as e:
                logger.error(f"Tool execution failed for '{tool_name}': {e}")
                return {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32000,
                        "message": str(e)
                    }
                }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {
                    "code": -32601,
                    "message": f"Method not found: {method}"
                }
            }


if __name__ == "__main__":
    server = TradingREAMCPServer()
    server.run()
