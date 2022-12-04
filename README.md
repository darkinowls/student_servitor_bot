# Student servitor bot - Abobus

###### My diploma work

The Telegram bot, which is created to support students.
It consists of 4 modules:

1. Queue module 
2. Gmail module
3. Schedule module
4. Basic module

It uses MongoDB Atlas as a database to remember all the sessions.
There are 2 collections of sessions: 
gmail_sessions and schedule_sessions

---

## ALL the bot commands

() - element is optional

[] - element is required

*a cursive command* - the command requires the reply to a queue 

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /queue (header)           | Creates a queue with a header                                                          |                               
| */swap [index] [index]*   | Swaps records in the queue by unique indexes. One of indexes should exist in the queue |
| */rm [index list]*        | Deletes records in the queue by indexes.                                               |
| */header [name]*          | Sets a header to the queue                                                             |
| *[record]*                | Creates record in the queue                                                            |
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail                               |                                
| /off_gmail                | Stops the gmail module for this group                                                  |                               
| /on_gmail                 | Resumes the gmail module for this group                                                |                               
| /my_gmail                 | Sends the gmail address a user has set                                                 |                               
| /schedule [file.json]     | Takes a file.json and it sets the schedule for the group                               |            
| /on_schedule              | Resumes the schedule module for this group                                             |                               
| /off_schedule             | Stops the schedule module for this group                                               |
| /my_schedule              | Returns the json file a user has set. If he hasn't the example json is sent            |
| /hi                       | Replies "hello". It is made if the bot works                                           |
| /json                     | Sends the json file of the message                                                     |
| /week                     | Reports the current week number                                                        |

---


### Queue module

() - element is optional

[] - element is required

*a cursive command* - the command requires the reply to a queue 

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /queue (header)           | Creates a queue with a header                                                          |                               
| */swap [index] [index]*   | Swaps records in the queue by unique indexes. One of indexes should exist in the queue |
| */rm [index list]*        | Deletes records in the queue by indexes.                                               |
| */header [name]*          | Sets a header to the queue                                                             |
| *[record]*                | Creates record in the queue                                                            |

The module allows students to self organize in their telegram groups.
Students can create a queue and manage queues. Each queue consists of records.
The record is an entity with a number(index) and the name of a student.

> A name should contain less than 100 characters.

> A number(index) is a natural number (1,2,3,4 ... 123, 124 ...)

> Queues are sorted by ascending numbers.

It's possible to:
* create a record by the /queue (header);
* replace records by the */swap [index] [index]* command;
* delete records by */rm [index list]*; 
* set a header for a queue - */header [name]*;
* add a record *[record]*;

There are 2 ways to add a record:

1. Add the last element - requires only name. An example: Denis Jibrony 
2. Add the record by its index - requires empty space. Examples: 22 Antony Blinken 


### Gmail module

[] - element is required

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail                               |                                
| /off_gmail                | Stops the gmail module for this group                                                  |                               
| /on_gmail                 | Resumes the gmail module for this group                                                |                               
| /my_gmail                 | Sends the gmail address a user has set                                                 |  

The module allows students to bind a gmail account to a group.
Thereby, every new gmail messages will be sent to the group.

### Schedule module

[] - element is required

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /schedule [file.json]     | Takes a file.json and it sets the schedule for the group                               |            
| /on_schedule              | Resumes the schedule module for this group                                             |                               
| /off_schedule             | Stops the schedule module for this group                                               |
| /my_schedule              | Returns the json file a user has set. If he hasn't the example json is sent            |

The module allows students to bind a lesson schedule to a group.
Thereby, the messages about lessons will be sent to the group.

### Basic module

The module allows students to use simple commands 
to make the bot say "hello", to send json of message and
say the current week number 