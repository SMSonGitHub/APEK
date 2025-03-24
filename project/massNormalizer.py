from time import sleep
import pyaudacity as pa

#sometimes normalization will not have the intended effect if you normalize all clips at once. normalizing individual clips sequentially can potentially provide better outcomes.
def mass_normalize(total_clips):
    """
    First normalizes each clip to a peak

    :param total_clips: The total number of clips to process.
    :param target_rms: The RMS level to normalize each clip to. Default is -20 dB.
    """
    for clip_number in range(total_clips):
        print(f"Processing clip {clip_number + 1}/{total_clips}")

        # Select the current clip (assuming the clip is already selected)
        pa.normalize(peak_level= -6, remove_dc_offset=True)
        pa.sel_next_clip()  # Ensure the current clip is fully selected



        print(f"Normalized clip {clip_number + 1} to {-3} dB.")
        sleep(0.25)

if __name__ == "__main__":
        # Define the total number of clips you want to process
        total_clips = 877  # Adjust based on your actual number of clips

        # Normalize each clip to the specified RMS level (-20 dB)
        mass_normalize(total_clips)
