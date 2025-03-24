from time import sleep


import pyaudacity as pa

#sometimes normalizing the root-mean-square (rms) will not have the intended effect if you normalize all clips at once. Normalizing individual clips sequentially can potentially provide better outcomes.
def mass_normalize(total_clips):
    """
    First normalizes each clip to a peak

    :param total_clips: The total number of clips to process.
    :param target_rms: The RMS level to normalize each clip to. Default is -20 dB.
    """
    for clip_number in range(total_clips):
        print(f"Processing clip {clip_number + 1}/{total_clips}")

        # Select the current clip (assuming the clip is already selected)
        pa.loudness_normalization(stereo_independent= False, RMS_level= -20, dual_mono= False)
        pa.sel_next_clip()  # Ensure the current clip is fully selected



        print(f"RMS Normalized clip {clip_number + 1} to {-20} dB.")
        sleep(0.5)

if __name__ == "__main__":
        # Define the total number of clips you want to process
        total_clips = 552  # Adjust based on your actual number of clips

        # Normalize each clip to the specified RMS level (-20 dB)
        mass_normalize(total_clips)