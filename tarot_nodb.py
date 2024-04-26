import pandas as pd
import random
from typing import List

class TarotNodb:
    def __init__(self) -> None:
        with open("./deck.json", 'r') as f:
            self.deck = pd.read_json(f)

    def writejson(self) -> None:
        with open("./deck.json", 'w') as f:
            self.deck.to_json(f, orient='records')
            
    def pickcard(self, n:int, scope:str='all') -> List[str]:
        if scope == 'all':
            rlist = list(range(78))
        elif scope == 'major':
            rlist = list(range(22))
        elif scope == 'minor':
            rlist = list(range(22,78))
        pick: List[int] = random.sample(rlist, n)
        reslist: List[str] = []
        for p in pick:
            res = self.deck.loc[self.deck['enum']==p]
            reslist.append(str(res))
            self.deck.loc[self.deck['enum']==p, 'picked']+=1
        return reslist
    
    def viewcard(self, name:str) -> str:
        res = self.deck.loc[self.deck['name'] == name]
        return str(res)
    
    def changehost(self) -> str:
        pick: int = random.randint(0,21)
        self.deck['is_host'] = False
        self.deck.loc[self.deck['enum']==pick]['is_host'] = True
        res = self.deck.loc[self.deck['enum']==pick] 
        return str(res)

