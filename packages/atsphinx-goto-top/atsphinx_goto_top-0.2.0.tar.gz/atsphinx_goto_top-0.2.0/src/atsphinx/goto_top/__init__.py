"""Add navigation buttion that scroll to top of page."""

from pathlib import Path
from typing import Optional

from docutils import nodes
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.locale import get_translation

__version__ = "0.2.0"

here = Path(__file__).parent
locale_dir = here / "locales"

_ = get_translation(__name__)


def register_config(app: Sphinx, config: Config):
    """Add config values for using extension."""
    config.templates_path.append(str(here / "templates"))
    config.html_static_path.insert(0, str(here / "static"))
    config.html_js_files.append("goto-top/main.js")
    config.html_css_files.append("goto-top/style.css")
    config.html_context["goto_top"] = {
        "design": config.goto_top_design,
        "scroll_behavior": config.goto_top_scroll_behavior,
        "content_id": config.goto_top_content_id,
        "template_id": config.goto_top_template_id,
        "side": config.goto_top_side,
        "button_text": config.goto_top_text or _("Back to top"),
    }


def append_template_element(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: dict,
    doctree: Optional[nodes.document],
) -> None:
    """Inject <template> into metadata."""
    name = "goto-top/navigation.html"
    if app.config.goto_top_design:
        name = f"goto-top/navigation-{app.config.goto_top_design}.html"
    template = app.builder.templates.render(name, context)
    context.setdefault("metatags", "")
    context["metatags"] += (
        f'<template id="{app.config.goto_top_template_id}">{template}</template>'
    )


def setup(app: Sphinx):  # noqa: D103
    app.add_config_value("goto_top_design", "", "env", str)
    app.add_config_value("goto_top_scroll_behavior", "auto", "env", str)
    app.add_config_value("goto_top_template_id", "tmpl_gotoTop", "env", str)
    app.add_config_value("goto_top_content_id", "gotoTop", "env", str)
    app.add_config_value("goto_top_side", "right", "env", str)
    app.add_config_value("goto_top_text", None, "env")
    app.add_message_catalog(__name__, str(locale_dir))
    app.connect("config-inited", register_config)
    app.connect("html-page-context", append_template_element)
    return {
        "version": __version__,
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
