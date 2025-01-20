from keras.src.api_export import keras_export

# Unique source of truth for the version number.
__version__ = "3.8.0.dev2025012003"


@keras_export("keras.version")
def version():
    return __version__
