# Student servitor bot - Abobus



Telegram bot, which is created to support students.
Has 3 modules:

- list module
- gmail module
- schedule module

---

## Bot commands

() - element is optional
[] - element is required

| command                   | what it does                                             |
|---------------------------|----------------------------------------------------------|
| /list (head)              | Creates list-queue. Head is optional                     |                               
| /swap [index] [index]     | Swaps records in the queue by indexes                    |
| /rm [index list]          | Deletes recods in the queue by indexes                   |
| /head [name]              | Sets header of the queue                                 |
| *\> reply to list-queue*  | Creates record in the queue                              |
| /gmail [gmail] [app-pass] | Creates gmail connection between the group and the gmail |                               
|                           |                                                          |                               