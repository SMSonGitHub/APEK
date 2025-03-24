import pyaudacity as pa
import os

# Path to the room tone and silence tracks
room_tone_path = r"F:\Path\To\Room Tone.wav"  # Update this to the correct path for room tone
silence_path = r"F:\Path\To\Silence.wav"  # Update this to the correct path for 6 seconds of silence


def add_room_tone_and_silence(clip_path: str, silence_needed: bool):
    """
    Add room tone to the beginning and end of a given audio clip, and optionally add silence after it.

    :param clip_path: The path to the audio clip.
    :param silence_needed: Whether to add silence after the clip (for clips followed by another utterance).
    """
    # Import the audio clip (utterance)
    pa.import_audio(clip_path)

    # Import room tone and paste it at the start
    pa.import_audio(room_tone_path)
    pa.select_all()  # Select the entire room tone track
    pa.copy()  # Copy room tone

    # Paste the room tone at the start of the clip
    pa.paste()  # Paste the room tone at the beginning of the utterance

    # Paste room tone again at the end
    pa.import_audio(room_tone_path)  # Import again to paste at the end
    pa.select_all()
    pa.copy()
    pa.paste()  # Paste the room tone at the end of the utterance

    # Optionally, add 6 seconds of silence if another clip follows
    if silence_needed:
        pa.import_audio(silence_path)
        pa.select_all()  # Select the entire silence track
        pa.copy()  # Copy silence
        pa.paste()  # Paste 6 seconds of silence after the clip


def process_script_clips(script_folder: str, script_name: str, first_name: str, last_name: str):
    """
    Process all clips within a script by adding room tone and silence, then export them as a single file.

    :param script_folder: The folder where the individual utterance files are stored.
    :param script_name: The name of the script to use for the final export.
    :param first_name: First name for file naming.
    :param last_name: Last name for file naming.
    """
    # Collect all utterance clip files
    clip_files = sorted([f for f in os.listdir(script_folder) if f.endswith(".wav")])

    # Process each utterance clip
    for idx, clip_file in enumerate(clip_files):
        clip_path = os.path.join(script_folder, clip_file)

        # Add room tone to this clip and optionally add silence if not the last clip
        silence_needed = (idx < len(clip_files) - 1)
        add_room_tone_and_silence(clip_path, silence_needed)

    # After processing all clips, join and export (export step needs manual confirmation)
    export_filename = f"{script_name}_{first_name}_{last_name}.wav"
    export_path = os.path.join(r"F:\Path\To\Export\Directory", export_filename)  # Update to your export directory

    # Notify to manually export (since export_selected_audio is not available)
    print(f"Processed clips. Please manually export: {export_filename}")


def process_all_scripts(parent_directory: str, first_name: str, last_name: str):
    """
    Process all scripts in the parent directory, combining clips and adding room tone and silence.

    :param parent_directory: The root directory containing the folders for each script.
    :param first_name: First name for file naming.
    :param last_name: Last name for file naming.
    """
    # Traverse through each folder (representing a script) in the parent directory
    for folder in os.listdir(parent_directory):
        script_folder_path = os.path.join(parent_directory, folder)
        if os.path.isdir(script_folder_path):
            print(f"Processing script: {folder}")
            process_script_clips(script_folder_path, folder, first_name, last_name)


if __name__ == "__main__":
    # Path to the directory containing the script folders
    parent_dir = r"F:\Path\To\Your\AudioFiles"  # Update this to your actual directory containing script folders

    first_name = "Sabien"  # Update with your first name
    last_name = "Ruffin"  # Update with your last name

    # Process all scripts and export the results
    process_all_scripts(parent_dir, first_name, last_name)
