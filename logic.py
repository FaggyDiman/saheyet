from pydantic import BaseModel, model_validator
from typing import List, Optional, Dict

class PlayerState(BaseModel):
    player_id: int
    current_location_id: str
    navigation_stack: List[str] = []
    transition_context: Optional[Dict] = None
    health: int = 1
    health_max: int 
    health_commentary: str = ""
    health_commentary_stylecolor: str = ""
    portrait: str = "" 

    @model_validator(mode='after')
    def set_portrait_after_init(self) -> 'PlayerState':
        self.portrait = self.get_portrait_by_health()
        self.health_commentary = self.get_health_commentary()
        self.health_commentary_stylecolor = self.get_health_stylecolor()
        return self

    def get_portrait_by_health(self):
        match self.health:
            case 1: return "knight_very_bad.png"
            case 2: return "knight_bad.png"
            case 3: return "knight.png"
            case 4: return "knight_good.png"
            case 5: return "knight_very_good.png"
            case _: return "knight.png"

    def get_health_commentary(self):
        match self.health:
            case 1: return "health_very_bad"
            case 2: return "health_bad"
            case 3: return "health_normal"
            case 4: return "health_good"
            case 5: return "health_very_good"
            case _: return "health_normal"

    def get_health_stylecolor(self):
        match self.health:
            case 5: return "text-light-green"
            case 4: return "text-green"
            case 3: return "text-yellow"
            case 2: return "text-orange"
            case 1: return "text-red"
            case _: return "text-yellow"

