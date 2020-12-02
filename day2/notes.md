# Part 1

In part 1, we used some classes to make the code more obvious for the later changes.

The complexity here is pretty simple to figure out:

## Parsing phase

Input length n
string length m

For each input:
    Split the string into two strings. Python string splitting takes `O(m + k)`, where here k is 1.
    then we do a second split for the string for the policy, which is also worst case `O(m + k)`,
    where k is 1.

    `O(m+k)` simplifies to `O(m)`.

This inital parsing phase is `O(n*m)`. Which in this case we can assume `O(n)`
(the time is dominated by the number of inputs, not the longest input)

## Validation phase

For each input:
   Go through the entire password (worse case `O(m)`), and count the number of times a character shows up
   Ensure that number is between some bounds (constant time)

So again, `O(n*m)`, so `O(n)`.

Therefore, we could call this `O(2n)`, or in otherwords, `O(n)`.

# Part 2

In part 2, our code actually speeds up. When looking up a specific character, we don't have to iterate,
thats a constant time lookup. So the second phase is now actually constant per input. This means we stay
at `O(n)` for parsing.

Here the `is_valid` method is the only bit of code that needs to change. We could also do it using xors
on the condition, but really, a count is a clean, and easy to extend, way of getting the job done.

