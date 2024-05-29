from typing import List

from app.config.configuration import Configuration
from app.config.profile import Profile
from app.interface import Interface

def _display_profile(profile: Profile, user_interface: Interface) -> None:
    """Display throught the interface the profile's presentation including metadatas
    @param profile: Profile
    @param user_interface: Interface
    """
    user_interface.request_output_to_user(f"Profile: {profile.name}")

    unique_tags = set()
    for audio_metadata in profile.audio_metadatas:
        unique_tags = unique_tags | set(audio_metadata.tags)
    unique_tags = list(unique_tags)
    unique_tags.sort()
    tags_list = ", ".join(unique_tags)
    user_interface.request_output_to_user(f"\nTags found:\n {tags_list}")

    user_interface.request_output_to_user("\nAudio's list:")
    for audio_metadata in profile.audio_metadatas:
        track_info = f"{audio_metadata.name}"
        track_info += f"by {audio_metadata.author}" if audio_metadata.author is not None else ''
        track_info += ', tags: '
        track_info += f"{audio_metadata.tags}" if audio_metadata.tags else 'no'
        track_info += ', source: ' + 'yes' if audio_metadata.source != '' else 'no'
        user_interface.request_output_to_user(
            f"- {track_info}"
        )

def request_profile(args: list | None, configuration: Configuration, user_interface: Interface) -> Profile:
    """Change the app's profile or display the current profile if no arguments are given
    @param args: List[str] or None
    @param configuration: Configuration
    @param user_interface: Interface
    @return Profile
    """
    if len(args) < 0:
        return None
    # Update profile or not
    if len(args) == 1:
        if configuration.profile is None:
            user_interface.request_output_to_user(
                "There is no profile set. Please set a profile."
            )
            return
        _display_profile(configuration.profile, user_interface)
        return configuration.profile
    
    profile_name = str(args[1]) # TODO is the profile name just a string without space allowed or can it have space?
    if profile_name not in configuration.get_profiles():
        user_interface.request_output_to_user(f"Warning: Unknown profile: \"{profile_name}\"")
        return configuration.profile

    configuration.profile = Profile(name=profile_name)
    configuration.fill_profile_with_metadata(user_interface)
    n_metadatas = len(configuration.profile.audio_metadatas)
    user_interface.request_output_to_user(f"Info: Profile updated: \"{n_metadatas}\" lines of metadatas found.")

    return configuration.profile
