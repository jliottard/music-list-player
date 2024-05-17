from app import configuration
from app.interface import Interface
from app.profile import Profile
from audio_import.audio_metadata import AudioMetadata
from audio_import.plain_text_parse import parse_plain_text_playlist_file

def _display_profile(profile: Profile, user_interface: Interface) -> None:
    """ TODO"""
    user_interface.request_output_to_user(f"Profile: {profile.name}")

    unique_tags = set()
    for audio_metadata in profile.audio_metadatas:
        unique_tags = unique_tags | set(audio_metadata.tags)
    tags_list = ", ".join(unique_tags)
    user_interface.request_output_to_user(f"\nTags found:\n {tags_list}")

    user_interface.request_output_to_user("\nAudio's list:")
    for audio_metadata in profile.audio_metadatas:
        track_info = f"{audio_metadata.name}"
        track_info += f"by {audio_metadata.author}" if audio_metadata.author != '' else ''
        track_info += f", tags: {audio_metadata.tags}"
        track_info += ", source: " + "yes" if audio_metadata.source != '' else "no"
        user_interface.request_output_to_user(
            f"- {track_info}"
        )

def _fill_profile(profile: Profile, user_interface: Interface) -> Profile:
    """File the metadata fields of profile
    @param profile: Profile
    @param user_interface: Interface
    @return Profile: the same profile
    """
    profile.audio_metadatas = parse_plain_text_playlist_file(
        playlist_file_absolute_path=configuration.get_playlist_file_path(profile),
        user_interface=user_interface
    )
    return profile

def request_profile(args: list | None, current_profile: Profile, user_interface: Interface) -> Profile:
    """Change the app's profile or display the current profile if no arguments are given
    @param args: List[str] or None
    @param current_profile: Profile
    @param user_interface: Interface
    @return Profile,
        or None if there is not commands nor arguments given
    """
    if len(args) < 0:
        return None
    # Update profile or not
    if len(args) == 1:
        if current_profile is None:
            user_interface.request_output_to_user(
                "There is no profile set."
            )
            user_interface.request_output_to_user(
                f"Setting the default profile ({configuration.DEFAULT_PLAYLIST_PROFILE_NAME}) as the playlist profile."
            )
            current_profile = Profile(name=configuration.DEFAULT_PLAYLIST_PROFILE_NAME)
            current_profile = _fill_profile(current_profile, user_interface)
        _display_profile(current_profile, user_interface)
        return current_profile
    
    profile_name = str(args[1]) # TODO is the profile name just a string without space allowed or can it have space?
    if profile_name not in configuration.get_profiles():
        user_interface.request_output_to_user(f"Unknown profile: \"{profile_name}\"")
        return current_profile

    new_profile = Profile(name=profile_name)
    new_profile = _fill_profile(new_profile, user_interface)
    n_metadatas = len(new_profile.audio_metadatas)
    user_interface.request_output_to_user(f"Profile updated: \"{n_metadatas}\" lines of metadatas found.")

    return new_profile
