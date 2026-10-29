# 🏛️ สถาปัตยกรรมระบบ Trading REA (Deep Architecture & Technical Spec)

เอกสารฉบับนี้อธิบายการแปลงโครงสร้างจาก [morluto/rea](https://github.com/morluto/rea) สู่ระบบการเทรดเชิงปริมาณอย่างละเอียด

---

## 1. การเปรียบเทียบสถาปัตยกรรมแบบตัวต่อตัว (1-to-1 Mapping)

| องค์ประกอบใน `morluto/rea` | บทบาทในการแกะซอฟต์แวร์ | องค์ประกอบใน `Trading REA` | บทบาทในการแกะตลาดการเงิน |
| :--- | :--- | :--- | :--- |
| **Phase 1: Decompile** | ถอดรหัส Binary/JS เป็น AST, Symbols, Functions | **Market Decompiler** (`market_decompiler.py`) | ถอดรหัสกราฟดิบ/Ticks เป็น Swing Points, FVG, Liquidity Pools |
| **Phase 2: Understand** | Trace เส้นทางการทำงาน และระบุ Evidence & Unknowns | **Empirical Trace Engine** (`empirical_trace_engine.py`) | Trace ระยะ Stop-Hunt, จำแนกลายนิ้วมือบอทสถาบัน, และคำนวณ Confidence |
| **Phase 3: Recreate** | สังเคราะห์โค้ดใหม่แบบ Clean-Room ให้ทำงานตรงตามเดิม | **Clean-Room Synthesizer** (`clean_room_synthesizer.py`) | สังเคราะห์คำสั่งเทรดสไนเปอร์ (50% FVG + 95th pctl SL) ส่งล่วงหน้า 0ms |
| **Evidence Bundle v2** | JSON สรุปหลักฐานเชิงประจักษ์ก่อนให้ AI ลงความเห็น | **Trading Evidence Bundle** (`evidence_bundle.py`) | ข้อมูลตัวเลขทางสถิติที่บังคับ AI ให้ตัดสินใจบนข้อเท็จจริง 100% |
| **MCP Server** | เปิดอินเทอร์เฟซมาตรฐานเชื่อมต่อกับ AI Coding Agents | **Trading MCP Server** (`mcp/server.py`) | รองรับ JSON-RPC 2.0 ให้ AI Agents เชื่อมต่อมาดึงหลักฐานและยิงออเดอร์ |
| **Native Providers** | Ghidra, Hopper, IDA, JADX, Node | **Financial Providers** | MetaTrader 5, Tick Volume Analyzers, Broker Microstructure |

---

## 2. โฟลว์ข้อมูลการประมวลผล (Data Flow Pipeline)

```
[MT5 Terminal / Tick Stream]
            │
            ▼
┌────────────────────────────────────────┐
│  Phase 1: Market Decompiler            │  <-- คำนวณ ATR, Swing Fractals,
│  (MarketAST)                           │      FVG 50% CE, Liquidity Pools
└────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────┐
│  Phase 2: Empirical Trace Engine       │  <-- วัด Stop-Hunt Pierce Depth,
│  (TradingEvidenceBundle v2)            │      วิเคราะห์ Effort vs Result,
│                                        │      ตรวจ Session DNA & Unknowns
└────────────────────────────────────────┘
            │
            ▼
┌────────────────────────────────────────┐
│  Phase 3: Clean-Room Synthesizer       │  <-- วาง Limit ที่ 50% FVG,
│  (CleanRoomOrder)                      │      ตั้ง SL นอกระยะแทงหลอก 95th pctl,
│                                        │      ชดเชย Spread สองฝั่ง Bid/Ask,
│                                        │      คุมเงิน $100 หรือ 10,000 Cents
└────────────────────────────────────────┘
            │
            ▼
[Pending Limit Order @ Broker Server (0 ms Execution)]
```

---

## 3. กฎความปลอดภัยทางสถิติ (Statistical Safeguards)

1. **ห้ามเดา (Zero Hallucination)**: หากไม่มีหลักฐานการกวาดสภาพคล่อง หรือค่าความเชื่อมั่นต่ำกว่า 65% ระบบจะปรับเป็น `WAIT_FOR_MORE_EVIDENCE` หรือ `REJECT_RISK_EXCEEDED` ทันที
2. **Rollover Death-Zone Filter**: ช่วงเวลา 04:00 - 05:15 น. (เวลาไทย) สเปรดโบรกเกอร์จะถ่างออก 5-10 เท่า ระบบจะบล็อกการเปิดคำสั่งใหม่ทุกกรณี
3. **Asymmetric Bid/Ask Compensation**: กราฟ MT5 พล็อตเฉพาะราคา Bid ระบบจะยกจุดเข้า `BUY_LIMIT` ขึ้นเท่ากับ `Spread + Ping Buffer` เพื่อให้ออเดอร์จับคู่ทันทีเมื่อ Bid แตะเส้น และถอย SL ฝั่ง `SELL` หนีสเปรดถ่าง
