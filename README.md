TConfig - Test Configuration Generator

Generates covering arrays based on two algorithms:

- Implementation of the "recursive block" algorithm (Williams).
- Implementation of the "in-parameter order" greedy algorith (Lei and Tai).

Covering arrays have the property that for a set of parameters, and a set of discrete values for
each paramater, every n-way combination of parameter values is covered somewhere in the array, for
specified coverage degree 'n'.  Example:  for n = 2, the tool generates a set of test configuration
where every pair-wise combination of parameter values is covered.

This repo contains a (work in progress) port of my graduate school project implementation tool 
"TConfig" that was originally written in Java, circa late 1990s.  The ported version is in Python,
and sets up a REST API for a web service interface.
