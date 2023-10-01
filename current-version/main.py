from spotiplex import (
connect_plex,
connect_spotify, 
getlidarrlists, 
# extract_playlist_id, 
# get_playlist_name,
# get_spotify_playlist_tracks,
# create_list,
# check_tracks_in_plex,
process_playlist
)


import concurrent.futures

from concurrent.futures import ThreadPoolExecutor
from decouple import config

# def main():
    
#     # Assuming you have this in your environment variables or settings
#     plex = connect_plex()
#     sp = connect_spotify()

#     try:
#         lidarr_playlists = getlidarrlists()

#         for playlist in lidarr_playlists:
#             try:
#                 playlist_id = extract_playlist_id(playlist)
#                 spotify_tracks = get_spotify_playlist_tracks(sp, playlist_id)
#                 plex_tracks, _ = check_tracks_in_plex(plex, spotify_tracks)
#                 playlist_name = get_playlist_name(sp, playlist_id)

#                 create_list(plex, plex_tracks, playlist_name)

#                 print(f"Processed playlist '{playlist_name}'.")

#             except Exception as e:
#                 print(f"An error occurred processing playlist {playlist}:", e)
#                 continue  # continue will ensure that the loop proceeds to the next playlist even if an error occurs
#     except Exception as playlistfailed:
#         print("Grabbing all playlists failed")
#         print(playlistfailed)

def main():
    plex = connect_plex()
    sp = connect_spotify()

    lidarr_playlists = getlidarrlists()
    workercount = int(config("WORKERS"))
    # Use ThreadPoolExecutor to process multiple playlists simultaneously
    with ThreadPoolExecutor(max_workers=workercount) as executor:
        # Use 'executor.submit' to start the function in a new thread
        futures = [executor.submit(process_playlist, playlist, plex, sp) for playlist in lidarr_playlists]
        
        # Wait for all tasks to complete. If you want to handle exceptions or 
        # gather results returned by the tasks, you can do that here.
        for future in concurrent.futures.as_completed(futures):
            try:
                # This will raise an exception if the function erred
                future.result()
            except Exception as e:
                print(f"Thread resulted in an error: {e}")




if __name__ == "__main__":
    main()