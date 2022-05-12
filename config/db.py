from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:10287@localhost:3306/dbstore")

meta = MetaData()

conn = engine.connect()