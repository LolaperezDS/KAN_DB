from models import RoomTable
from database import SessionLocal, engine




session = SessionLocal(bind=engine)

for floor in range(1, 10):
    for block in range(1, 17):
        for size in "SL":
            bl = str(block)
            if block < 10:
                bl = "0" + str(block)
            session.add(RoomTable(number=f"{floor}{bl}{size}"))
session.commit()
session.close()
