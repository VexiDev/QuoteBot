# QuoteBot

## Info

> Use this bot to save quotes from your friends or any user, using simple and straightforward commands.
> The bot stores all of your quotes into the cloud and makes backup everday at midnight.


## Add the Bot

> If you don't want to figure out how to host QuoteBot yourself you can always use the version I host. This version will get updates sooner and more consistently then this github.
  
> if you are in a server that has QuoteBot already running you can use the q!invite command to get the link

  if not

> You can use this [link](https://discord.com/api/oauth2/authorize?client_id=814379239930331157&permissions=8&scope=bot)


## Self Hosting (WIP incomplete)

MAKE SURE YOU HAVE PYTHON 3.9+

If your planning on hosting on heroku you're in luck everything is basically setup for you;
Just clone the repository using 

> $ git clone

Then follow the CLI instructions on your heroku app's deploy tab

If your using a database from heroku, use PostgreSQL. Then navigate to ~/cogs/setup.py in your cloned repository and insert your credentials

Then run the following

> $ git commit -am "all"

> $ git push heroku master

after that heroku will launch QuoteBot


If your not using heroku and plan to local host then its almost as easy,

You'll want to clone the repository
> $ git clone

Navigate to the installed folder then run

> $ pip3 install -r requirements.txt

After that open the cogs folder. Find setup.py and enter your database credentials

Currently only supporting PostgreSQL, more soon.

Next open Main.py, at the bottom and add your bot token where it says TOKEN

(If you do not know what/where your bot token is then read this [guide](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/))

To start the bot in the orignial directory run 

> $ python Main.py



If everything worked you should see

> Successfully connected to QuoteBot! 


REMINDER SELF HOSTING IS NOT YET AVAILABLE

If you encounter any issues or bugs please dm me on discord vexi#0420 or join this server and make a ticket (link coming)

## Developed by vexi#0420
