import asyncio

from windyquery import DB

db = DB()
asyncio.new_event_loop().run_until_complete(db.connect('PRAXIS_BOT_DB', {
    'host' : 'standalone_db',
    'port' : '5432',
    'database' : 'PRAXIS_BOT_DB',
    'username' : 'PRAXIS_BOT',
    'password' : '#Praxis#Praxis#Praxis',
}, default=True))

def init():
    print("test")

if __name__ == "__main__":
    init()
