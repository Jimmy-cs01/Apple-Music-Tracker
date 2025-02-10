# Apple-Music-Tracker
Apple music tracker that logs data into excel spreadsheet 
----------------------------------------------------------------------------
NOTE : This program contains a 'while True' loop and will run indefinitely 
       press CTRL + C to 'KeyboardInterrupt'
----------------------------------------------------------------------------

```
pip install -r requirements.txt
```
```
python3 music.py
```
Code view test 
```python
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
```
