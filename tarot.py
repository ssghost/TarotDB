from surrealdb import Surreal
import asyncio
import random
from typing import List

class Tarot:
    def __init__() -> None:
        pass

    async def upload(self) -> None:
        with open("./deck.json") as f:
            df = f.read()
        async with Surreal("ws://localhost:8000/rpc") as db:
            await db.signin({"user": "root", "pass": "root"})
            await db.use("tarotdb", "tarotdb")
            await db.delete(df)
            await db.create(df)
    
    async def pickcard(self, n:int, scope:str='all') -> List[str]:
        if scope == 'all':
            rlist = list(range(78))
        elif scope == 'major':
            rlist = list(range(22))
        elif scope == 'minor':
            rlist = list(range(22,78))
        pick: List[int] = random.sample(rlist, n)
        reslist: List[str] = []
        async with Surreal("ws://localhost:8000/rpc") as db:
            await db.signin({"user": "root", "pass": "root"})
            await db.use("tarotdb", "tarotdb")
            for p in pick:
                res = await db.query("SELECT * FROM deck WHERE enum=type::number($enum)", {'enum':p})
                reslist.append(str(res))
                await db.query("UPDATE deck SET picked=picked+1 WHERE enum=type::number($enum)", {'enum':p})
        return reslist
    
    async def viewcard(self, name:str) -> str:
        async with Surreal("ws://localhost:8000/rpc") as db:
            await db.signin({"user": "root", "pass": "root"})
            await db.use("tarotdb", "tarotdb")
            res = await db.query("SELECT * FROM deck WHERE name=type::string($name)", {'name':name})
        return str(res)
    
    async def changehost(self) -> str:
        pick: int = random.randint(0,21)
        async with Surreal("ws://localhost:8000/rpc") as db:
            await db.signin({"user": "root", "pass": "root"})
            await db.use("tarotdb", "tarotdb")
            await db.query("UPDATE deck SET is_host=false")
            res = await db.query("UPDATE deck SET is_host=true WHERE enum=type::number($enum)", {'enum':pick})
        return str(res)
    