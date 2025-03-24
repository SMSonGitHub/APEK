

import pyaudacity as pa
import os


# Path to the pre-recorded room tone file
room_tone_path = r"your_directory"  # Update this to the path that contains the file you wish to append to the FRONT of your existing audio.

def add_room_tone_to_clip(clip_path: str):
    """
    Add room tone to the beginning and end of a given audio clip and overwrite the original file.

    :param clip_path: The path to the audio clip.
    """


    pa.import_audio(clip_path) # Import the audio clip (the line from the script)
    pa.import_audio(room_tone_path) # import the room tone

    # select the room tone

    #copy
    pa.copy()

    #select the
    pa.shift_down()
    pa.curs_track_start()
    pa.paste()
    pa.curs_track_end()
    pa.paste()
    pa.shift_down()
    pa.remove_tracks()
    pa.select_all()
    pa.join()
    pa.next_track()
    pa.delete()

    clip_no_ext = clip_path.split('.')[0]
    # Export the modified clip, overwriting the original file
    # pa.export(clip_no_ext + 'exported.wav')
    pa.export(clip_path)
    # Close the project in Audacity to prepare for the next file
    pa.close()

def process_all_wav_files(parent_directory: str):
    """
    Process all .wav files in the given directory and its subdirectories.
    Append room tone to the beginning and end of each clip, and overwrite the original file.

    :param parent_directory: The root directory containing the folders with audio clips.
    """
    # Traverse through the parent directory and its subfolders
    for root, dirs, files in os.walk(parent_directory):
        for file_name in files:
            if file_name.endswith(".wav"):  # Only process .wav files
                clip_path = os.path.join(root, file_name)  # Full path to the audio file
                # create lof file by appending the clips we want to open to the file.
                print(f"Processing {clip_path}...")

                # Add room tone and overwrite the original file
                add_room_tone_to_clip(clip_path)

                print(f"Room tone added and file saved: {clip_path}")

if __name__ == "__main__":
    # Path to the directory containing the folders with the .wav files
    parent_directory = rf"your_directory"  # Update this to path that contains the files you want the audio appended to. Be careful to not confuse this path with the above path.

    # Process all .wav files in the directory and subdirectories
    process_all_wav_files(parent_directory)