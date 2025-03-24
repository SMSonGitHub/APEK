import pyaudacity as pa
import os
import re
from bs4 import BeautifulSoup

#if you have a .aup file that contains multiple individual clips, you can use this function to label each clip and export them with the desired name.
def get_file_names_in_directory(directory_path: str) -> list[str]:
    """
    Get the list of file names in the specified directory.

    :param directory_path: The path to the directory.
    :return: A list of file names.
    """
    file_names = []
    for file_name in os.listdir(directory_path):
        # Check if it's a file (not a directory)
        if os.path.isfile(os.path.join(directory_path, file_name)):
            file_names.append(file_name)
    return file_names

def extract_highlighted_text_from_file(file_path, column_index):
    with open(file_path, 'r', encoding='utf-8') as file_handle:
        soup = BeautifulSoup(file_handle, 'html.parser')
        highlighted_texts = []

        # Find all rows in the table
        table_rows = soup.find_all('tr')
        print(f"Processing file: {file_path} - Found {len(table_rows)} rows")

        for row in table_rows:
            cells = row.find_all('td')
            if len(cells) > column_index:  # Ensure the column exists in this row
                cell = cells[column_index]

                # First check for spans with background color for highlighting
                spans = cell.find_all('span', style=re.compile(r'background:\s*#ffff00'))
                for span in spans:
                    extracted_text = span.get_text().strip()
                    if extracted_text:
                        print(f"Found highlighted text in span: {extracted_text}")
                        highlighted_texts.append(extracted_text)

                # Then check for divs with class "highlight"
                divs = cell.find_all('div', class_="highlight")
                for div in divs:
                    extracted_text = div.get_text().strip()
                    if extracted_text:
                        print(f"Found highlighted text in div: {extracted_text}")
                        highlighted_texts.append(extracted_text)

            else:
                print(f"Row does not have enough columns: {row}")

    if not highlighted_texts:
        print(f"No highlighted texts extracted from {file_path}")

    return highlighted_texts

def do_things():
    #sorts the files by name in the directory so the labels are applied to the clips in the correct order.
    # Choose the correct directory to pull from
    directory_path = r"directory name"

    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

    file_names = sorted([file_name for file_name in os.listdir(directory_path)
                         if os.path.isfile(os.path.join(directory_path, file_name)) and file_name.endswith('.html')],
                        key=natural_sort_key)

    file_script_ids_dictionary = {}
    total_labels = 0  # Counter for total labels

    # Looping through filenames in the directory
    for name in file_names:
        try:
            full_path = rf"{directory_path}/{name}"  # Get the names of the files
            highlighted_text_list = extract_highlighted_text_from_file(full_path, 0)  # Pull highlighted text from the files
            file_script_ids_dictionary[name] = highlighted_text_list
            total_labels += len(highlighted_text_list)  # Update the total label count
        except Exception as e:
            print(f"Error processing file {name}: {str(e)}")

    # Process each script and label the clips
    for key_filename, utterances in file_script_ids_dictionary.items():
        print(f"Processing script: {key_filename}")

        script_id = os.path.splitext(key_filename)[0]  # Script ID without the file extension
        first_name = 'first_name'
        last_name = 'last_name'

        # Ensure the export directory exists for this script
        export_directory = os.path.join(directory_path, script_id)
        if not os.path.exists(export_directory):
            os.makedirs(export_directory)

        for utterance_id in utterances:
            print(f"Processing utteranceID: {utterance_id}")

            pa.last_track()
            pa.curs_track_start()
            pa.sel_next_clip()
            pa.cut()
            pa.toggle()
            pa.prev_track()
            pa.toggle()
            # paste cut data into temp
            pa.paste()
            pa.toggle()


            # Prepend and Append 1 second room tone to clip
            pa.first_track()
            pa.next_track()
            pa.curs_track_start()
            pa.sel_next_clip()
            pa.copy()
            pa.toggle()
            pa.next_track()
            pa.next_track()

            #pre-pend
            pa.curs_track_start()
            pa.paste()
            #append
            pa.curs_track_end()
            pa.paste()
            pa.toggle()


            # Append 6 seconds of silence to clip.
            pa.first_track()
            pa.curs_track_start()
            pa.sel_next_clip()
            pa.copy()
            pa.toggle()
            pa.last_track()
            pa.prev_track()
            # append
            pa.curs_track_end()
            pa.paste()

            # append temp to temp result
            pa.curs_track_end()
            pa.sel_track_start_to_cursor()
            pa.cut()
            pa.toggle()
            pa.prev_track()
            pa.curs_track_end()
            # paste temp at the end of temp_result
            pa.paste()
            pa.toggle()

        # join all the utterance_id labels into one clip
        pa.sel_track_start_to_cursor()
        pa.join()
        pa.sel_track_start_to_end()
        # cut temp result to clipboard
        pa.cut()
        pa.toggle()

        wav_file_name = f"{script_id}_{first_name}_{last_name}"
        export_clip_region_by_labels(export_directory, wav_file_name)
        #end files names

    print(f"Total labels created: {total_labels}")


def export_clip_region_by_labels(export_dir, label):
    # Export the labeled clip
    export_path = os.path.join(export_dir, f"{label}.wav")
    pa.export(export_path)
    print(f"Exported clip to: {export_path}")

def select_tracks(first_track=0, track_count=0, low=None, high=None):
    # type: (Optional[float], Optional[float]) -> str
    """TODO

    Audacity Documentation:
        Nullifies existing selection when called without arguments
        first_track = 0, data_track = 4
        track_count must = 1 if the function is to select anything.

        example usage for silence selection
            select_tracks(first_track=0, track_count=1)

        example usage for room_tone
            select_tracks(first_track=1, track_count=1)

    ."""

    if not isinstance(first_track, (type(None), float, int)):
        raise Exception('high argument must be float or int, not ' + str(type(high)))
    if not isinstance(track_count, (type(None), float, int)):
        raise Exception('low argument must be float or int, not ' + str(type(low)))

    # Only include arguments if they are not None. (If they are none, then the selection is "unchanged" according to the documentation.)
    macro_arguments = []
    if first_track is not None:
        macro_arguments.append('Track="{}"'.format(first_track))
    if track_count is not None:
        macro_arguments.append('TrackCount="{}"'.format(track_count))

    return pa.do('SelectTracks: ' + ' '.join(macro_arguments))





















if __name__ == "__main__":
    do_things()
