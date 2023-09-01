## Spidermun
Spidermun is a simple discord bot that makes managing large discord servers a lot easier. <a href="https://discord.com/oauth2/authorize?client_id=1144931541298970654&permissions=8&scope=bot">Here</a> is the invite link :)

## Warning!
The bot was created for a certain discord server. If you plan to use it on your own, you might want to take a look at the code and change some stuff. 

## Features

#### commands:
- **/ping** - Lets the user test if the bot is responding.
- **/push** - Creates and updates categories (creates new channels if needed) - categories can be set using the `/set_klasy` command.
- **/push_newyear** - Automatically renames categories to match the new school year (2D --> 3D, etc.).
- **/stash** - Deletes and updates categories (deletes old channels if needed) - categories that shouldn't ever be deleted can be set using the `/set_permanent_categories` command.
- **/set_klasy** - Sets the categories that the bot creates or modifies when using `/push`.
- **/show_klasy** - Shows the current list of categories.
- **/set_permanent_categories** - Sets the categories that will never be affected by `/stash`.
- **/show_permanent_categories** - Shows the categories that will never be affected by `/stash`.
- **/set_trusted_ids** - Sets the IDs that can run commands which affect channels and categories.
- **/show_trusted_ids** - Shows the IDs that can run commands which affect channels and categories.

#### other stuff:
After user anwsers the pre-join questions, the bot automatically greets him and gives him access to certain categories.

## Details
#### detailed info on some commands:
- **/push** - The `/push` command grabs the list from `/show_klasy` and creates `-text` and `-audio` categories for each string in it. For example: If `/show_klasy` returns ['some_category', 'some_other_category'], running `/push` will create `some_category-text`, `some_category-audio`, `some_other_category-text`, and `some_other_category-audio` categories. This command is useful for efficiently creating and managing large numbers of categories. You can also create a category called `0-text` and `0-audio`, then add channels to them, and let the bot handle the rest of the job for other categories. For example: `0-text`: #some-text, #some-other-text; `0-audio`: #some-audio, #some-other-audio, `/show_klasy`: ['some_category', 'some_other_category'] - after running `/push`: some_category-text: #some-text, #some-other-text; some_category-audio: #some-audio, #some-other-audio; some_other_category-text: #some-text, #some-other-text; some_other_category-audio: #some-audio, #some-other-audio;.

- **/stash** - The `/stash` command removes old categories and channels. After running the command, the bot checks every category. If a category is not listed in `/show_permanent_categories` or `/show_klasy`, it gets deleted. If a category is not deleted, the bot checks if the channels inside it are also present in `#0-text` or `#0-audio`. Any channel inside of the current category but not in the 0's get deleted. This command simplifies the process of removing old channels created by `/push`.

## Contributing
I honestly doubt that anyone would ever want to contribute to a project that some random guy wrote in a day (honestly, this is probably the worst public repo on this profile), but if you would like to do so, you can view the list of stuff to-do below :)

## TO-DO list:
1. create the /amend command (the amend command will change the names of channels inside of categories based on the name inside of the 0's)
2. implement the /push_newyear command (this command is explained in the commands section)