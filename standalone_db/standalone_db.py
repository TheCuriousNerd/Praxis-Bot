import asyncio

from windyquery import DB

db = DB()

async def init():
    initConnection()
    if await isSetup():
        await setupTables()


async def initConnection():
    asyncio.get_event_loop().run_until_complete(db.connect('db_name', {
        'host' : 'localhost',
        'port' : '5432',
        'database' : 'PRAXIS_BOT_DB',
        'username' : 'PRAXIS_BOT',
        'password' : '#Praxis#Praxis#Praxis',
    }, default=True))

async def isSetup():
    return False

async def setupTables():
    await db.schema('TABLE IF NOT EXISTS Praxis_KeyValues_String').create(
        'id             serial PRIMARY KEY',
        'key            text',
        'value          text'
    )


if __name__ == "__main__":
    init()