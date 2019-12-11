# GSP Algorithm implementation with Python
---
## Installation

Requires Python 3. 
Python 3.6+ is preffered for an ordered output. Because in Python 3.6+ dictionaries are insertion ordered.
[Python 3.7 installation](https://www.python.org/downloads/release/python-370/)
## Run

```
python3 GSP.py <input_file> <output_file> <minimum_support_value>
```
##### *Example Run Command*

```
python3 GSP.py input.txt output.txt 0.75
```

##### *Example Input File*
```
(4), (7), (1 6), (1 3), (2 4), (3)
(1 4), (3), (2 3), (2 3 4)
(5 6), (1 2), (5 6), (3), (2)
(2), (3 4), (2 5), (1), (2 4)
```

##### *Example Output File*
```
(1) #SUP: 4
(2) #SUP: 4
(3) #SUP: 4
(4) #SUP: 3
(2 4) #SUP: 3
(1), (2) #SUP: 4
(1), (3) #SUP: 3
(1), (4) #SUP: 3
(2), (2) #SUP: 3
(2), (3) #SUP: 4
(3), (2) #SUP: 4
(3), (4) #SUP: 3
(4), (2) #SUP: 3
(4), (4) #SUP: 3
(1), (2 4) #SUP: 3
(1), (3), (2) #SUP: 3
(3), (2 4) #SUP: 3
(4), (2 4) #SUP: 3
```