There's a game called Deuces I grew up playing. 
It's also known by Big Two or in Cantonese, Chaw Dai Dee. 

This little side project contains an initial attempt at generating all possible game states for Deuces. 
There are many, many states, and I'm estimating the final product will be gigabytes worth of game state. 
I'm guessing it will not be nearly as huge as chess, since the game state converges over time, but we'll see. 

Currently, I'm porting over all the logic into Go, since it will be orders of magnitude faster than Python. 

In the future, I might try to create a bot that loads the necessary gamespace into memory and plays as optimally as possible. 
