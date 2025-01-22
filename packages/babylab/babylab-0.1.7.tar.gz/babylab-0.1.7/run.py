"""Run app."""

from .babylab.app import create_app

app = create_app(env="prod")

if __name__ == "__main__":
    app.run(debug=False)
