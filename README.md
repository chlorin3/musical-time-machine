# musical-time-machine
Scrape the top 100 song titles from Billboard 100 and create a spotify playlist with those songs

1. It asks you what year you would like to travel to in YYY-MM-DD format.
2. Using BeautifulSoup, it scrapes the top 100 song titles on that date into a Python List.
3. Then a list of Spotify song URIs is created based on the list of song names.
When a song is not available in Spotify, it is skipped over.
4. A new private playlist is created with the name "YYYY-MM-DD Billboard 100", where the date is the date provided by the user in step 1.
5. Each song is added to this new playlist.
