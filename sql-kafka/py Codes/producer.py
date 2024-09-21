import six
import sys

# Workaround for six.moves import error in Python 3.12
if sys.version_info >= (3, 12, 2):
    sys.modules['kafka.vendor.six.moves'] = six.moves

from kafka import KafkaProducer
import json
import random
from datetime import datetime, timedelta
import numpy as np

producer = KafkaProducer(
    bootstrap_servers='localhost:29092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_fake_transaction(transaction_id):

    days_offset = int(np.random.normal(loc=180, scale=60))  # Normal distribution
    transaction_date = (datetime.now() - timedelta(days=days_offset)).strftime('%Y-%m-%d')
    
    customer_id = random.choices(
        population=[random.randint(75, 150) for _ in range(50)],
        weights=[random.expovariate(1) for _ in range(50)],
        k=1
    )[0]
    
    amount = int(np.random.lognormal(mean=4, sigma=1.5))
    
    transaction = {
        'transaction_id': transaction_id,
        'customer_id': customer_id,
        'transaction_date': transaction_date,
        'amount': amount
    }
    return transaction

for i in range(0, 15000):
    transaction = generate_fake_transaction(i)
    producer.send(topic='transactions', value=transaction)
    print(f'Transaction {transaction["transaction_id"]} sent to Kafka topic.')

producer.flush()
