from app.common.Injector import Injector

from app.screen.randompicker.RandomPickerScreen import RandomPickerScreen
from app.screen.randompicker.RandomPickerPresenter import RandomPickerPresenter

def main():
    injector = Injector()

    view = injector.get_random_picker_screen()
    view.present('fullscreen')
    

if __name__ == '__main__':
    main()
