from app.command import Command

def print_help() -> None:
    """Print the command names and their usage"""
    print("The available commands are :")
    for command in list(Command):
        help_text = command.help()
        print(f"- {command.value:10s}\t{help_text}")
