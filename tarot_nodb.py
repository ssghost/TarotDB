import pandas as pd
import random
from typing import List

class TarotNodb:
    def __init__(self) -> None:
        with open("./deck.json", 'r') as f:
            self.deck = pd.read_json(f)

    def writejson(self) -> None:
        with open("./deck.json", 'w') as f:
            self.deck.to_json(f)
            
    
    async def pickcard(self, n:int, scope:str='all') -> List[str]:
        if scope == 'all':
            rlist = list(range(78))
        elif scope == 'major':
            rlist = list(range(22))
        elif scope == 'minor':
            rlist = list(range(22,78))
        pick: List[int] = random.sample(rlist, n)
        reslist: List[str] = []
        for p in pick:
            res = await self.db.query("SELECT * FROM deck WHERE enum=type::number($enum)", {'enum':p})
            reslist.append(str(res))
            await self.db.query("UPDATE deck SET picked=picked+1 WHERE enum=type::number($enum)", {'enum':p})
        return reslist
    
    async def viewcard(self, name:str) -> str:
        res = await self.db.query("SELECT * FROM deck WHERE name=type::string($name)", {'name':name})
        return str(res)
    
    async def changehost(self) -> str:
        pick: int = random.randint(0,21)
        await self.db.query("UPDATE deck SET is_host=false")
        res = await self.db.query("UPDATE deck SET is_host=true WHERE enum=type::number($enum)", {'enum':pick})
        return str(res)
    
    async def close(self) -> None:
        await self.db.close()