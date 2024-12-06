Python Tkinter Minesweeper
===========================

Minesweeper game written in Python using Tkinter GUI library.

<img src="https://i.imgur.com/8JwCyAQ.png" alt="Screenshot on OSX" height="350"/>

*** Project Instructions can be found on FinalProjectV2.pdf****
*** Method level mapping of original minesweeper vs our MVC implemented Minesweeeper can be found on Method level Mapping.pdf ***

Game Features:
----------------
Multiple difficulty levels (Beginner, Intermediate, Expert)
GUI and Text-based interfaces
Test mode with custom board layouts
Treasure hunt feature for instant wins
Timer tracking gameplay duration

Game Controls:
----------------
Action         GUI	                  Text Mode
Reveal Cell	   Left Click	         'r' command
Flag Cell	   Right Click           'f' command
Quit Game	   Close Window	         'q' command

Display Symbols:
===============
Symbol	Meaning
💣	    Mine
🚩	    Flag
💎	    Treasure
❌	   Wrong Flag
🎉	    Victory

Difficulty Levels:
==================
Level	         Board Size	   Mines Range
Beginner	     8x8	       1-10
Intermediate	16x16	       11-40
Expert	        30x16	       41-99

Test Mode Features:
==================
Custom board layouts via CSV files
Specific mine placement rules
Optional treasure placement
Board validation checks

Architecture:
============
The game follows MVC (Model-View-Controller) architecture:
Model: Handles game logic and state
View: Manages display (GUI/Text)
Controller: Processes user input

Requirements:
=============
Python 3.x
Tkinter (for GUI mode)
CSV support (for test mode)

Running the Game
================
bash
python3 minesweeper.py