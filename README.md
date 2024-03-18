# CALCULATING PI BY HAND ~~using a computer and Python~~

This project implements the calculation done in Matt Parker's 2024 video of his attempt to calculate the mathematic constant π without using any computation device.

The formula used peaked my curiosity and I though it would be fun to implement it in Python and see how long a Python code could reach the same precision they got in the video.

## Math and computer

This projects implements all of it's math functions. Since it relies on numbers with a lot of decimal places, it's not possible using float, or even double, to assign the values.

All calculations were done following algorithms that uses numbers in string.

### Performance

Most of the calculations are repeated several times as the numbers grow both in module and in number of decimal places. This makes the code really inefficient.

To help speed up the process, the code uses just that: Process. The multiprocessing module to be specific.

Each bit of computation is delegated to run in a separated process, and each result is combined at the end to form the final value of pi.

## Precision

The numbers' precision is dictated by the `DECIMAL_LIMIT` environment variable. But this doesn't mean it has "DECIMAL_LIMIT" number of correct decimal places. As each calculation is made with a potentially "1-digit off" value, all of this is carried over, and the final result is usually 3 or 4 places wrong.

This means that if you assign `DECIMAL_LIMIT=200`, you're more likely to have 196 or 197 correct decimal places of pi.