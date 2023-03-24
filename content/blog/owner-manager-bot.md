+++
title="Owner Manager Bot"
date=2022-05-16
template="post.html"

[extra]
image="owner-manager-bot.png"
+++

## Motivation

Visits have recently become available again at my residence hall. This is a great opportunity to invite friends and colleagues over for a good time or to do college work, so it would be nice if I had an extra chair. Others friends of mine have thought the same and only one of them has an extra chair, so we have to coordinate.

We have a Telegram group between us where we can talk to pass the chair to each other. Still, asking for who has the chair and having to wait two hours for the answer is not very comfortable. For me, this is a perfect opportunity to solve a small problem with an overengenieered solution with which I can experiment with some new technology. And this is how `owner-manager-bot` was born.

## How it works

As I don't have much time available and I wanted to experiment a little bit with some technology that will be discussed later, I decided to keep the bot with a fairly simple structure. I have thought about expanding it with some additional functionalities that will later be discussed, but I have preferred to opt for a simple and transparent interface.

The structure for using the bot is very straightforward. The bot is added in a group to manage a set of *elements*. Each element is assigned an *owner*. Users then can:
- Create an element with `mkitem`.
- Delete an element with `rmitem`.
- Assign themselves as owners of an element with `chown`.
- Show a summary of the elements that correspond to each owner with `status`.

## Technologies

To develop this project I have used three technologies mainly. I have programmed with Python, for the facility that it gives me when programming and using its modules.

Specifically, I was interested in using [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/), with which I had previously worked in the development of [iGo](https://github.com/albertcanales/iGo-AP2). Their documentation is a marvel and I wanted to work with a tool that I was familiar with.

Where I wanted to explore a bit was in the DB. I have always used SQL based databases: SQLite, Microsoft SQL Server and Postgresql. I've adapted a lot conceptually to the relational model, and I was looking for a small project to get my feet wet with the NoSQL model, and this was the perfect opportunity. I went with [TinyDB](https://tinydb.readthedocs.io/en/latest/) because of its incredible simplicity, allowing me to get first impressions of the model without getting into the complications of the chosen implementation.

Finally, as I had never made an installer in Bash, I decided to implement one that allows me, with a single command, to have the bot running on the server at all times.

## Implementation

As said, the implementation is quite simple. The code it distributes in two files that, roughly speaking, differentiate the frontend and the backend:

- `bot.py`: Contains the main, starts the bot and manages the interaction with the user with a function for each command. It makes calls to `db.py` to perform data queries.
- `db.py`: Provides an API to interact with TinyDB database objects. In most cases the return value is used as an indication of whether the operation was successful, so that the frontend can notify the user accordingly.

In addition to the Python code, `install.sh` is also included, which installs the bot and generates the corresponding service for Systemd.

## Extensions

As stated above, one of the pillars of the project is to keep the tool simple to use. In my opinion, that rules out some ideas such as the following:

1. being able to use `mkitem`, `rmitem` and `chown` for several elements simultaneously. If this were done, it should force some arbitrary restriction in the names (such as not containing spaces) or complicate the commands, both undesirable.

2. Being able to `chown` another user. For privacy, the Telegram API does not allow to get all users in a group. In order to implement this, you would have to register the possible owners first, just like with an `mkown` command, but it would complicate the interface too much. This could be avoided if all owners were administrators, but it is too restrictive a condition.

Still, there are a couple of interesting ideas that might not be so disruptive to the simplicity of the program, although they seem to me to be specific enough not to be necessary:

1. restrict `mkobj` and `rmobj` to administrators. An `access` command could be added that would support two modes, *public* (everyone can use the bot) and *restrict* (restricting bot use to administrators).

2. Add a `statistics` command to obtain certain interesting data. For example, report which are the most common owners of each object.

Finally, the installer could receive a couple of improvements that I will probably implement in the future, as they will be useful for other projects:

1. Possibility to update or uninstall the program.

2. A lowering of privileges in the execution of the program. Currently the default installer runs the program as root because its database is in the same location as the executables, which is write-protected. It would be convenient to move the DB to a location with lower privileges in order to be able to run the program without needing to be root.

## Summary

We have been using the bot for a few days with friends and it fulfills its initial task perfectly, although it is not very complicated considering that in our case we only use it for a single element, the chair.

Regarding its implementation, I'm quite happy to have achieved a simple set of instructions: essential but sufficient. Naturally it is easy to be minimalist in such a basic project, but when I design projects it is common for me to lose track with additional functionalities that rarely get used and muddy the clarity of the user interface and the code implementation. It has been a good exercise to try the opposite (and in my opinion succeed).

About TinyDB and the non-relational model, technology with which I wanted to experiment in this project, my feelings are not particularly good. It is true that being less restrictive allows you not to be so meticulous in the initial design of the database, but that brings an instability when manipulating the data that I don't feel with the relational model and I don't like it.

I will try to use this model again for future projects, I am sure that with practice I will adapt better to its paradigm and feel more comfortable. It is also possible that I will try some other NoSQL based system, because although I like the simplicity of TinyDB, I don't know if its fundamental commands would adapt very well to more complex projects, and other systems may allow simpler implementations for the programmer.

Finally, I am also happy with how the installer turned out. It is a piece that always remains in the background but that facilitates the use of a project, so now that I have already programmed mine I will try to implement it in all the projects that require it.

* * *

*You can take a look at the source code of the project [here](https://github.com/albertcanales/owner-manager-bot). For any suggestion on comment, don't hesitate to [contact me](mailto:albertcanalesros@gmail.com)*

*Thanks for reading!*

