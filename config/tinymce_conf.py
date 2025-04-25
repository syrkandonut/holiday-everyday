# HTML Editor Window width and height
WINDOW_WIDTH: str = "2000px"
WINDOW_HEIGHT: str = "700px"

# Menubar options, for example file, edit, etc.
MENUBAR: bool = False

# Encoding raw for HTML format. & != &amp, < != &lt
ENTITY_ENCODING: str = "raw"

# Plugins
PLUGINS: str = str(" ").join(
    ["autosave", "save", "fullscreen", "image", "link", "wordcount"]
)

# Toolbar
TOOLBAR: str = str(" | ").join(
    ["fullscreen", "undo redo", "styles", "blockquote", "link image"]
)

# Style text formats. For example <p>, h1, h2, etc.
STYLE_TITLE_H3: str = "Заголовок"
STYLE_VALUE_H3: str = "h3"

STYLE_TITLE_H4: str = "Подзаголовок"
STYLE_VALUE_H4: str = "h4"

STYLE_TITLE_P: str = "Обычный"
STYLE_VALUE_P: str = "p"

STYLE_FORMATS: list[dict[str, str]] = [
    {
        "title": STYLE_TITLE_H3,
        "format": STYLE_VALUE_H3,
    },
    {
        "title": STYLE_TITLE_H4,
        "format": STYLE_VALUE_H4,
    },
    {
        "title": STYLE_TITLE_P,
        "format": STYLE_VALUE_P,
    },
]

# Undo-redo history depth
UNDO_REDO_LEVELS: int = 50

# Image paster func JS
IMAGE_PASTE_FUNC: str = """function (cb, value, meta) {
        var input = document.createElement("input");
        input.setAttribute("type", "file");
        if (meta.filetype == "image") {
            input.setAttribute("accept", "image/*");
        }

        input.onchange = function () {
            var file = this.files[0];
            var reader = new FileReader();
            reader.onload = function () {
                var id = "blobid" + (new Date()).getTime();
                var blobCache = tinymce.activeEditor.editorUpload.blobCache;
                var base64 = reader.result.split(",")[1];
                var blobInfo = blobCache.create(id, file, base64);
                blobCache.add(blobInfo);
                cb(blobInfo.blobUri(), { title: file.name });
            };
            reader.readAsDataURL(file);
        };
        input.click();
    }"""

IMAGE_SETTINGS: dict[str, bool] = {
    "image_dimensions": False,
    "image_description": False,
}

# Default content style
DEFAULT_CONTENT_STYLE = (
    "body { font-family:Roboto,Helvetica,Arial,sans-serif; font-size:14px }"
)

TINYMCE_DEFAULT_CONFIG = {
    "width": WINDOW_WIDTH,
    "height": WINDOW_HEIGHT,
    "content_style": DEFAULT_CONTENT_STYLE,
    "entity_encoding": ENTITY_ENCODING,
    "menubar": MENUBAR,
    "plugins": PLUGINS,
    "toolbar": TOOLBAR,
    "style_formats": STYLE_FORMATS,
    "custom_undo_redo_levels": UNDO_REDO_LEVELS,
    "file_picker_callback": IMAGE_PASTE_FUNC,
    **IMAGE_SETTINGS,
}
