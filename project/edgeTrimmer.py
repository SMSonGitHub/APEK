import pyautogui
import pyaudacity as pa
import time

# the purpose of this function is to remove a fixed amount of audio from each clip. your shortcut may be different so please be careful.
def apply_macro_to_clips(total_clips):
    """
    Applies the macro using 'Alt + A' to all clips in the selected track.

    :param total_clips: The total number of clips to process.
    """
    for clip_number in range(total_clips):
        # Simulate pressing 'Alt + A' to trigger the macro
        print(f"Processing clip {clip_number + 1}/{total_clips}")
        pyautogui.hotkey('alt', 'a')  # Simulates pressing Alt + A

        # Optional delay to ensure Audacity has time to process the command
        time.sleep(0.5)  # Adjust as necessary based on the macro's execution time

        # Move to the next clip
        pa.sel_next_clip()


if __name__ == "__main__":
    # Define the total number of clips you want to process
    total_clips = 552  # Adjust this based on your actual number of clips

    # Apply the macro to each clip
    apply_macro_to_clips(total_clips)
