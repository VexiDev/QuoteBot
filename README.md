# QuoteBot
<a href="https://top.gg/bot/814379239930331157">
  <img src="https://top.gg/api/widget/814379239930331157.svg">
</a>

### This branch is outdated!
> For the most up to date code and to track the progress of QuoteBot v5 please switch to the v5 branch

## Info

> Use this bot to save quotes from your friends or any user in your server, using simple and straightforward commands.

> The bot stores all of your quotes into the cloud and you can see them at any time

> use q!help for a list of all available commands on quotebot

## Add the Bot

> If you don't want to figure out how to host QuoteBot yourself you can always use the version I host. 
This version will get updates sooner and more consistently then this github.
> if you are in a server that has QuoteBot already running you can use the button on QuoteBot's profile to get the link

  if not

> You can use this [link](https://discord.com/api/oauth2/authorize?client_id=814379239930331157&permissions=8&scope=bot)


## Self Hosting (OUTDATED, probably wont work)

If you want to host the bot yourself the bot was designed to run on heroku follow the steps below to set it up;

Clone the repository using 

> $ git clone https://github.com/VexiDev/QuoteBot.git

Create a heroku app at https://dashboard.heroku.com/deploy
Then follow the CLI instructions on your heroku app's deploy tab (https://dashboard.heroku.com/apps/{appname}/deploy/heroku-git)

Add a database to your heroku app ([add a database](https://elements.heroku.com/addons/heroku-postgresql)). Then navigate to 
> ~/cogs/setup.py

in your cloned repository and insert your credentials ([find your credentials here](https://data.heroku.com/))

Then run the following in your directory

> $ git add *

> $ git commit -am "all"

> $ git push heroku master

after that heroku will launch QuoteBot

If everything worked you should see this in your heroku console 
> Successfully connected to QuoteBot! 

You can see your app logs by running the following

> $ heroku logs -a {appname} -t

in your command prompt program

If it does not run, start the app manually on the heroku dashboard
