from enum import Enum

from django.utils.html import format_html
from django.utils.safestring import SafeString

from config.settings import SERVER_URI


class HTMLColor(Enum):
    WHITE = "white"
    BLACK = "black"
    GREEN = "green"
    GREY = "grey"
    RED = "#ba2120"


def html_get_thumbnail(image_url: str) -> SafeString:
    width: str = "100px"
    height: str = "auto"
    style: str = f'style="width: {width}; height: {height};"'

    html_string: str = '<img src="{}" ' + style + " />"

    return format_html(html_string, image_url)


def html_get_button(
    button_color: HTMLColor,
    text_color: HTMLColor,
    button_text: str,
    source_url: str,
) -> SafeString:
    style: str = (
        f'style="background-color: {button_color.value}; color: {text_color.value};"'
    )

    html_string: str = '<a class="button" href="{}"' + style + ">{}</a>"

    return format_html(html_string, source_url, button_text)


def html_get_preview_with_thumbnail(project_id: int, image_url: str) -> SafeString:
    width: str = "100px"
    height: str = "auto"
    href_to: str = "portfolio"

    style: str = f'style="width: {width}; height: {height};"'

    html_string: str = (
        '<a href="{}/{}/{}/" ' + 'target="_blank">' + '<img src="{}"' + style + "/></a>"
    )

    return format_html(html_string, SERVER_URI, href_to, project_id, image_url)


def html_get_preview_without_thumbnail(
    project_id: int, warning_text: str
) -> SafeString:
    html_string: str = '<a href="{}/portfolio/{}/" target="_blank">{}</a>'

    return format_html(html_string, SERVER_URI, project_id, warning_text)
