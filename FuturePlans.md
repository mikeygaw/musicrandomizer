**Immediate Plans:**

Bulk Importer for bands.

Group related functions together as classes.

User defined names and weights for favorite levels

Unit Tests?

Randomizer will be adjusted to ask the user wether to allow repeats or all differnet albums. Right now I have it setup to reselect an album if 
the one chosen had already been picked this session.
There's two problems with this:
A) A while loop can go infinite if the number of albums to pick from is less than the number of albums the user entered to pick
B) I have not been able to find a way to modify iterations or range to ensure tha correct number of albums are chosen.

**Long Term Plans:**

Weighting is going to be more dynamic and based on play counts and other variables. This requires me to learn Api's to pull data from 
Last.fm
