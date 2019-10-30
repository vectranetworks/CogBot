### Install notes

When using the SLACK backend with cogbot you will need to configure one or more BOT_ADMINS.  To determine this value connect  
cogbot and the slack client to the slack backend and then issue a   

!whoami  command at cogbot.  The response will be something like  

cogbotAPP 12:47 PM  
┏━━━━━━━━━━┳━━━━━━━━━━━━━━━┓  
┃ key      ┃ value         ┃  
┡━━━━━━━━━━╇━━━━━━━━━━━━━━━┩  
│ person   │ `@Craig Simon`│  
├──────────┼───────────────┤  
│ nick     │ `craig`       │  
├──────────┼───────────────┤  
│ fullname │ `Craig Simon` │  
├──────────┼───────────────┤  
│ client   │ `DP79DALJ0`   │  
└──────────┴───────────────┘  
• string representation is '@Craig Simon'  
• class is 'SlackPerson'  

To set the BOT_ADMINS use the nick value and prefix it with the @ sign.  Therefor the command for the above would be  
BOT_ADMINS = ('@craig')  
It should be in the format @NICK  

To invite cogbot to a channel issue '/invite @cogbot' command in chat.
When the bot is not in a channel you can communicate with it by clicking on it's channel and issuing commands.

To remove cogbot left click on the bot itself and select remove.
When cogbot is in a channel you can issue ! commands in the channel and the bot will pick them up.