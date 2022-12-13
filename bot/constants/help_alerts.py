HELP_TITLE = "H"

SWAP_HELP = HELP_TITLE + "/swap 1 2\n" \
                         "Swaps the replied queue records by indexes"

RM_HELP = HELP_TITLE + "/rm 1 2\n" \
                       "Deletes the replied queue records by indexes"

HEADER_HELP = HELP_TITLE + "/header Lab 5 Math\n" \
                           "Sets the replied queue header"

ADD_HELP = HELP_TITLE + "1 Arthur Jotaro\n" \
                        "Creates the replied queue record"

HELP = \
    """
<pre>Commands:
    
/queue - Creates a queue

/gmail [gmail] [app-pass] - Creates gmail connection between the group and the gmail                           

/gmail - Sends the gmail address a user has set

/schedule [file.json] - Takes a file.json and it sets the schedule for the group

/schedule - Returns the json file a user has set. If he hasn't the example json is sent            

/hi - Replies hello

/json - Sends the message json file

/week - Reports the current week number

/help - Sends the message with commands
</pre>
    """
