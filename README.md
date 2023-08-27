## Spidermun
Spidermun is a simple discord bot that makes managing large discord servers a lot easier. <a href="https://discord.com/oauth2/authorize?client_id=1144931541298970654&permissions=8&scope=bot">Here</a> is the invite link :)

## Warning!
The bot was created for a certain discord server. If you plan to use it on your own, you might want to take a look at the code and change some stuff. 

## Features

#### commands:
<ul>
    <li><strong>/ping</strong> - lets user test if the bot is responding</li>
    <li><strong>/push</strong> - creates and updates categories (creates new channels if needed) - categories can be set using /set_klasy command</li>
    <li><strong>/push_newyear</strong> - automatically renames categories to match the new school year (2D --> 3D, etc.)</li>
    <li><strong>/stash</strong> - deletes and updates categories (deletes old channels if needed) - categories that shouldn't ever be deleted can be set using the /set_pernament_categories command</li>
    <li><strong>/set_klasy</strong> - sets the categories that the bot creates/modifies when using /push</li>
    <li><strong>/show_klasy</strong> - shows the current list of categories</li>
    <li><strong>/set_permanent_categories</strong> - sets the categories that will never be affected by /stash</li>
    <li><strong>/show_permanent_categories</strong> - shows the categories that will never be affected by /stash</li>
    <li><strong>/set_trusted_ids</strong> - sets the ids that can run commands which affect channels and categories</li>
    <li><strong>/show_trusted_ids</strong> - shows the ids that can run commands which affect channels and categories</li>
</ul>

#### other stuff:
After user anwsers the pre-join questions, the bot automatically greets him and gives him access to certain categories.

## Details
#### detailed info on some commands:
<ul>
    <li> 
        <strong>/push</strong> command grabs the channels from /show_klasy and creates -text, -audio for them. Example: /show_klasy - ['some_category', 'some_other_category'], /push -creates some_category-text, some_category-audio, some_other_category-text and some_other_category-audio. Other than helping with creating large amounts of categories it also helps with managing them. If you create a category called 0-text and 0-audio, you will be able to just add the channels there and let the bot do all of the work for you in other categories. Example: 0-text: #some-text, #some-other-text. 0-audio: #some-audio, #some-other-audio - after running the /push command the bot will go through every category inside of the /show_klasy and add the channels to them.
    </li>
    <li> 
        <strong>/stash</strong> command gets rid of the old categories and channels. After running the command, the bot loops through every category and checks if it is either in /show_permanent_categories or in /show_klasy, if it is in none, then it deletes the category - if the category doesn't get deleted, the bot checks if the channels inside of it are also inside of #0-text / #0-audio. If any channel is inside of the current category but isn't inside of the 0's - it gets deleted. This command makes it really easy to get rid of old channels created by /push
    </li>
</ul>

## Contributing
I honestly doubt that anyone would ever want to contribute to a project that some random guy wrote in a day (honestly, this is probably the worst public repo on this profile), but if you would like to do so, you can view the list of stuff to-do below :)

## TO-DO list:
1. create a waiting animation (waiting for the bot to finish creating / deleting stuff can be annoying, i was thinking sending "-" and then later editing it using this list every second: ["\", "|", "/", "-"]. I think that it would be a lot cooler than just sending the "doing stuff.." message)
2. create the /amend command (the amend command will change the names of channels inside of categories based on the name inside of the 0's)
3. implement the /push_newyear command (this command is explained in the commands section)