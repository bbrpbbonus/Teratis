# 🎮 Teratris - เกมจับคู่บล็อกที่ตกลงมา

โปรเจคนี้เป็นส่วนหนึ่งของการสอบ Exit Exam วิชา Computer Games Programming ปีการศึกษา 1/2567
สาขาวิชาวิทยาการคอมพิวเตอร์ คณะวิทยาศาสตร์ สถาบันเทคโนโลยีพระจอมเกล้าเจ้าคุณทหารลาดกระบัง

##  รายละเอียดเกม

เกม Teratris เป็นการผสมผสานระหว่างเกม Tetris แบบดั้งเดิมกับกลไกการจับคู่แบบ Match-3 โดยผู้เล่นจะต้องจัดการกับบล็อกที่ตกลงมาเพื่อสร้างคะแนนให้ได้ตามเป้าหมายภายในเวลาที่กำหนด

##  เป้าหมายของเกม

- สะสมคะแนนให้ได้ 1,000 คะแนนภายในเวลา 3 นาที
- จัดการบล็อกที่ตกลงมาให้เหมาะสม
- สร้าง Combo เพื่อเพิ่มคะแนน

##  คุณสมบัติหลัก

ตามข้อกำหนดของโจทย์:
- ✅ เกมทำงานบน PC Computer
- ✅ ขนาดกระดาน 10x20 ช่อง
- ✅ มีบล็อก 5 สี ได้แก่:
  - สีทอง (Gold)
  - สีม่วง (Purple)
  - สีฟ้า (Deep Sky Blue)
  - สีเขียว (Lime Green)
  - สีแดง (Tomato Red)
- ✅ บล็อกจะหายไปเมื่อเรียงเต็มแถว
- ✅ บล็อกด้านบนจะตกลงมาแทนที่เมื่อมีช่องว่าง
- ✅ มีระบบคะแนนและเวลาจำกัด (Time-Based)

##  วิธีการเล่น

### การควบคุม
- ⬅️ ปุ่มลูกศรซ้าย: เลื่อนบล็อกไปทางซ้าย
- ➡️ ปุ่มลูกศรขวา: เลื่อนบล็อกไปทางขวา
- ⬇️ ปุ่มลูกศรลง: เร่งความเร็วการตกของบล็อก
- ⬆️ ปุ่มลูกศรขึ้น: หมุนบล็อก
- Space: ทำให้บล็อกตกลงทันที
- P: หยุดเกมชั่วคราว
- R: เริ่มเกมใหม่ (เมื่อเกมจบแล้ว หรือเมื่อที่ต้องการ)

##  การติดตั้ง

### ความต้องการของระบบ
- Python 3.8 หรือสูงกว่า
- Pygame library

### ขั้นตอนการติดตั้ง
1. Clone repository:
```bash
git clone https://github.com/bbrpbbonus/Teratis.git
cd Teratris
```

2. ติดตั้ง dependencies:
```bash
pip install pygame
```

3. รันเกม:
```bash
python main.py
```

##  ระบบคะแนน

- การเคลียร์แถวจะได้คะแนนพื้นฐานดังนี้:
  - 1 แถว: 100 คะแนน
  - 2 แถว: 300 คะแนน
  - 3 แถว: 500 คะแนน
  - 4 แถว: 800 คะแนน
- คะแนนจะคูณด้วยจำนวน Combo ที่ทำได้
- เป้าหมายคือต้องทำคะแนนให้ได้ 1,000 คะแนนภายใน 3 นาที

##  เครดิต

พัฒนาโดย 65050492 นายบริพัตร จริยาทัศน์กร
อาจารย์ที่ปรึกษา: อ. วิชญะ ต่อวงศ์ไพชยนต์

##  การอ้างอิง

- การใช้ Pygame สำหรับการพัฒนาเกม: [Pygame Documentation](https://www.pygame.org/docs/)
- แรงบันดาลใจจากเกม Tetris และ Match-3 games

---
_โปรเจคนี้เป็นส่วนหนึ่งของการสอบ Exit Exam KMITL_
