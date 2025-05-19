import random
from fastapi import FastAPI, Depends
from starlette.middleware.cors import CORSMiddleware
from database import engine, SessionLocal, Base
from model import Transact
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # або ["*"] для всіх (небажано в проді)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- Pydantic модель для створення ставки ---
class TransactCreate(BaseModel):
    bet: int
    trans_type: str  # краще, ніж просто "type"


# --- Ініціалізація бази даних ---
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --- Скидання кубиків ---
@app.get('/roll')
async def roll(db: Session = Depends(get_db)):
    b = -1
    dices = [random.randint(1, 6) for _ in range(6)]
    counts = [dices.count(i) for i in range(1, 7)]
    comb = {'pair': False, 'full house': False, 'yahtzee': False, 'three pairs': False, 'other': False}

    if 5 in counts:
        comb['yahtzee'] = True
    elif 4 in counts and 2 in counts:
        comb['full house'] = True
    elif counts.count(2) == 3 or 6 in counts or (4 in counts and 2 in counts):
        comb['three pairs'] = True
    elif max(counts) >= 2:
        comb['pair'] = True
    else:
        comb['other'] = True
    if list(comb.values()).index(True) >= 0:
        if comb['pair']:
            m = 1       #коефіцієнт для комбінації
        elif comb['full house']:
            m = 2
        elif comb['yahtzee']:
            m = 3
        elif comb['three pairs']:
            m = 4
        elif comb['other']:
            m=0
        b = db.query(Transact).filter(Transact.type == 'bet').order_by(Transact.id.desc()).first()
        win_tr = Transact(value=-b.value * m, type='win')
        db.add(win_tr)
        db.commit()
        db.refresh(win_tr)

    return {"dices": dices, 'comb': comb}


@app.get('/balance')
def balance(db: Session = Depends(get_db)):
    bal = 100
    tr = db.query(Transact).all()
    for i in tr:
        bal += i.value
    return bal

@app.get('/rtp')
def rtp (db: Session = Depends(get_db)):
    bets = db.query(Transact).filter(Transact.type=='bet')
    wins = db.query(Transact).filter(Transact.type=='win')
    all_bets = 0
    all_wins = 0
    for i in bets:
        all_bets +=i.value
    for i in wins:
        all_wins += i.value
    print('rtp: '+str((all_wins/(all_bets*-1))*100)+'%')
    return str(all_wins)+'/'+str(all_bets*-1)+'='+str((all_wins/(all_bets*-1))*100)

# --- Створення транзакції ставки ---
@app.get('/bet/{cost}')
async def betting(cost, db: Session = Depends(get_db)):
    tr = Transact(value=-int(cost), type='bet')
    db.add(tr)
    db.commit()
    db.refresh(tr)
    return tr


# --- Отримати всі транзакції ---
@app.get('/all')
async def all_bet(db: Session = Depends(get_db)):
    t = db.query(Transact).all()
    return t
