import asyncio

from windyquery import DB

db:DB = DB()
asyncio.new_event_loop().run_until_complete(db.connect('PRAXIS_BOT_DB', {
    'host' : 'standalone_db',
    'port' : '5432',
    'database' : 'PRAXIS_BOT_DB',
    'username' : 'PRAXIS_BOT',
    'password' : 'PraxisPraxisPraxis',
}, default=True))

def init():
    print("test")


async def maintest(db:DB):
    # SELECT id, name FROM users
    await db.schema('TABLE users').create(
    'id            serial PRIMARY KEY',
    'group_id      integer references groups (id) ON DELETE CASCADE',
    'created_at    timestamp not null DEFAULT NOW()',
    'email         text not null unique',
    'is_admin      boolean not null default false',
    'address       jsonb',
    'payday        integer not null',
    'CONSTRAINT unique_email UNIQUE(group_id, email)',
    'check(payday > 0 and payday < 8)'
    )

    # CREATE TABLE accounts LIKE users
    await db.schema('TABLE accounts').create(
        'like users'
    )

    # CREATE TABLE IF NOT EXISTS accounts LIKE users
    await db.schema('TABLE IF NOT EXISTS accounts').create(
        'like users'
    )

    await db.table('users').insert(
    {'id': 1, 'name': 'Tom'},
    {'id': 2, 'name': 'Jerry'},
    {'id': 3, 'name': 'DEFAULT'}
    )

    users = await db.table('users').select('id', 'name')
    print(users[0]['name'])

if __name__ == "__main__":
    init()
    asyncio.run(maintest(db))
