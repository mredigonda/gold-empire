# "Gold Empire" - Django Project

Gold Empire is a browser-based toy game project similar in various aspects to [Ogame](https://us.ogame.gameforge.com/) and [Ikariam](https://us.ikariam.gameforge.com/).

You can look at a quick demo [here](https://mred-django-project.herokuapp.com/).
- username: demo
- password: secretkey 

You could also create a new account, you don't need any email. (I know that's dangerous, but this is for educational purposes only).
The database resets every 24h, so don't expect your account to last long.

In this game, there are three resources (gold, rock and wood), and you goal is to get more and more resources (by upgrading buildings that produce those resources) and to use them to create (or buy, I don't know) units that give you the power to attack other users in the game (and steal their resources).

## Notes

This game is not meant for playing, it's just a game made with the sole purpose of learning more about the Django Framework. 

## General Guide

### Home

In the home page, you can view information on the number of units of each type that you have. You can also view the last 5 battles in which you participated, and the result of each of them.

### Buildings

In the buildings page, you can upgrade your buildings and check the current level of each of them. It's not indicated in the game, but these are the details of each building:

- Gold Mine: it produces `1 + 3*(LEVEL-1)` units of gold per second.
- Rock Mine: it produces `4 + 5*(LEVEL-1)` units of rock per second.
- Lumber Camp: it produces `5 + 7*(LEVEL-1)` units of wood per second.

### Units

In the units page you can view details about each type of unit. There are six different types of units, and the details of each of them (attack, defense, costs, etc.) are provided in this page. The units are used to fight with other users, which will be explained below.

### Attack

Here, every five minutes, you will see a different user that you can challenge to a battle. In a battle against someone, the result depends on the quality and quantity of your units against the ones of your opponent. After you click the 'attack' button, the probabilities are calculated and the result is given as a notification. If you win, you get 10% of the resources of your opponent, and you destroy 10% of your opponent's units. If you lose, you lose 10% of your units.

## Possible Improvements

There are tons of ways in which one may improve this project. I'll write a few here:

- You can battle the same guy over and over again. The correct thing to do would be to provide a countdown after each battle, so you don't abuse any other player.
- The notifications on the homepage look exactly the same as other kind of notifications. This can be improved (UI). 
- A tutorial could be added to the menu, explaining common things. 
- In these kind of games, there are also other types of buildings that are about 'technologies'. Something like this could be implemented.
- The resources could be updated live in the browser.
