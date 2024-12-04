from sqlmodel import SQLModel, create_engine, Session
from models import *

engine = create_engine('postgresql+psycopg://avnadmin:AVNS_MK_EMRIynysRfnfgk_w@pg-2652f3f7-tanmayjain4477-228c.e.aivencloud.com:24969/defaultdb?sslmode=require')

def start_db():
    print("Server is running with Postgres instance")
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        print("Session started")
        yield session