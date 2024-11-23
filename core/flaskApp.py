from flask import Flask

app = Flask(
    __name__,
    static_url_path='',
    static_folder='static',
    # template_folder='web/templates', # TODO?
)

# Module exports...
__all__ = [
    'app',
]
