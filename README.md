# Student servitor bot - Abobus

###### My diploma work

The Telegram bot, which is created to support students.
It consists of 3 modules:

1. Queue module 
2. Gmail module
3. Schedule module

It uses MongoDB Atlas as a database to remember all the sessions.

---

## Bot commands

() - element is optional

[] - element is required

*a cursive command* - the command requires the reply to a queue 

| Command                   | What it does                                                                                     |
|---------------------------|--------------------------------------------------------------------------------------------------|
| /queue (header)           | Creates a queue with a header                                                                    |                               
| */swap [index] [index]*   | Swaps records in the queue by unique indexes. One of indexes should exist in the queue           |
| */rm [index list]*        | Deletes records in the queue by indexes.                                                         |
| */header [name]*          | Sets a header to the queue                                                                       |
| *[record]*                | Creates record in the queue                                                                      |
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail                                         |                               
| /schedule [file.json]     | Takes a file.json and it sets the schedule for the group                                         |                               
| /off_gmail                | Stops the gmail module for this group                                                            |                               
| /on_gmail                 | Resumes the gmail module for this group                                                          |                               
| /on_schedule              | Resumes the schedule module for this group                                                       |                               
| /off_schedule             | Stops the schedule module for this group                                                         |
---


### Queue module

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

The module allows students to bind a gmail account to a group.
Thereby, every new gmail messages will be sent to the group.

### Schedule module

The module allows students to bind a lesson schedule to a group.
Thereby, the messages about lessons will be sent to the group.