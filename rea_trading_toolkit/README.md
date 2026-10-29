# 🛡️ Trading REA: Reverse Engineer Anything for Quantitative Trading

> **ระบบเทรดอัจฉริยะเชิงวิศวกรรมย้อนรอย (Trading Reverse-Engineering Engine)**  
> ได้รับการออกแบบและพัฒนาขึ้นโดยนำแนวคิด โครงสร้าง และสถาปัตยกรรมระดับโลกจาก [morluto/rea](https://github.com/morluto/rea) มาปรับใช้กับการเทรดเชิงปริมาณ (Quantitative Trading & Market Microstructure) โดยเฉพาะ

---

## 1. ปรัชญาหลัก (Core Philosophy)

ในโปรเจกต์ `morluto/rea` หัวใจสำคัญคือ **"การเปลี่ยน AI จากผู้คาดเดา (Hallucinating Guesser) ให้กลายเป็นนักสืบเชิงประจักษ์ (Empirical Investigator)"** โดยใช้กระบวนการ 3 ขั้นตอน: **Decompile -> Understand -> Recreate** พร้อมระบบ **Evidence-Centric Design** ที่ทุกข้อสรุปต้องมีหลักฐานตัวเลขยืนยัน

ใน **Trading REA** เรามองตลาดการเงินและพฤติกรรมราคาเสมือน **"ซอฟต์แวร์ระบบปิด (Compiled Binary Black-Box)"** ที่ถูกควบคุมโดยอัลกอริทึมของธนาคารและสถาบันการเงิน:

```
+-----------------------------------------------------------------------------------+
|                            TRADING REA 3-PHASE PIPELINE                            |
+-----------------------------------------------------------------------------------+
|  [PHASE 1: DECOMPILE]  -->  [PHASE 2: UNDERSTAND]    -->  [PHASE 3: RECREATE]     |
|  Market-AST Parser          Empirical Evidence v2         Clean-Room Synthesizer  |
|  - Swing Pivots (High/Low)  - Stop-Hunt Pierce Depth      - 50% FVG Equilibrium   |
|  - Active FVG Gaps          - Effort vs Result Ratio      - 95th Pctl Safe SL     |
|  - Liquidity Pools (BSL/SSL)- Chronos Thai Session DNA    - Asymmetric Spread Adj |
|  - Volume Delta Profile     - Known Limitations & Score   - Zero-Ping Limit Order |
+-----------------------------------------------------------------------------------+
```

---

## 2. โครงสร้างระบบ (Directory Architecture)

โครงสร้างโฟลเดอร์ถูกออกแบบเลียนแบบ `morluto/rea` อย่างเคร่งครัด แยกเป็นสัดส่วนชัดเจน:

```text
rea_trading_system/
├── README.md                      # เอกสารภาพรวมและการใช้งาน
├── rea_cli.py                     # CLI Tool หลัก (เหมือน rea-agents ใน morluto/rea)
├── contracts/                     # Data Contracts & Pydantic Schemas
│   ├── market_ast.py              # Phase 1: สัญญาโครงสร้างตลาด Decompiled AST
│   ├── evidence_bundle.py         # Phase 2: สัญญาชุดหลักฐาน Evidence Bundle v2
│   └── execution_order.py         # Phase 3: สัญญาคำสั่งเทรด Clean-Room Order
├── providers/                     # เครื่องมือตรวจสอบเฉพาะทาง (Inspection Engines)
│   ├── market_decompiler.py       # Phase 1: ตัวแยกส่วนกราฟและ Tick Data
│   ├── empirical_trace_engine.py  # Phase 2: ตัวสืบลายนิ้วมือบอทสถาบันและหลักฐาน
│   ├── broker_blindspot_engine.py # ตัววิเคราะห์จุดบอดและกฎลับของโบรกเกอร์
│   ├── clean_room_synthesizer.py  # Phase 3: ตัวสังเคราะห์คำสั่งแก้ทางเจ้ามือ
│   └── ea_strategy_decompiler.py  # เครื่องมือถอดรหัสบอท EA/PineScript ภายนอก
├── mcp/                           # Model Context Protocol (MCP) Server
│   ├── server.py                  # JSON-RPC 2.0 Stdio Server
│   └── tools.py                   # ทะเบียน MCP Tools สำหรับ AI Agents
├── evidence_vault/                # คลังจัดเก็บ Snapshot หลักฐาน Evidence JSON แต่ละรอบ
└── tests/                         # ชุดการทดสอบระบบแบบอัตโนมัติ
    └── test_rea_pipeline.py       # Unit tests ผ่าน 100%
```

---

## 3. กระบวนการ 3 ขั้นตอน (The 3 Phases in Detail)

### Phase 1: Decompile (แยกส่วนโครงสร้างตลาด)
* **โมดูล:** `providers/market_decompiler.py`
* **หน้าที่:** รับข้อมูลแท่งเทียนและ Tick Volume (จาก MT5 หรือ Fallback Simulator) แล้วแยกชิ้นส่วนออกมาเป็น `MarketAST`:
  - **Swing Points:** จุดสูงสุด/ต่ำสุดสำคัญที่ยังไม่ถูกกวาดสภาพคล่อง
  - **Fair Value Gaps (FVG):** ช่องว่างราคาที่เกิดจากการผลักดันของสถาบัน พร้อมคำนวณจุดดุลยภาพ 50% (Consequent Encroachment)
  - **Liquidity Pools:** กลุ่ม Stop-loss ของรายย่อย (Buy-Side และ Sell-Side Liquidity)
  - **Volume Delta:** อัตราส่วน Effort vs Result (แรงผลักดันเทียบกับปริมาณวอลุ่ม)

### Phase 2: Understand & Evidence Generation (พิสูจน์ด้วยหลักฐาน ห้ามเดา)
* **โมดูล:** `providers/empirical_trace_engine.py`
* **หน้าที่:** สร้าง `TradingEvidenceBundle` (มาตรฐาน Evidence v2) โดยทุกข้อสรุปต้องมีตัวเลขเชิงสถิติ:
  - **Stop-Hunt Pierce Depth:** วัดระยะแทงทะลุแนวรับ/แนวต้านเป็นเท่าของ ATR(14)
  - **Algo Fingerprinting:** จำแนกลายนิ้วมืออัลกอริทึม เช่น `JUDAS_SWING_STOP_RAID`, `ICEBERG_ABSORPTION_WALL`, `LIQUIDITY_VACUUM_MANIPULATION`, หรือ `TWAP_VWAP_TREND_EXECUTION`
  - **Chronos Session DNA:** วิเคราะห์กรอบเวลาตลาดตามเวลาไทย (06:00-13:00 เอเชีย, 13:00-16:00 ลอนดอนสับขาหลอก, 19:00-23:00 ตลาดมหาอำนาจ, 04:00-05:15 เขตอันตราย Rollover สเปรดถ่าง)
  - **Known Limitations & Unknowns:** ระบุปัจจัยเสี่ยงอย่างตรงไปตรงมา เช่น ข่าวเศรษฐกิจสำคัญ หรือช่วงเปลี่ยนวัน
  - **Statistical Confidence Score:** คำนวณค่าความเชื่อมั่นทางสถิติ (0.00 - 1.00) ก่อนอนุญาตให้ยิงออเดอร์

### Phase 3: Recreate / Clean-Room Synthesizer (สังเคราะห์คำสั่งแก้ทาง)
* **โมดูล:** `providers/clean_room_synthesizer.py`
* **หน้าที่:** นำผลจาก Phase 2 มาสร้างคำสั่ง `CleanRoomOrder` ที่สมบูรณ์แบบ:
  - **Entry:** วาง Pending Limit Order ดักไว้ที่จุดดุลยภาพ 50% FVG เพื่อความแม่นยำระดับสไนเปอร์
  - **Hard SL:** วางไว้นอกระยะแทงหลอกที่ระดับ 95th Percentile ($0.78 \times \text{ATR}$) พร้อมถอยหนีสเปรดถ่าง
  - **0ms Server Execution:** คำสั่งเป็น Pending Order มี Hard SL และ TP ฝังไปด้วยเสมอ รันบนเซิร์ฟเวอร์โบรกเกอร์ ไม่สะเทือนแม้เน็ตมือถือหลุด
  - **Strict Capital Standard:**
    - พอร์ต **Standard**: คำนวณความเสี่ยงบนฐานทุน **$100** (เสี่ยง 1% = $1.00)
    - พอร์ต **Cent**: คำนวณความเสี่ยงบนฐานทุน **10,000 Cents** (เสี่ยง 1% = 100 Cents)

---

## 4. โมดูลพิเศษที่ดึงมาจาก `morluto/rea`

### 4.1 EA & Strategy Decompiler (`providers/ea_strategy_decompiler.py`)
ความสามารถในการแกะรหัสซอฟต์แวร์เทรดภายนอก เช่น ไฟล์ EA (`.mq4`, `.mq5`), TradingView Pine Script (`.pine`), หรือโค้ด Python:
- ตรวจจับตรรกะอันตราย **Martingale** (การเบิ้ล Lot เมื่อแพ้)
- ตรวจจับ **Grid Averaging** (การเปิดไม้อมขาดทุนแก้ทาง)
- ตรวจจับ **Naked Orders** (การเปิดออเดอร์แบบไม่มี Stop Loss)
- ถอดรหัสสูตร Indicator และระดับพารามิเตอร์ลับออกมาวิเคราะห์

### 4.2 Broker Blindspot Neutralizer (`providers/broker_blindspot_engine.py`)
วิเคราะห์และแก้ทางกลไกของโบรกเกอร์:
- ชดเชยจุดบอดกราฟ MT5 ที่วาดเฉพาะราคา Bid (ยกจุดเข้า Buy Limit ขึ้น และถอย SL ฝั่ง Sell)
- ตรวจจับระยะห่างขั้นต่ำ `TRADE_STOPS_LEVEL` และ `TRADE_FREEZE_LEVEL` เพื่อป้องกัน `Error 10016`

---

## 5. การใช้งานผ่าน CLI (Command Line Interface)

สามารถสั่งการผ่าน Terminal ได้ทันที:

```bash
# 1. ทดสอบรันครบ 3 ขั้นตอน (Pipeline)
python rea_trading_system/rea_cli.py pipeline --symbol XAUUSD --tf M15

# 2. Phase 1: ส่อง Decompile โครงสร้างตลาด
python rea_trading_system/rea_cli.py decompile --symbol XAUUSD --tf M15

# 3. Phase 2: สืบลายนิ้วมือและออก Evidence Bundle
python rea_trading_system/rea_cli.py trace --symbol XAUUSD --tf M15

# 4. Phase 3: สังเคราะห์คำสั่งเทรด Clean-Room (พอร์ต Standard หรือ Cent)
python rea_trading_system/rea_cli.py synthesize --symbol XAUUSD --account CENT --risk 1.0

# 5. ตรวจสอบจุดบอดและค่าสเปรดของโบรกเกอร์
python rea_trading_system/rea_cli.py audit-broker --symbol XAUUSD

# 6. ถอดรหัสและวิเคราะห์ความเสี่ยงของบอท EA หรือ Pine Script ภายนอก
python rea_trading_system/rea_cli.py decompile-strategy --file path/to/strategy.mq4

# 7. เริ่มต้นรัน Trading REA MCP Server (JSON-RPC 2.0 stdio)
python rea_trading_system/rea_cli.py mcp-serve
```

---

## 6. การเชื่อมต่อกับ AI Agents ผ่าน MCP (Model Context Protocol)

ตัวระบบมี MCP Server ในตัว (`mcp/server.py`) ทำให้ AI Coding Assistant (เช่น Claude Code, Antigravity, Cursor, หรือ Gemini CLI) สามารถเรียกใช้เครื่องมือได้ทันทีผ่าน `stdio`:

เครื่องมือที่พร้อมให้ AI เรียกใช้:
1. `rea_decompile_market`: ดึง Market-AST 
2. `rea_build_evidence_bundle`: วิเคราะห์หลักฐานและออก Evidence Bundle
3. `rea_synthesize_clean_order`: สร้างคำสั่งเทรดสไนเปอร์
4. `rea_audit_broker_blindspot`: ตรวจสเปรดและระดับ Stop Level
5. `rea_inspect_external_strategy`: ตรวจสอบโค้ดบอทภายนอก

---

## 7. ผลการทดสอบความถูกต้อง (Test Results)

ระบบมี Unit Test ครอบคลุมการทำงานทุกส่วนใน [tests/test_rea_pipeline.py](file:///d:/โปรเจค%20ai/บอทเทรด/rea_trading_system/tests/test_rea_pipeline.py):

```text
Ran 7 tests in 4.498s
OK (All tests passed successfully)
```
- Phase 1 Market-AST Verification: PASS
- Phase 2 Evidence Bundle & Confidence Verification: PASS
- Phase 3 Clean-Room Synthesis (Standard $100 & Cent 10,000): PASS
- Broker Blindspot Neutralizer: PASS
- Toxic EA/Martingale Decompiler: PASS
- MCP Dispatcher & Contracts: PASS
