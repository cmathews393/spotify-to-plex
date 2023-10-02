from spotiplex import (
    connect_plex,
    connect_spotify,
    getlidarrlists,
    # extract_playlist_id,
    # get_playlist_name,
    # get_spotify_playlist_tracks,
    # create_list,
    # check_tracks_in_plex,
    process_playlist,
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


def process_for_user(user, plex, sp, lidarr_playlists, workercount):
    if user:
        # Switch to the alternate user context
        plex = plex.switchUser(user)
        print(f"Processing playlists for user: {user}")

    # Use ThreadPoolExecutor to process multiple playlists simultaneously
    with ThreadPoolExecutor(max_workers=workercount) as executor:
        # Use 'executor.submit' to start the function in a new thread
        futures = [
            executor.submit(process_playlist, playlist, plex, sp)
            for playlist in lidarr_playlists
        ]

        # Wait for all tasks to complete. If you want to handle exceptions or
        # gather results returned by the tasks, you can do that here.
        for future in concurrent.futures.as_completed(futures):
            try:
                # This will raise an exception if the function erred
                future.result()
            except Exception as e:
                print(f"Thread resulted in an error: {e}")


def connection_handler():
    print("Initiating Plex connection...")
    try:
        plex = connect_plex()
        print("Plex connection succeeded")
    except Exception as plexfailed:
        print("Plex connection failed")
        print(plexfailed)
        print("Exiting")
        exit()
    print("Initiating Spotify Connection")
    try:
        sp = connect_spotify()
        print("Spotify connection succeeded")
    except Exception as spotifailed:
        print("Spotify connection failed")
        print(spotifailed)
        print("Exiting...")
        input()
        exit()
    print("Getting synced Lidarr playlists...")
    try:
        lidarr_playlists = getlidarrlists()
        print("Playlists grabbed")
        lidarrworking = True
        return (plex, sp, lidarr_playlists, lidarrworking)
    except Exception as lidarrfailed:
        print("Lidarr playlist import failed")
        print(lidarrfailed)
        print(
            "Lidarr import failed. Press ENTER to use a manual playlist ID (not implemented yet)"
        )
        playlistid = input("Enter playlistID: ")
        if len(playlistid) <= 1:
            print("No playlist provided, exiting...")
            input()
            exit()
        else:
            lidarrworking = False
            return (plex, sp, playlistid, lidarrworking)


def main():
    plex, sp, lidarr_playlists, lidarrworking = connection_handler()

    workercount = int(config("WORKERS"))

    # Convert comma-separated users string to list of users
    userlist = config("USERS").split(",") if config("USERS") else []

    # Process for the main user first

    process_for_user(None, plex, sp, lidarr_playlists, workercount)

    # Then process for each user in the user list
    for user in userlist:
        process_for_user(user.strip(), plex, sp, lidarr_playlists, workercount)


if __name__ == "__main__":
    main()