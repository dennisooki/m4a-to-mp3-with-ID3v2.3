import argparse
import os
from mutagen.mp4 import MP4
from mutagen import id3
from pydub import AudioSegment

def convert_m4a_to_mp3(input_file, output_file):
    """
    Converts an M4A file to an MP3 file with ID3v2.3 tags.
    """
    # Load the M4A file and extract the metadata
    m4a = MP4(input_file)

    title = m4a.get('\xa9nam', [""])[0]
    artist = m4a.get('\xa9ART', [""])[0]
    album = m4a.get('\xa9alb', [""])[0]
    genre = m4a.get('\xa9gen', [""])[0]
    track = m4a.get('\xa9trk', [0])[0][0] if m4a.get('\xa9trk') else 0
    year = m4a.get('\xa9day', [""])[0]
    comment = m4a.get('\xa9cmt', [""])[0]

    # Load the M4A audio and export it as an MP3 file
    audio = AudioSegment.from_file(input_file, format="m4a")
    audio.export(output_file, format="mp3")

    # Update the ID3v2.3 tags for the MP3 file
    id3_tags = id3.ID3(output_file)
    id3_tags["TIT2"] = id3.TIT2(encoding=3, text=title)
    id3_tags["TPE1"] = id3.TPE1(encoding=3, text=artist)
    id3_tags["TALB"] = id3.TALB(encoding=3, text=album)
    id3_tags["TCON"] = id3.TCON(encoding=3, text=genre)
    id3_tags["TRCK"] = id3.TRCK(encoding=3, text=str(track))
    id3_tags["TYER"] = id3.TYER(encoding=3, text=str(year))
    id3_tags["COMM"] = id3.COMM(encoding=3, lang='eng', text=comment)
    id3_tags.save(output_file)

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Convert M4A files to MP3 with ID3v2.3 tags")

    # Add the directory argument
    parser.add_argument("--directory", "-d", required=True, help="Directory containing M4A files")
    parser.add_argument("--output-dir", "-o", required=True, help="Output directory")

    # Parse the arguments
    args = parser.parse_args()

    # Get the directory and output directory from the command-line arguments
    directory = args.directory
    output_dir = args.output_dir

    # If the directory is ".", use the current working directory
    if directory == ".":
        directory = os.getcwd()

    # If the output directory is ".", use the current working directory
    if output_dir == ".":
        output_dir = os.getcwd()

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Iterate through the files in the directory
    for filename in os.listdir(directory):
        if filename.endswith(".m4a"):
            input_file = os.path.join(directory, filename)
            output_file = os.path.join(output_dir, os.path.splitext(filename)[0] + ".mp3")
            convert_m4a_to_mp3(input_file, output_file)
            print(f"Converted {filename} to {os.path.basename(output_file)}")

if __name__ == "__main__":
    main()