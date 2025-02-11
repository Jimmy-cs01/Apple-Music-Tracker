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
    if listen_duration < 15:
        return

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date, time_part = timestamp.split(' ')
    
    minutes = listen_duration // 60
    seconds = listen_duration % 60
    
    data = {
        "Date": [date],
        "Time": [time_part],
        "Title": [song_name],
        "Artist": [artist_name],
        "Album": [album_name],
        "Minutes": [minutes],
        "Seconds": [seconds],
    }
    
    new_entry_df = pd.DataFrame(data)
    
    try:
        existing_df = pd.read_excel(excel_file_path)
        updated_df = pd.concat([existing_df, new_entry_df], ignore_index=True)
    except FileNotFoundError:
        updated_df = new_entry_df

    updated_df.to_excel(excel_file_path, index=False)
    print(f"Logged: {timestamp} - {song_name} by {artist_name} - {album_name} (Listened for {minutes} min {seconds} sec)")
    
def main():
    last_logged_song = None
    start_time = None
    excel_file_path = input("Name of excel file (no need for .xlsx): ") + ".xlsx"

    while True:
        song_name, artist_name, album_name = get_current_track()
        if song_name and artist_name:
            album_name = album_name if album_name else ""
            current_song = (song_name, artist_name, album_name)
            
            if current_song == last_logged_song:
                pass  # Still playing the same song
            else:
                if last_logged_song is not None and start_time is not None:
                    listen_duration = round(time.time() - start_time)  # Calculate precise duration
                    append_to_excel(last_logged_song[0], last_logged_song[1], last_logged_song[2], listen_duration, excel_file_path)
                
                start_time = time.time()  # Reset start time for new song
                last_logged_song = current_song
        
        else:
            if last_logged_song is not None and start_time is not None:
                listen_duration = round(time.time() - start_time)
                append_to_excel(last_logged_song[0], last_logged_song[1], last_logged_song[2], listen_duration, excel_file_path)
                last_logged_song = None
                start_time = None
        
        time.sleep(1)  # Keep checking every second
        
main()