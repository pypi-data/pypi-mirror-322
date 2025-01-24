from typer import Typer


system = Typer(help="", no_args_is_help=True)

@system.command("init")
def init():
    """
    Initialize the service. It will add a service to linux systemd, to startup on boot.
    """
    

@system.command("status")
def status():
    """
    Check the status of the background service.
    """

