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

def append_to_excel(song_name, artist_name, album_name, listen_duration, excel_file_path):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date, time = timestamp.split(' ')
    
    data = {
        "Date": [date],
        "Time": [time],
        "Title": [song_name],
        "Artist": [artist_name],
        "Album": [album_name],
        "Listen Duration (seconds)": [listen_duration]
    }
    
    new_entry_df = pd.DataFrame(data)
    
    try:
        existing_df = pd.read_excel(excel_file_path)
        updated_df = pd.concat([existing_df, new_entry_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_entry_df

    updated_df.to_excel(excel_file_path, index=False)
    print(f"Logged: {timestamp} - {song_name} by {artist_name} - {album_name} (Listened for {listen_duration} seconds)")

def main():
    last_logged_song = None
    listen_duration = 0
    tick_speed = 5 # How fast the program will update 
    excel_file_path = input("Name of excel file (no need for .xlsx): ") + ".xlsx"
    
    while True:
        song_name, artist_name, album_name = get_current_track()
        if song_name and artist_name:
            album_name = album_name if album_name else ""
            current_song = (song_name, artist_name, album_name)
            if current_song == last_logged_song:
                listen_duration += tick_speed
            else:
                if last_logged_song is not None:
                    append_to_excel(last_logged_song[0], last_logged_song[1], last_logged_song[2], listen_duration, excel_file_path)
                listen_duration = tick_speed
                last_logged_song = current_song
        else:
            if last_logged_song is not None:
                append_to_excel(last_logged_song[0], last_logged_song[1], last_logged_song[2], listen_duration, excel_file_path)
                last_logged_song = None
                listen_duration = 0
        
        time.sleep(tick_speed)

main()
