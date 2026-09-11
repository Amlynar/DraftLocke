import json
import copy

from dataclasses import dataclass
from typing import Optional, List, Dict


# ---------- Core leaf objects ----------

@dataclass
class GeneralInfo:
    pokedex_number: str
    type: str

    @staticmethod
    def parse_general(data: dict) -> "GeneralInfo":
        return GeneralInfo(
            pokedex_number=data["pokedexNumber"],
            type=data["type"]
        )


@dataclass
class EvolutionStage:
    name: str
    type: Optional[str]
    level: Optional[int]
    stone: Optional[str]

    @staticmethod
    def parse_evolution(data: dict) -> "EvolutionStage":
        return EvolutionStage(
                name=data["name"],
                type=data["type"],
                level=data["level"],
                stone=data["stone"]
            )

    @staticmethod
    def parse_evolutions(data: list) -> List["EvolutionStage"]:
        return [
            EvolutionStage.parse_evolution(e)
            for e in data
        ]


@dataclass
class Move:
    name: str
    type: str
    power: Optional[int]
    accuracy: Optional[int]
    pp: int


@dataclass
class LevelUpMove(Move):
    level: int

    @staticmethod
    def parse_level_up_move(data: dict) -> "LevelUpMove":
        return LevelUpMove(
                level=data["level"],
                name=data["name"],
                type=data["type"],
                power=data["power"],
                accuracy=data["accuracy"],
                pp=data["pp"]
            )

    @staticmethod
    def parse_level_up_moves(data: list) -> List["LevelUpMove"]:
        return [
            LevelUpMove.parse_level_up_move(m)
            for m in data
        ]


@dataclass
class TMMove(Move):
    number: str
    location: str

    @staticmethod
    def parse_tm_move(data: dict) -> "TMMove":
        return TMMove(
                number=data["number"],
                name=data["name"],
                type=data["type"],
                power=data["power"],
                accuracy=data["accuracy"],
                pp=data["pp"],
                location=data["location"]
            )

    @staticmethod
    def parse_tm_moves(data: list) -> List["TMMove"]:
        return [
            TMMove.parse_tm_move(m)
            for m in data
        ]


@dataclass
class HMMove(Move):
    number: str

    @staticmethod
    def parse_hm_move(data: dict) -> "HMMove":
        return HMMove(
                number=data["number"],
                name=data["name"],
                type=data["type"],
                power=data["power"],
                accuracy=data["accuracy"],
                pp=data["pp"]
            )

    @staticmethod
    def parse_hm_moves(data: list) -> List["HMMove"]:
        return [
            HMMove.parse_hm_move(m)
            for m in data
        ]


@dataclass
class BaseStats:
    hp: int
    attack: int
    defense: int
    special: int
    speed: int
    total: int
    average: float

    @staticmethod
    def parse_base_stats(data: dict) -> "BaseStats":
        return BaseStats(**data)


# ---------- Aggregate Pokémon ----------

@dataclass
class Pokemon:
    name: str
    general: GeneralInfo
    evolution: List[EvolutionStage]
    gameshark_code: str
    level_up_moves: List[LevelUpMove]
    tm_moves: List[TMMove]
    hm_moves: List[HMMove]
    base_stats: BaseStats

    @staticmethod
    def parse_pokemon(name: str, data: dict) -> "Pokemon":
        return Pokemon(
            name=name,
            general=GeneralInfo.parse_general(data["general"]),
            evolution=EvolutionStage.parse_evolutions(data["evolution"]),
            gameshark_code=data["gamesharkCode"],
            level_up_moves=LevelUpMove.parse_level_up_moves(data["levelUpMoves"]),
            tm_moves=TMMove.parse_tm_moves(data["tmMoves"]),
            hm_moves=HMMove.parse_hm_moves(data["hmMoves"]),
            base_stats=BaseStats.parse_base_stats(data["baseStats"]),
        )
    
    @staticmethod
    def load_pokemon(data: Dict[str, dict]) -> Dict[str, "Pokemon"]:
        pokedex = {}

        for name, p in data.items():
            pokedex[name] = Pokemon.parse_pokemon(name=name,data=p)

        return pokedex


# ---------- Service ----------

class PokemonInfoService:

    def __init__(self):
        self.pokedex: Dict[str, Pokemon] = None
        self.pokemon = None
        self.base_evolution_names = None

    def get_pokedex(self):
        self.load_pokedex()
        return copy.deepcopy(self.pokedex)


    def load_pokedex(self):
        if self.pokedex is None:
            file_name = 'data/pokemon_info.json'
            json_data = self.read_json_file(file_name)
            self.pokedex = Pokemon.load_pokemon(json_data)
            self.pokemon = list(self.pokedex.keys())

    def load_base_evolution_pokemon(self) -> List[Pokemon]:
        if self.base_evolution_names is None:
            base_pokemon = []

            for pokemon in self.pokedex.values():
                if pokemon.evolution and pokemon.evolution[0].name == pokemon.name:
                    base_pokemon.append(pokemon.name)

            self.base_evolution_names =  base_pokemon



        
    def read_json_file(self, filename):
        """
        Reads a JSON file and returns a Python dictionary/list.
        """
        try:
            # Open the file in read mode ('r') using a 'with' statement
            with open(filename, 'r') as file:
                # Use json.load() to deserialize the file's content
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from the file '{filename}'. Check file format.")
            return None

