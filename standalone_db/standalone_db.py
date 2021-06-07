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
    print("db: " , db)


def maintest(db:DB):
    async def make_table():
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

    async def add_users():
        db.table('users').insert(
            {'id': 1, 'name': 'Tom'},
            {'id': 2, 'name': 'Jerry'},
            {'id': 3, 'name': 'DEFAULT'}
            )
    async def get_user():
        result = db.table('users').select('id', 'name')
        return result

    asyncio.get_event_loop().run_until_complete(make_table())
    asyncio.get_event_loop().run_until_complete(add_users())

    users = asyncio.get_event_loop().run_until_complete(get_user())


    print(type(users))
    print(users)
    print(users.table('users'))
    print(users[0]['name'])


def Async_maintest(db:DB):
    async def make_table():
        await db.schema('TABLE users').create(
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

    async def add_users():
        await db.table('users').insert(
            {'id': 1, 'name': 'Tom'},
            {'id': 2, 'name': 'Jerry'},
            {'id': 3, 'name': 'DEFAULT'}
            )
    async def get_user():
        result = await db.table('users').select('id', 'name')
        return result

    asyncio.get_event_loop().run_until_complete(make_table())
    asyncio.get_event_loop().run_until_complete(add_users())

    users = asyncio.get_event_loop().run_until_complete(get_user())


    print(type(users))
    print(users)
    print(users.table('users'))
    print(users[0]['name'])

if __name__ == "__main__":
    init()
    #Async_maintest(db)
    maintest(db)
