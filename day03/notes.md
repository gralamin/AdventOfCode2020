# Solution

So here we think of this as a spheroid. This means that instead of repeating the pattern a bunch,
we just wrap around the sides. Then its simply a matter of checking each spot. I'm actually keeping
track of where we are at all times and checking if my code goes out of bounds, but it could be sped
up by simply blindly moving.

In terms of complexity, we are accessing a list of lists at various positions, with worst case infinite
(slope of 0 down), but generally we are just iterating once per line of the input per slope. Thus, this is
essentially O(n) in the cases we are interested in.
