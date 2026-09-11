from app.common.PokemonInfoService import PokemonInfoService

from app.screen.randompicker.RandomPickerScreen import RandomPickerScreen
from app.screen.randompicker.RandomPickerPresenter import RandomPickerPresenter

class Injector:

    def __init__(self):
        self.pokemon_info_service: PokemonInfoService = None


    """ Services """

    def get_pokemon_info_service(self) -> PokemonInfoService:
        if not self.pokemon_info_service:
            self.pokemon_info_service = PokemonInfoService()
        return self.pokemon_info_service


    """ Screens """

    def get_random_picker_screen(self) -> RandomPickerScreen:
        view = RandomPickerScreen()
        presenter = RandomPickerPresenter(view=view)
        presenter.inject(injector=self)
        view.presenter = presenter
        return view
    