class ImagePaths:
    dark_theme_images = {"delete": r"Resources/Images/DarkThemeImages/Delete_black.png",
                         "goal": r"Resources/Images/DarkThemeImages/Goal_black.png",
                         "home": r"Resources/Images/DarkThemeImages/Home_Black.png",
                         "project": r"Resources/Images/DarkThemeImages/Project_black.png",
                         "settings": r"Resources/Images/DarkThemeImages/Settings_black.png",
                         "todo": "Resources/Images/DarkThemeImages/Todo_black.png"
                         }

    light_theme_images = {"delete": r"Resources/Images/LightThemeImages/Delete_white.png",
                          "goal": r"Resources/Images/LightThemeImages/Goal_white.png",
                          "home": r"Resources/Images/LightThemeImages/Home_white.png",
                          "project": r"Resources/Images/LightThemeImages/Project_white.png",
                          "settings": r"Resources/Images/LightThemeImages/Settings_white.png",
                          "todo": "Resources/Images/LightThemeImages/Todo_white.png"
                          }

    current_theme = "dark"
    _themes = {0: "dark", 1: "light"}

    @classmethod
    def __repr__(cls):
        return f"ImagePaths({cls.dark_theme_images}; {cls.light_theme_images})"

    @classmethod
    def __str__(cls):
        return f"{cls.dark_theme_images.keys()}"

    @classmethod
    def get_image(cls, key: str) -> str:
        return cls.dark_theme_images[key] if cls.current_theme == "light" else cls.light_theme_images[key]

    @classmethod
    def theme(cls):
        return cls.current_theme

    @classmethod
    def set_theme(cls, theme: int):
        try:
            cls.current_theme = cls._themes[theme]

        except KeyError:
            raise Exception(f"Invalid theme {theme}. Only 0/1 is accepted")
