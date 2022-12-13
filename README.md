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

* () - element is optional
* [] - element is required
* *a cursive command* - the command requires the reply to a queue

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /queue (header)           | Creates a queue with a header                                                          |                               
| */swap [index] [index]*   | Swaps records in the queue by unique indexes. One of indexes should exist in the queue |
| */rm [index list]*        | Deletes records in the queue by indexes.                                               |
| */header [name]*          | Sets a header to the queue                                                             |
| *[record]*                | Creates record in the queue                                                            |
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail                               |                                
| /gmail                    | Sends the gmail address a user has set                                                 |                     
| /off_gmail                | Stops the gmail module for this group                                                  |                               
| /on_gmail                 | Resumes the gmail module for this group                                                |                               
| /schedule [file.json]     | Takes a file.json and it sets the schedule for the group                               |
| /schedule                 | Returns the json file a user has set. If he hasn't the example json is sent            |                  |            
| /on_schedule              | Resumes the schedule module for this group                                             |                               
| /off_schedule             | Stops the schedule module for this group                                               |
| /hi                       | Replies "hello". It is made if the bot works                                           |
| /json                     | Sends the json file of the message                                                     |
| /week                     | Reports the current week number                                                        |
| /help                     | Sends helpful message with all the commands                                            |
| /start                    | Sends helpful message with all the commands                                            |

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

> 256 is maximum number of records

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

---

### Gmail module

[] - element is required

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail                               |                                
| /gmail                    | Sends the gmail address a user has set                                                 |                     
| /off_gmail                | Stops the gmail module for this group                                                  |                               
| /on_gmail                 | Resumes the gmail module for this group                                                |                               

The module allows students to bind a gmail account to a group.
Thereby, every new gmail messages will be sent to the group.

---

### Schedule module

[] - element is required

| Command                   | What it does                                                                           |
|---------------------------|----------------------------------------------------------------------------------------|
| /schedule [file.json]     | Takes a file.json and it sets the schedule for the group                               |
| /schedule                 | Returns the json file a user has set. If he hasn't the example json is sent            |                  |            
| /on_schedule              | Resumes the schedule module for this group                                             |                               
| /off_schedule             | Stops the schedule module for this group                                               |

The module allows students to bind a lesson schedule to a group.
Thereby, the messages about lessons will be sent to the group.

#### Schedule fields:

* week: 1-2. There are odd days(1) and even ones(2). **Required**
* day: "Monday", "Thursday" ... "Sunday". Any day of the week. **Required**
* link: a link string of the meeting "https://...". **Optional**
* name: The subject name or anything else. **Required**
* time: 24-Hours time format: "00:00". **Required**

#### An example of json schedule:
```json
{
  "schedule": [
    {
      "link": "https://zoom.com/321",
      "day": "Monday",
      "time": "08:30",
      "week": 1,
      "name": "Math"
    },
    {
      "day": "Tuesday",
      "time": "12:30",
      "week": 1,
      "name": "Dancing"
    },
    {
      "link": "https://zoom.com/123",
      "day": "Wednesday",
      "time": "11:30",
      "week": 1,
      "name": "Economics"
    },
    {
      "link": "https://zoom.com/123",
      "day": "Thursday",
      "time": "09:30",
      "week": 2,
      "name": "IT bussiness"
    },
    {
      "day": "Friday",
      "time": "10:30",
      "week": 2,
      "name": "Data mining"
    },
    {
      "day": "Saturday",
      "time": "10:00",
      "week": 2,
      "name": "Dev ops"
    },
    {
      "link": "https://zoom.com/123",
      "day": "Sunday",
      "time": "14:30",
      "week": 2,
      "name": "Programming"
    }
  ]
}
```

---

### Basic module

| Command   | What it does                                   |
|-----------|------------------------------------------------|
| /hi       | Replies "hello". It is made if the bot works   |
| /json     | Sends the json file of the message             |
| /week     | Reports the current week number                |
| /help     | Sends helpful message with all the commands    |
| /start    | Sends helpful message with all the commands    |

The module allows students to use simple commands
to make the bot say "hello", to send json of message and
say the current week number