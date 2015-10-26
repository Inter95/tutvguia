Introduction
===================
This is script allows to create personalized list of movies or TV Shows to be integrated in the local library and to be played for [Pulsar](https://github.com/steeve/plugin.video.pulsar).

The advantage is that you have all the tools from local library as trailer, cinema experience, etc.

The script makes a database, then you can run the script periodic and it will add only the new entries.  If you erase the file from the local library, it won't add it again.

You can erase the database any moment from the script plugin.  

It is possible to write the list manually or create them from internet.

Subscribing TV shows
===================
listing = ['Game of thrones', 'The Simpsons']  `example from list tv shows`

ID = [] `empty for tv shows`

**subscription.integration(**listing, ID,'SHOW', path to save**)**

Subscribing Movies without IMDB_ID
===================================
listing = ['Frozen (2013)', 'Guardians of the Galaxy (2014)'] `example from list movies, it is better to have the year`

ID = [] `IMDB_ID, if it is empty the function will figure it out`

**subscription.integration(**listing, ID,'MOVIE', path to save**)**

Subscribing Movies with IMDB_ID
===============================
listing = ['Edge of tomorrow', 'Gone girl']  `example from list movies, the year isn't necessary`

ID = ['tt1631867', 'tt2267998'] `IMDB_ID, if it is empty the function will figure it out`

**subscription.integration(**listing, ID,'MOVIE', path to save**)**


Settings class
===============
It gets information from addon configuration

settings = subscription.Settings() # create the setting object

settings.movie_folder = path to save the movies
settings.show_folder = path to save the tv shows


Browser to create the list from internet
============================================
**browser = subscription.Browser()**  ` define the browser to open URL`
* browser.open(url)
* url to open
* return true if it is 200 status
* browser.status : status and error
* browser.content : content html

**browser.login(**url, payload, verification expression**)** `open a page and do the login, return true if can login`

* url login page
* payload dictionary {'username': username, 'pass', password, ..} all the variable from the FORM
* verification expression, string to check it couldn't login, like incorrect username and password.
