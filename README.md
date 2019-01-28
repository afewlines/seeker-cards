# seeker-cards
ever want to play cards against humanity? great. play this instead. need playtesters.

this is a framework for a web-based cards against humanity client.

loads cards in from a .csv in the highest directory, currently named 'cards_master.csv' until i implement functionality to select file. format is as such:

| type | text | play |
| ------------- |:-------------| -----:|
| prompt | I wish the dev had kept `____` in the final release | 1 |
| prompt | This app is what happens when you combine `____` and `____` . | 2
| response | Good gameplay. | __ __ |

in the final csv, first row should be first card(not header row).

## the webserver
change the ip in `main.py` to whatever ip will be hosting it (if you don't quite know, use the ip of the machine that's running it).

users connect at `http://[ip]:8080`.

## the users
usernames aren't scrubbed, aren't checked for duplicates (yet).
