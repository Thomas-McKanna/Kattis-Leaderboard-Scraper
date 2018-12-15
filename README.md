# Kattis Leaderboard Scraper

Gathers select users scores from Kattis and presents them in an HTML table. It also keeps track of previous scores so you can see who is passing who up.

## Requirements

You will likely need to install some python packages to get the script running (you can see requirments.txt for a list). The commands you need to copy and paste in the terminal are as follows:

```
python3 -m pip install lxml
python3 -m pip install yattag
```

## How to Use:

Open up the names.txt file and fill with a comma separated list of Kattis usernames. You can find a person's kattis username by going to their kattis page (you may need to ask them their username if they are not on the top 50 board for MST).

Kattis user pages have the following form: `https://open.kattis.com/users/<username>`

Then just run the script with

```
python3 scraper.py
```
  
## Meaning of Status Symbols:

The first time you run the script, it will generate a history file so that it can compare the scores next time you run the script.

Subsequent runs with display an icon indicating how the users score has changed.

* Green up arrow means passed someone up
* Red down arrow means been passed up
* Flame means more than 10 points have been earned since last run
* Green dot means score has increase, but position remains unchanged
* Yellow dot means score has stayed the same and position remains unchanged



