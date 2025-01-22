""" Plugin for mkdocs that adds custom markdown extensions. """

from mkdocs.plugins import BasePlugin
from mkdocs.utils import copy_file
from mkdocs.config import base, config_options as c
from .regex import RegexExtension
from .unicode import UnicodeExtension
from pathlib import Path

class PillsConfig(base.Config):
    language = c.Optional(c.Type(str))
    regex = c.Type(bool, default=True)
    unicode = c.Type(bool, default=True)

class PillsPlugin(BasePlugin[PillsConfig]):
    """Plugin for mkdocs that adds custom markdown extensions."""

    def __init__(self):
        self.css_output_path = None
        self.css_base_path = None
        super().__init__()

    def on_config(self, config):
        """Add the custom markdown extensions to the config."""

        # Guess language if not provided
        if not hasattr(self, 'language'):
            if hasattr(config.theme, 'language'):
                self.language = config.theme.language
            elif hasattr(config.theme, 'locale'):
                self.language = config.theme.locale.language

        if self.config.regex:
            config["markdown_extensions"].append(RegexExtension())

        if self.config.unicode:
            config["markdown_extensions"].append(UnicodeExtension(language=self.language))

        css = Path("css/pills.css")
        self.css_output_path = Path(config["site_dir"]) / css
        self.css_base_path = Path(__file__).parent / css

        config["extra_css"].append(str(css))

    def on_post_build(self, config):
        """Copy the epigraph.css file to the site directory."""
        _ = config
        copy_file(self.css_base_path, self.css_output_path)

        icons_base_path = Path(__file__).parent / "css"
        icons_output_path = Path(config["site_dir"]) / "css"

        for icon in ["regex.svg", "unicode.svg"]:
            copy_file(icons_base_path / icon, icons_output_path / icon)
