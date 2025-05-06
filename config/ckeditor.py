_CKEDITOR_REMOVE_PLUGINS: dict[str, list[str]] = {
    "removePlugins": ["MediaEmbedToolbar", "ImageToolbar", "figure"]
}

_CKEDITOR_TOOLBAR: dict[str, dict[str, list[str]]] = {
    "toolbar": {"items": ["heading", "|", "link", "blockQuote", "imageUpload"]}
}
_CKEDITOR_HEADING: dict[str, dict[str, list[dict[str, str]]]] = {
    "heading": {
        "options": [
            {
                "model": "paragraph",
                "title": "Обычный",
                "class": "ck-heading_paragraph",
            },
            {
                "model": "heading1",
                "view": "h1",
                "title": "Заголовок",
                "class": "ck-heading_heading1",
            },
            {
                "model": "heading2",
                "view": "h2",
                "title": "Подзаголовок",
                "class": "ck-heading_heading2",
            },
        ]
    }
}

CKEDITOR_5_CONFIGS = {
    "default": {
        **_CKEDITOR_REMOVE_PLUGINS,
        **_CKEDITOR_TOOLBAR,
        **_CKEDITOR_HEADING,
    }
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = (
    "authenticated"  # Possible values: "staff", "authenticated", "any"
)

CKEDITOR_5_UPLOAD_FILE_TYPES = ["jpeg", "jpg", "png", "gif", "jfif", "webp", "bmp"]
