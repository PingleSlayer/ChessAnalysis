# ChessAnalysis

## Introduction
Welcome to the Chess Game Analyzer project! This open-source project aims to provide a versatile and extensible tool for analyzing chess games. Whether you're a chess enthusiast, a developer looking to contribute, or someone interested in understanding the intricacies of chess games, this project is designed to cater to your needs.

## Features
- PGN File Support: Easily import and analyze games from Portable Game Notation (PGN) files, a standard for representing chess games.
- Position Analysis: Gain insights into key positions throughout the game, allowing for a deeper understanding of strategic elements.
- Move Analysis: Dive into detailed evaluations for each move, highlighting the best moves and potential improvements.
- Game Analysis: Receive an overall analysis of the entire game, helping you grasp its flow and critical moments.

## Contributing
We welcome contributions/suggestions from the community! If you'd like to contribute to the project please do.

(This is my first real GitHub project so if I am doing something wrong let me know!)

## To Do
- Fix problem in move_analysis.py -> move_info() -> no piece at to_square?
- Properly test existing code
- Find easy to understand, useful move tags and accompanying boundary conditions
- Use Lichess API for openings, endgame tablebase,...
- Add tools for positional analysis like king safety, board control, pawn structure, attacking chances, threats,...
- Add tools for move analysis like movetype (fork, pin,...), alternatives,...
- Add tools for game analysis like accuracy, recommended areas of improvement,...
- Display for easy use maybe?

## Sources
- Using stockfish as engine
- Using python-chess library
- Using openings from chess-openings repository
