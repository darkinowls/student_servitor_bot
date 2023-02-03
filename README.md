# Student servitor bot

###### My diploma work

### Overview

The Telegram bot, which is created to support students.

Telegram bot consists of 4 modules. Each module has its own commands and features
You can click on one of the modules here to see the details:

1. [Queue module](#queue-module)
2. [Gmail module](#gmail-module)
3. [Schedule module](#schedule-module)
4. [Basic module](#basic-module)

It uses MongoDB Atlas as a database to remember all the sessions.
There are 2 collections of sessions:
gmail_sessions and schedule_sessions

---

### Navigation

1. [All the bot commands and their features](#all-the-bot-commands-and-their-features) (recommended for users)
    * [Queue module usage in details](#queue-module)
        * [Queue module commands](#queue-module-commands)
        * [What to do with Queue module](#what-to-do-with-queue-module)
    * [Gmail module in details](#gmail-module)
        * [Gmail module commands](#gmail-module-commands)
        * [Gmail module set up](#gmail-module-set-up)
    * [Schedule module in details](#schedule-module)
        * [Schedule module commands](#schedule-module-commands)
        * [Schedule field rules](#schedule-field-rules)
        * [An example of json schedule](#an-example-of-json-schedule)
        * [Schedule module set up with images](#schedule-module-set-up-with-images)
2. [How to install a bot on a server](#installation-on-a-server) (recommended for deployment engineer)
    1. [Get Telegram API keys](#telegram-api-keys)
    2. [Get MongoDB Atlas Database](#mongodb-atlas)
    3. [Student Servitor Bot set up](#student-servitor-bot-set-up)

---

## All the bot commands and their features

Let's look at *ALL* the commands in the table below.

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
| /start                    | The same as /help                                                                      |

---

### Queue module

The module allows students to self organize in their telegram groups.
Students can create a queue and manage queues. Each queue consists of records.
The record is an entity with a number(index) and the name of a student.

#### Queue module commands

() - element is optional

[] - element is required

*a cursive command* - the command requires the reply to a queue

| Command                 | What it does                                                                           |
|-------------------------|----------------------------------------------------------------------------------------|
| /queue (header)         | Creates a queue with a header                                                          |                               
| */swap [index] [index]* | Swaps records in the queue by unique indexes. One of indexes should exist in the queue |
| */rm [index list]*      | Deletes records in the queue by indexes.                                               |
| */header [name]*        | Sets a header to the queue                                                             |
| *[record]*              | Creates record in the queue                                                            |

#### What to do with Queue module

* A parameter to command should contain less than 100 characters.
* A number(index) is a natural number (1,2,3,4 ... 123, 124 ...)
* 256 is maximum number of records
* Queues are sorted by ascending numbers.

It's possible to:

* create a record by the /queue (header)
    * A header is optional text (no more than 100 chars);
      Examples:
        * /queue
        * /queue Math, 2nd work


* add a record *[record]*
    * It adds a record to a queue
    * A record consists of index(a positive number) and name (no more than 100 chars);
    * Reply to a queue is required
    * There are 2 ways to add a record:
        1. Add the last element - requires only name.
            * An example: Denis Jibrony
        2. Add the record by its index - requires empty space.
            * An example: 22 Antony Blinken


* replace records by the */swap [index] [index]* command;
    * It swaps two records in a queue by index
    * At least one index exists in a queue
    * If only one index exists in a queue, the record is moved
    * Reply to a queue is required
        * An example: /swap 25 3


* delete records by */rm [index list]* command;
    * It removes records by indexes
    * Reply to a queue is required
    *
    * Index list is at least one number and at most 256 numbers
        * An example: /rm 12 2 4 2 55
        * An example: /rm 1


* set a header for a queue - */header [name]* command;
    * It sets a header to a queue
    * Reply to a queue is required
    * A header is text (no more than 100 chars);

There is a hint when you click at one of the button, if you forget one

![hint_buttons.png](images_for_readme/hint_buttons.png)

---

### Gmail module

The module allows students to bind a gmail account to a group.
Thereby, every new gmail messages will be sent to the group.

#### Gmail module commands

[] - element is required

| Command                   | What it does                                             |
|---------------------------|----------------------------------------------------------|
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail |                                
| /gmail                    | Sends the gmail address a user has set                   |                     
| /off_gmail                | Stops the gmail module for this group                    |                               
| /on_gmail                 | Resumes the gmail module for this group                  |                               

#### Gmail module set up

Firstly, in order to set gmail module up you need to get application password from your gmail.

**The detail google guide how to get one: https://support.google.com/accounts/answer/185833**

**Secondly, it's required to turn on IMAP in your gmail account and DON'T forget to save changes**

The link to settings: https://mail.google.com/mail/u/1/#settings/fwdandpop

You should to do this:
![img.png](images_for_readme/gmail_imap.png)

Then you should send /gmail [gmail] [app-pass] in the chat with the bot like below:

> /gmail yourgmail@gmail.com gsmpchivlxkoiqad

You will get a feedback like below:

![img.png](images_for_readme/gmail_feedback.png)



---

### Schedule module

The module allows students to bind a lesson schedule to a group.
Thereby, the messages about lessons will be sent to the group.

#### Schedule module commands

[] - element is required

| Command               | What it does                                                                |
|-----------------------|-----------------------------------------------------------------------------|
| /schedule [file.json] | Takes a file.json and it sets the schedule for the group                    |
| /schedule             | Returns the json file a user has set. If he hasn't the example json is sent |                  |            
| /on_schedule          | Resumes the schedule module for this group                                  |                               
| /off_schedule         | Stops the schedule module for this group                                    |

#### Schedule field rules

* week: 1 or 2. There are odd days(1) and even ones(2). If not present - both weeks. **Optional**
* link: a link string of the meeting "https://...". **Optional**
* day: "Monday", "Thursday" ... "Sunday". Any day of the week. **Required**
* name: The subject name or anything else. **Required**
* time: 24-Hours time format: "00:00". **Required**

#### An example of json schedule

```json
{
  "schedule": [
    {
      "link": "https://zoom.com/321",
      "day": "Monday",
      "time": "08:30",
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

#### Schedule module set up with images

Firstly, a json schedule file is required to be created like [this above](#an-example-of-json-schedule)

![schedule_json.png](images_for_readme/schedule_json.png)

Secondly, you have to attach the file in telegram in the chat with the bot

![choose_schedule.png](images_for_readme/choose_schedule.png)

Write in the following caption the command "/schedule" and click "send" like below:

![img.png](images_for_readme/send_as_schedule.png)

After all you will get a feedback like down below:

![schedule_feedback.png](images_for_readme/schedule_feedback.png)

---

### Basic module

The module allows students to use simple commands
to make the bot say "hello", to send json of message and
say the current week number

| Command | What it does                                 |
|---------|----------------------------------------------|
| /hi     | Replies "hello". It is made if the bot works |
| /json   | Sends the json file of the message           |
| /week   | Reports the current week number              |
| /help   | Sends helpful message with all the commands  |
| /start  | Sends helpful message with all the commands  |

---

## Installation on a server

### Telegram API keys

Firstly, you need to be registered in Telegram

Secondly, You need to get Telegram **api_id** and **api_hash**.

You can get api_id by the link:
https://my.telegram.org/apps
The Complete guide:
https://my.telegram.org

Thirdly, you have to obtain a telegram bot and its **bot_token**
The complete guide:
https://core.telegram.org/bots/tutorial

### MongoDB Atlas

You need to obtain MongoDB database in Atlas by the guide: https://www.mongodb.com/basics/create-database

After all, you need to obtain **connection string**. The guide is
helpful: https://www.mongodb.com/docs/guides/atlas/connection-string/

### Student Servitor Bot set up

Firstly, you need to copy this project by the command:

```bash
git clone https://github.com/Darkinowls/student_servitor_bot.git
```

Then you need create .env file with your **api_id**, **api_hash**, **bot_token** and **connection string**

There is an .env.example as an example:

```dotenv
API_ID=12345678
API_HASH=12345678906de2fbmage1a3b6e8TYPE4
BOT_TOKEN=1234567890:AAFUawNMAGELchPtMjmkyMagethXjDBKiu4

MONGO_CONNECTION_STRING=mongodb+srv://user:password@cluster.mongodb.net/student_bot?retryWrites=true&w=majority
```

Don't forget to set up venv and activate it:

```shell
python -m venv .venv
source .venv/Scripts/activate
```

Then, in order to install all the required modules in this python project you need to run:

```shell
pip install requirements.txt
```

To run the project:

```shell
python main.py
```