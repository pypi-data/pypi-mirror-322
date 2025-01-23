import typer
import uvicorn
from .lib.server_handler import VideoServer

app = typer.Typer()

@app.command()
def serve(
    port: int = typer.Option(8000, "-p", "--port", help="Port to serve on"),
    host: str = typer.Option("0.0.0.0", "-h", "--host", help="Host address to bind to")
):
    """
    Serve video files from the current directory
    """
    server = VideoServer()
    typer.echo(f"Starting video server at http://{host}:{port}")
    uvicorn.run(server.app, host=host, port=port)

def main():
    app()

if __name__ == "__main__":
    main()
