import random
from typing import List

# Remove after
from framework.alert.alert_dialog import PYIAlert


from app.common.PokemonInfoService import PokemonInfoService, Pokemon


class RandomPickerPresenter:

    def __init__(self, view):
        self.view = view
        self.base_evolution_pokemon = None

    def inject(self, injector):
        self.pokemon_info_service: "PokemonInfoService" = injector.get_pokemon_info_service()

    # ---------- View Callbacks ----------

    def on_generate_pressed(self, count: int):
        PYIAlert.simple_alert(title="Error",message="View is None")
        
        pokemon_pool = self.get_base_evolution_pokemon()
        # self.view.show_random_pokemon(pokemon_pool)

        selected = random.sample(pokemon_pool, count)
        self.view.show_random_pokemon(selected)

    def on_pokemon_selected(self, pokemon):
        """
        Hook for future:
        - push detail screen
        - show modal
        - log selection
        """
        print(f"Selected Pokémon: {pokemon.name}")


    # ---------- Helper Functions ----------

    def get_base_evolution_pokemon(self):
        if self.base_evolution_pokemon is None:

            base_pokemon = []
            pokedex = self.pokemon_info_service.get_pokedex()

            for pokemon in pokedex.values():
               if pokemon.evolution and pokemon.evolution[0].name == pokemon.name:
                base_pokemon.append(pokemon)

            # self.base_evolution_pokemon = self.get_banned_pokemon(base_pokemon)
            self.base_evolution_pokemon = base_pokemon
        return self.base_evolution_pokemon
    
    def is_final_evolution(self, pokemon: Pokemon) -> bool:
        return (
            pokemon.evolution
            and pokemon.evolution[-1].name.lower() == pokemon.name.lower()
        )

    
    def get_final_evolution_name(self, pokemon: Pokemon) -> str | None:
        if not pokemon.evolution:
            return None
        return pokemon.evolution[-1].name
    
    def is_overpowered_final(self, pokemon: Pokemon) -> bool:
        return (
            pokemon.base_stats.total >= 420
            and self.is_final_evolution(pokemon)
        )

    def get_banned_pokemon(self, pokemon_list: list[Pokemon]) -> list[Pokemon]:
        banned = []

        # Build lookup by name for fast access
        pokemon_by_name = {p.name: p for p in pokemon_list}

        # Find all overpowered final evolutions
        overpowered_finals = {
            p.name
            for p in pokemon_list
            if self.is_overpowered_final(p)
        }

        for pokemon in pokemon_list:
            final_name = self.get_final_evolution_name(pokemon)

            if final_name in overpowered_finals:
                banned.append(pokemon)

        return banned



