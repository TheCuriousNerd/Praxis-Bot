import asyncio

import time

from windyquery import DB

db:DB = DB()


def init():
    print("Letting DB setup")
    time.sleep(5)
    print("Initiating Connection")
    asyncio.new_event_loop().run_until_complete(db.connect('PRAXIS_BOT_DB', {
    'host' : 'standalone_db_main',
    'port' : '5432',
    'database' : 'PRAXIS_BOT_DB',
    'username' : 'PRAXIS_BOT',
    'password' : 'PraxisPraxisPraxis',
}, default=True))


def maintest(db:DB):
    # SELECT id, name FROM users
    db.schema('TABLE users').create(
    'id            serial PRIMARY KEY',
    'group_id      integer references groups (id) ON DELETE CASCADE',
    'created_at    timestamp not null DEFAULT NOW()',
    'email         text not null unique',
    'name         text not null',
    'is_admin      boolean not null default false',
    'address       jsonb',
    'payday        integer not null',
    'CONSTRAINT unique_email UNIQUE(group_id, email)',
    'check(payday > 0 and payday < 8)'
    )

    # CREATE TABLE accounts LIKE users
    db.schema('TABLE accounts').create(
        'like users'
    )

    # CREATE TABLE IF NOT EXISTS accounts LIKE users
    db.schema('TABLE IF NOT EXISTS accounts').create(
        'like users'
    )

    db.table('users').insert(
    {'id': 1, 'name': 'Tom'},
    {'id': 2, 'name': 'Jerry'},
    {'id': 3, 'name': 'DEFAULT'}
    )

    users = db.table('users').select('id', 'name')
    print(type(users))

if __name__ == "__main__":
    init()
    maintest(db)
