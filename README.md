# 2024 Advent of Code with Python
## Day 6, part 2
Real speedbump in the road here. Example input worked, but not the real input. Made a visualization in js to try to debug it. Took a while, but figured out the following problems with the code:
- Not recording all directions when guard is turning.
- Placing new obstacle on previous path, which means the guard won't reach the obstacle position in the first place.
- Duplicate obstacle positions.

## Day 7, part 1
Once again, example input worked, but real input didn't. I made the wrong assumption that the sum of all values would always be the lower boundry and the product would be the upper boundry. This is not true when one of the number is a 1. Optimizing too hard.
