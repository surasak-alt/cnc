# 🛡️ Autonomous AI REA Trading System (`cnc` Backup Repository)

สถาปัตยกรรมระบบเทรดควอนตัมอัตโนมัติ (2026–2036 Ideal Architecture) ที่ดัดแปลงจากแนวคิด **Reverse Engineer Anything (`morluto/rea`)** แบบ **Two-Folder Lean Architecture** ปราศจาก Bias, มีระบบสลับโมเดลอัตโนมัติ (4-Level Sovereign Failover Cascade) และใช้ทุนมาตรฐาน **$100 (Standard) / 10,000 Cents (Cent)**

---

## 📂 โครงสร้างโปรเจกต์ (Two-Folder Lean Architecture)

```text
.
├── our_rea_trading_bot/          # [โฟลเดอร์ที่ 1] ระบบ REA สำหรับบอทเทรดของเราโดยเฉพาะ (Live Bot + War-Room + Auto-Failover)
│   ├── model_intelligence_router.py  # ระบบคัดกรองโมเดล 4-Tier + Auto-Failover (Gemini 4 Argon -> 3.8 Pro -> 3.8 Flash -> Local NumPy)
│   ├── war_room_commander.py         # ศูนย์บัญชาการ 6 ด่าน (Decompile -> Empirical -> MC 1000 -> Red Team -> Truth FSM -> Execution)
│   ├── mt5_execution_bridge.py       # สะพานเชื่อม MetaTrader 5 ยิง Pending Order (0ms Slippage) + คุมความเสี่ยง $100 / 10,000 Cents
│   ├── bot_cli.py                    # CLI หลักสำหรับเทรด, สั่งจำลอง Failover, และวัดการใช้โทเคนจริง
│   ├── cockpit_server.py             # Live Web Server (Port 8095)
│   ├── tactical_cockpit.html         # หน้าจอเรดาร์ควบคุมแบบ Glassmorphism
│   └── data/                         # เก็บสมอง Bayesian Memory, Token Quota Ledger และ Evidence Bundles
│
├── rea_trading_toolkit/          # [โฟลเดอร์ที่ 2] ชุดเครื่องมือ REA กลางสำหรับการเทรดทั่วไป & MCP Server
│   ├── contracts/                    # โครงสร้างข้อมูล Pydantic v2 (MarketAST, EvidenceBundleV2, ExecutionOrderContract)
│   ├── providers/                    # แกนคำนวณคณิตศาสตร์ 8 ตัว (500-Bar Z-Test, 1000-Path NumPy MC, Red Team, Truth Gatekeeper ฯลฯ)
│   ├── mcp/                          # MCP Server (Model Context Protocol) 5 Tools สำหรับเชื่อมต่อ AI Agent
│   ├── tests/                        # Unit Tests ตรวจสอบความถูกต้องและระบบ Auto-Failover (7/7 Passing)
│   └── rea_cli.py                    # CLI อเนกประสงค์สำหรับสแกนคู่เงิน/แกะรอย EA/สแกนโบรกเกอร์
│
├── AI_MEMORY_REA_TRADING.md      # ความทรงจำถาวรของระบบ AI REA Trading
└── MASTER_AI_TRADING_BLUEPRINT.md # พิมพ์เขียวสถาปัตยกรรมฉบับสมบูรณ์
```

---

## 🚀 คำสั่งเริ่มต้นใช้งานด่วน (Quick Start)

### 1. รันชุดทดสอบความสมบูรณ์ของระบบทั้ง 7 ด่าน (Unit Tests)
```powershell
python rea_trading_toolkit/tests/test_rea_pipeline.py
```

### 2. ตรวจสอบการสลับโมเดลอัตโนมัติ (Model Auto-Failover) และวัดโทเคนจริง
```powershell
python our_rea_trading_bot/bot_cli.py model-audit --symbol XAUUSD --tf M15
```

### 3. สั่งรัน War-Room เต็มรูปแบบ (Dry-Run ปลอดภัย หรือ `--live` เมื่อพร้อมยิงเข้า MT5)
```powershell
python our_rea_trading_bot/bot_cli.py war-room --symbol XAUUSD --tf M15 --account-type STANDARD
```

### 4. เปิดหน้าจอเรดาร์ Tactical Cockpit (Port 8095)
```powershell
python our_rea_trading_bot/bot_cli.py cockpit --port 8095
```
*(จากนั้นเปิดเบราว์เซอร์ไปที่ `http://127.0.0.1:8095`)*
