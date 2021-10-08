from typing import List, Optional, Union
from pydantic import BaseModel, Field
from fastapi import Form


class Effect(BaseModel):
    name: str


class Item(BaseModel):
    name: str
    item_img: Optional[str]


class Weapon(Item):
    attack: float
    dmg_multiplier_bonus: Optional[float] = 0.0


class Armor(Item):
    physical_defense: float
    magical_defense: float
    elemental_defense: float


class Spell(Item):
    dmg_bonus: Optional[float] = 0.0
    heal: Optional[float] = 0.0


item_model = Union[Weapon, Armor, Spell]

class BatchCharDelete(BaseModel):
    min_level: Optional[int]
    max_level: Optional[int]


class Character(BaseModel):
    name: str
    password: str
    id: int
    hp: float
    level: int
    xp: float
    kromers: int
    dark_dollars: int
    status_effects: List[Effect] = []
    owned_items: List[Item] = []
    char_portrait: Optional[str]
    theme_music: Optional[str]
    description: Optional[str] = Field(
        None, title = "The character's in-game description.", max_length = 300
    )
