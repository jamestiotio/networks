#!/usr/bin/env python3
# Demonstration of convergent and stable TCP Reno behavior for Homework 2 Question 5.3 & 5.4
# James Raphael Tiovalen (1004555)

N = 1000000
cutoff = 120
increase = 10

# These initial seed values actually do not matter in the long run
c1 = 80
c2 = 40

print("CONVERGENT MAXIMUM CWND VALUES\n")

# Question 5.3
for _ in range(N):
    if c1 + c2 >= cutoff:
        c1, c2 = c1 / 2, c2 / 2
    else:
        c1 += increase
        c2 += increase

print(f"QUESTION 5.3:\n- Connection 1: {c1} KB\n- Connection 2: {c2} KB\n")

# Question 5.4
for i in range(N):
    if c1 + c2 >= cutoff:
        c1, c2 = c1 / 2, c2 / 2
    else:
        c1 += increase
        # This actually does not matter as well in the long run (whether it is 0 or 1), as long as it is ONLY either one and it occurs half of the time relative to c1
        # The following line would work as well:
        # if i % 2 == 1:
        if i % 2 == 0:
            c2 += increase

print(f"QUESTION 5.4:\n- Connection 1: {c1} KB\n- Connection 2: {c2} KB\n")
