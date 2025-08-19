from app.command import Command
from app.interface import Interface
from app.message_priority import MessagePriority

def print_help(user_interface: Interface) -> None:
    """Print the command names and their usage
    @param user_interface: Interface
    """
    user_interface.request_output_to_user("The available commands are :", MessagePriority.INFO)
    for command in list(Command):
        help_text = command.help()
        user_interface.request_output_to_user(f"- {command.value:10s}\t{help_text}", MessagePriority.INFO)
