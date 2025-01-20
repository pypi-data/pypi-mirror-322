import typer
from .pkicompose import process_yaml

app = typer.Typer()
app.command()(process_yaml)

if __name__ == "__main__":
    app()