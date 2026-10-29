# 🤖 Our REA Trading Bot (`our_rea_trading_bot/`)

> **ระบบเทรดสดอัจฉริยะประจำพอร์ตของเราโดยเฉพาะ (Autonomous War-Room Live Trading Bot)**  
> เชื่อมต่อสมองจาก [`rea_trading_toolkit/`](file:///d:/โปรเจค%20ai/บอทเทรด/rea_trading_toolkit) เข้ากับพอร์ต MetaTrader 5 จริง, ระบบสลับโมเดล AI 4 ระดับ, และผู้พิทักษ์ความเร็ว 0ms

---

## โครงสร้างไฟล์ (Ultra-Lean Architecture)

| ไฟล์ | บทบาทหน้าที่ |
| :--- | :--- |
| [`bot_cli.py`](file:///d:/โปรเจค%20ai/บอทเทรด/our_rea_trading_bot/bot_cli.py) | CLI หลักสำหรับสั่งการบอทของเรา (`war-room`, `model-audit`, `execute-sniper`, `guard`, `cancel-all`, `panic-close`) |
| [`war_room_commander.py`](file:///d:/โปรเจค%20ai/บอทเทรด/our_rea_trading_bot/war_room_commander.py) | ห้องบัญชาการสงคราม 2026–2036 เชื่อม Decompiler + Red Team + Monte Carlo 1,000 รอบ + Truth Gatekeeper เข้ากับ MT5 |
| [`model_intelligence_router.py`](file:///d:/โปรเจค%20ai/บอทเทรด/our_rea_trading_bot/model_intelligence_router.py) | ตัวคัดเลือกและสลับโมเดล AI 4 ระดับ (Tier 0 ถึง Tier 3) พร้อมตัววัดโทเคนจริงระดับตัวอักษรและคำนวณโควต้าแพ็กเกจ |
| [`mt5_execution_bridge.py`](file:///d:/โปรเจค%20ai/บอทเทรด/our_rea_trading_bot/mt5_execution_bridge.py) | สะพานเชื่อม MT5 จริง, ยิง Pending Order 0ms พร้อม Hard SL/TP, Auto Break-Even (+0.85R), Trailing (+1.5R), และตัดขาดทุนรายวัน 3% |
| [`cockpit_server.py`](file:///d:/โปรเจค%20ai/บอทเทรด/our_rea_trading_bot/cockpit_server.py) & [`tactical_cockpit.html`](file:///d:/โปรเจค%20ai/บอทเทรด/our_rea_trading_bot/tactical_cockpit.html) | หน้าจอควบคุม HUD สดแบบ 1-Click บนเบราว์เซอร์ (`http://127.0.0.1:8765` ใช้ 0 โทเคน) |
