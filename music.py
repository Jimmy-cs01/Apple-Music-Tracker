import datetime
import time
import subprocess
import pandas as pd

def get_current_track():
    script = '''
    tell application "Music"
        if it is running then
            if player state is playing then
                set trackName to name of current track
                set artistName to artist of current track
                try
                    set albumName to album of current track
                on error
                    set albumName to "" 
                end try
                return trackName & " - " & artistName & " - " & albumName
            end if
        end if
    end tell
    '''
    try:
        result = subprocess.run(['osascript', '-e', script], text=True, capture_output=True, check=True)
        output = result.stdout.strip()
        if output:
            return output.split(" - ", 2)
    except subprocess.CalledProcessError:
        return None, None, None
    return None, None, None

def append_to_excel(song_name, artist_name, album_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date, time = timestamp.split(' ')
    
    data = {
        "Date": [date],
        "Time": [time],
        "Title": [song_name],
        "Artist": [artist_name],
        "Album": [album_name]
    }
    
    new_entry_df = pd.DataFrame(data)
    excel_file_path = 'song_log.xlsx'
    
    try:
        existing_df = pd.read_excel(excel_file_path)
        updated_df = pd.concat([existing_df, new_entry_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_entry_df

    updated_df.to_excel(excel_file_path, index=False)
    print(f"Logged: {timestamp} - {song_name} by {artist_name} - {album_name}")

def main():
    last_logged_song = None
    
    while True:
        song_name, artist_name, album_name = get_current_track()
        if song_name and artist_name:
            album_name = album_name if album_name else ""
            current_song = (song_name, artist_name, album_name)
            if current_song != last_logged_song:
                append_to_excel(song_name, artist_name, album_name)
                last_logged_song = current_song
        time.sleep(10)

main()