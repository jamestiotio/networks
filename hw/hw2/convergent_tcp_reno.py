#!/usr/bin/env python3
# Demonstration of convergent and stable TCP Reno sawtooth behavior for Homework 2 Question 5.3 & 5.4
# James Raphael Tiovalen (1004555)

N = 10000000
cutoff = 120
increase = 10

# These initial seed values actually do not matter in the long run (i.e., they can take any real values), as long as they are not too far away to converge after N iterations
c1, c2 = 80, 40

print("CONVERGENT MAXIMUM CWND VALUES\n")

### Question 5.3
for _ in range(N):
    if c1 + c2 >= cutoff:
        # We pick only the maximum cwnd values and see how they settle/converge
        c1_max, c2_max = c1, c2
        c1, c2 = c1 / 2, c2 / 2
    else:
        c1 += increase
        c2 += increase

assert c1_max + c2_max == cutoff

print(f"QUESTION 5.3:\n- Connection 1: {c1_max} KB\n- Connection 2: {c2_max} KB\n")

### Question 5.4
for i in range(N):
    if c1 + c2 >= cutoff:
        # We pick only the maximum cwnd values and see how they settle/converge
        c1_max, c2_max = c1, c2
        c1, c2 = c1 / 2, c2 / 2
    else:
        c1 += increase
        # This actually does not matter as well in the long run (whether it is 0 or 1), as long as it is ONLY either one and it occurs half of the time relative to c1
        # The following line would work as well:
        # if i % 2 == 1:
        if i % 2 == 0:
            c2 += increase

assert c1_max + c2_max == cutoff

print(f"QUESTION 5.4:\n- Connection 1: {c1_max} KB\n- Connection 2: {c2_max} KB\n")
