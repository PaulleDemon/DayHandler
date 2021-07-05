
class ThemeController:

    """ This class controls the theme. Any theme change is to be handled by this class.
    It also notifies theme change to registered classes """

    main_app = None  # must register main QApplication class
    icon_classes = set()  # register classes which has icon associated with it

    dark_theme_images = {"delete": r"Resources/Images/DarkThemeImages/Delete_black.png",
                         "goal": r"Resources/Images/DarkThemeImages/Goal_black.png",
                         "home": r"Resources/Images/DarkThemeImages/Home_Black.png",
                         "project": r"Resources/Images/DarkThemeImages/Project_black.png",
                         "settings": r"Resources/Images/DarkThemeImages/Settings_dark.png",
                         "todo": r"Resources/Images/DarkThemeImages/Todo_black.png"
                         }

    light_theme_images = {"delete": r"Resources/Images/LightThemeImages/Delete_white.png",
                          "goal": r"Resources/Images/LightThemeImages/Goal_white.png",
                          "home": r"Resources/Images/LightThemeImages/Home_white.png",
                          "project": r"Resources/Images/LightThemeImages/Project_white.png",
                          "settings": r"Resources/Images/LightThemeImages/Settings_Light.png",
                          "todo": r"Resources/Images/LightThemeImages/Todo_white.png"
                          }

    current_theme_file = r"UserResources/current_theme.txt"

    current_theme = "dark"
    _themes = {0: "dark", 1: "light"}
    theme_paths = {0: r"Resources/DarkTheme.qss", 1: r"Resources/LightTheme.qss"}

    @classmethod
    def get_theme_info(cls):
        return f"ThemeController({cls.dark_theme_images}; {cls.light_theme_images})"

    @classmethod
    def get_theme_keys(cls):
        return f"{list(cls.dark_theme_images.keys())}"

    @classmethod
    def get_image(cls, key: str) -> str:
        return cls.dark_theme_images[key] if cls.current_theme == "light" else cls.light_theme_images[key]

    @classmethod
    def get_current_theme(cls):
        return cls.current_theme

    @classmethod
    def get_current_theme_index(cls):
        return 0 if cls.current_theme == "dark" else 1

    @classmethod
    def _set_theme(cls, theme: int):
        try:
            cls.current_theme = cls._themes[theme]

        except KeyError:
            raise Exception(f"Invalid theme {theme}. Only 0/1 is accepted")

    @classmethod
    def register_main_app(cls, app):  # must register a QApplication instance or class to which stylesheet is applied
        cls.main_app = app

    @classmethod
    def load_theme(cls, theme=None):  # used to load theme

        if theme is None:
            try:
                with open(cls.current_theme_file) as file:
                    theme = int(file.read())

            except Exception as e:
                print(f"Exception: {e}")
                theme = 1

        if theme not in [0, 1]:
            theme = 1

        with open(cls.theme_paths[theme]) as file:
            theme_file = file.read()

        try:
            with open(cls.current_theme_file, 'w') as file:
                file.write(str(theme))

        except Exception:
            pass

        cls._set_theme(theme)
        cls.main_app.setStyleSheet(theme_file)
        cls.notify_theme_change()

    @classmethod
    def register_icon_class(cls, icon_class):  # register classes that needs to be notified od change in the theme
        cls.icon_classes.add(icon_class)

    @classmethod
    def notify_theme_change(cls):  # notifies the registered class of the change in theme so they can switch icons

        for item in cls.icon_classes:
            try:
                item.load_icon()

            except NameError:
                raise NotImplementedError
