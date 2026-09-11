import ui

class RandomPickerScreen(ui.View):

    def __init__(self):
        super().__init__()
        self.presenter = None

        self.name = "Pokémon Generator"
        self.background_color = 'white'

        # Title
        self.title_label = ui.Label()
        self.title_label.text = "Random Pokémon Picker"
        self.title_label.alignment = ui.ALIGN_CENTER
        self.title_label.font = ('<System-Bold>', 20)

        # Slider label
        self.slider_label = ui.Label()
        self.slider_label.alignment = ui.ALIGN_CENTER

        # Slider (1–10)
        self.slider = ui.Slider()
        self.slider.continuous = True
        self.slider.value = 0.5
        self.slider.action = self.on_slider_change

        # Generate button
        self.generate_button = ui.Button(title="Generate")
        self.generate_button.action = self.on_generate_pressed

        # TableView for Pokémon list
        self.table_view = ui.TableView()
        self.table_view.data_source = self
        self.table_view.delegate = self

        # Internal state
        self._pokemon = []

        for v in (
            self.title_label,
            self.slider_label,
            self.slider,
            self.generate_button,
            self.table_view,
        ):
            self.add_subview(v)

        self.update_slider_label()

    # ---------- Layout (responsive) ----------

    def layout(self):
        w, h = self.width, self.height
        padding = 16

        self.title_label.frame = (0, padding, w, 30)

        self.slider_label.frame = (
            padding,
            self.title_label.y + 40,
            w - padding * 2,
            24
        )

        self.slider.frame = (
            padding,
            self.slider_label.y + 26,
            w - padding * 2,
            34
        )

        self.generate_button.frame = (
            padding,
            self.slider.y + 44,
            w - padding * 2,
            44
        )

        self.table_view.frame = (
            0,
            self.generate_button.y + 54,
            w,
            h - (self.generate_button.y + 54)
        )

    # ---------- UI Events ----------

    def on_slider_change(self, sender):
        self.update_slider_label()

    def update_slider_label(self):
        count = int(self.slider.value * 9) + 1
        self.slider_label.text = f"Number of Pokémon: {count}"

    def on_generate_pressed(self, sender):
        count = int(self.slider.value * 9) + 1
        self.presenter.on_generate_pressed(count)

    # ---------- Presenter Callbacks ----------

    def show_random_pokemon(self, pokemon_list):
        """
        pokemon_list = List[Pokemon]
        """
        self._pokemon = pokemon_list
        self.table_view.reload()

    # ---------- TableView Data Source ----------

    def tableview_number_of_rows(self, tableview, section):
        return len(self._pokemon)

    def tableview_cell_for_row(self, tableview, section, row):
        cell = ui.TableViewCell('subtitle')
        pokemon = self._pokemon[row]

        cell.detail_text_label.alignment = ui.ALIGN_RIGHT

        # Assumes a Pokemon object (not just name)
        cell.text_label.text = pokemon.name
        cell.detail_text_label.text = pokemon.gameshark_code
        cell.accessory_type = 'disclosure_indicator'
        return cell

    # ---------- TableView Delegate ----------

    def tableview_did_select(self, tableview, section, row):
        pokemon = self._pokemon[row]
        self.presenter.on_pokemon_selected(pokemon)
