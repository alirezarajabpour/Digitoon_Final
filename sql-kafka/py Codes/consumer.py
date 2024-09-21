import six
import sys

# Workaround for six.moves import error in Python 3.12
if sys.version_info >= (3, 12, 2):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaConsumer
import json
from sqlalchemy import create_engine, Column, Integer, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:29092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

DATABASE_URI = 'mysql+mysqlconnector://digitoon:digitoon123@localhost:13306/logs'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

class Transaction(Base):
    __tablename__ = 'transactions'
    transaction_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer)
    transaction_date = Column(Date)
    amount = Column(Numeric(10, 2))

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def insert_transaction(transaction):
    new_transaction = Transaction(
        transaction_id=transaction['transaction_id'],
        customer_id=transaction['customer_id'],
        transaction_date=transaction['transaction_date'],
        amount=transaction['amount']
    )
    session.add(new_transaction)
    session.commit()

try:
    for message in consumer:
        transaction = message.value
        insert_transaction(transaction)
        print(f'Transaction {transaction["transaction_id"]} inserted into MySQL.')
except KeyboardInterrupt:
    pass
finally:
    session.close()
