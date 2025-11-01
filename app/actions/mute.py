
from app.interface import Interface
from app.message_priority import MessagePriority


def mute(args: list, user_interface: Interface) -> None:
    """Mute the message of the <interface>
    @param args: Tuple[Command, [str]] or None, expecting "mute <priority>
    @param user_interface: Interface
    """
    if len(args) == 0:
        return None
    if len(args) == 1:
        muteness_status = user_interface.muteness_status()
        user_interface.request_output_to_user(muteness_status, MessagePriority.WARNING)
        return
    if len(args) > 2:
        return None
    
    try:
        priority = MessagePriority.from_string(args[1])
    except ValueError as value_error:
        user_interface.request_output_to_user(f"Unknown {priority} priority : ", MessagePriority.WARNING)
        return None
    user_interface.request_output_to_user(f"Muting the {priority} priority : ", MessagePriority.WARNING)
    user_interface.mute_message(priority)

def unmute(args: list, user_interface: Interface) -> None:
    """Unmute the message of the <interface>
    @param args: Tuple[Command, [str]] or None, expecting "mute <priority>
    @param user_interface: Interface
    """
    if len(args) == 0:
        return None
    if len(args) == 1:
        muteness_status = user_interface.muteness_status()
        user_interface.request_output_to_user(muteness_status, MessagePriority.WARNING)
        return
    if len(args) > 2:
        return None
    
    try:
        priority = MessagePriority.from_string(args[1])
    except ValueError as value_error:
        user_interface.request_output_to_user(f"Unknown {priority} priority : ", MessagePriority.WARNING)
        return None
    user_interface.request_output_to_user(f"Muting the {priority} priority : ", MessagePriority.WARNING)
    user_interface.unmute_message(priority)