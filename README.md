# TConfig - Test Configuration Generator

#### Combinatorial test coverage:  generate pair-wise combinations of values using covering arrays.

Generates covering arrays based on two algorithms:

- Implementation of the "recursive block" algorithm (Williams).
- Implementation of the "in-parameter order" greedy algorith (Lei and Tai).

Covering arrays have the property that for a set of parameters, and a set of discrete values for
each parameter, every n-way combination of parameter values is covered somewhere in the array, for
specified coverage degree 'n'.  Example:  for n = 2, the tool generates a set of test configurations
where every pair-wise combination of parameter values is covered.

This repo contains a (work in progress) port of my graduate school project implementation tool 
"TConfig" that was originally written in Java, circa late 1990s.  The ported version is in Python,
and sets up a REST API for a web service interface.  Please see this repo (which is even more of a work 
in progress than this repo) for a front-end browser client to work with the REST API:
https://github.com/awwilliams/tconfig-client

## Example

Suppose that you had to test a Python program that offered a REST API and a browser
client (such as this one :-), and cross-platform functionality is a concern.  Here
are four parameters of interest, and a set of values for each parameter.

**Operating systems:**
1. Windows
2. Mac OS
3. Linux

**Python version:**
1. 3.6
2. 3.7
3. 3.8
4. 3.9

**Browser**

1. Firefox
2. Chrome
3. Edge
4. Safari

**DB backend**

1. SQLite
2. MySQL
3. Postgres

Testing all possible combinations would require 3 x 4 x 4 x 3 = 144 configurations.

However, suppose that it would be acceptable to include every pair-wise interaction in some test
configuration, but that it is unlikely that there would be some issue that would only appear if there
was a particular 3-way or 4-way combination of values.  Then, a covering array of degree 2 would
suffice.

Here is a covering array of degree 2 for the above parameters and values.  It consists of
only 16 configurations:
    
Config # | OS      | Python version |  Browser |  Database |
| -----: | :-----: | :------------: | :------: | :-------: |
|  1     | Windows | 3.6            | Chrome   | SQLite    |
|  2     | Linux   | 3.7            | Firefox  | MySQL     |
|  3     | Mac OS  | 3.8            | Firefox  | Postgres  |
|  4     | *       | 3.9            | Safari   | *         |
|  5     | Windows | 3.7            | Edge     | *         |
|  6     | Linux   | 3.6            | Safari   | Postgres  |
|  7     | Mac OS  | 3.9            | Chrome   | MySQL     |
|  8     | *       | 3.8            | Firefox  | SQLite    |
|  9     | Windows | 3.8            | Safari   | MySQL     |
| 10     | Linux   | 3.9            | Edge     | SQLite    |
| 11     | Mac OS  | 3.6            | Firefox  | *         |
| 12     | *       | 3.7            | Chrome   | Postgres  |
| 13     | Windows | 3.9            | Firefox  | Postgres  |
| 14     | Linux   | 3.8            | Firefox  | *         |
| 15     | Mac OS  | 3.7            | Firefox  | SQLite    |
| 16     | *       | 3.6            | Edge     | MySQL     |

(*) - Any value can be used in these configurations; specific values are not needed
for coverage purposes.

Observe that if you choose any 2 of the columns, all combinations of values between
those two columns will be covered within the set of configurations.

### Setup

#### Requirements

- Python >= 3.6.  It is recommended to create a virtual environment, and then install packages in that environment
- Required Python packages:  ``pip install -r requirements.txt``
- Development Python packages:  ``pip install -r requirements_dev.txt``

#### Running (Windows)

Open a console window in the top-level project directory.

In that window:

- ``set FLASK_APP=tconfig.api.service``
- (optional, not for production) ``set FLASK_DEBUG=1``
- ``flask run``

Open a browser, and navigate to this URL:

- http://127.0.0.1:5000/tconfig/api/v1/

The REST API documentation should be displayed.  Expand the default
namespace to see the available REST commands.
  
#### Populate sample parameters and values:


- http://localhost:5000/tconfig/api/v1/setup

You should see JSON output similar to the following:

```buildoutcfg
{
    "parameter_set": {
        "parameters": [
            {
                "values": [
                    {
                        "parameter": 1,
                        "position": 0,
                        "name": "Red",
                        "uid": 1
                    },
                    {
                        "parameter": 1,
                        "position": 1,
                        "name": "Green",
                        "uid": 2
                    }
                ],
                "position": 0,
                "excluded": [],
                "excluded_by": [],
                "name": "Colour",
                "parameter_set": 1,
                "uid": 1
            },
            {
                "values": [
                    {
                        "parameter": 2,
                        "position": 0,
                        "name": "Bird",
                        "uid": 3
                    },
                    {
                        "parameter": 2,
                        "position": 1,
                        "name": "Cat",
                        "uid": 4
                    },
                    {
                        "parameter": 2,
                        "position": 2,
                        "name": "Dog",
                        "uid": 5
                    },
                    {
                        "parameter": 2,
                        "position": 3,
                        "name": "Fish",
                        "uid": 6
                    }
                ],
                "position": 1,
                "excluded": [],
                "excluded_by": [],
                "name": "Pet",
                "parameter_set": 1,
                "uid": 2
            },
            {
                "values": [
                    {
                        "parameter": 3,
                        "position": 0,
                        "name": "Fast",
                        "uid": 7
                    },
                    {
                        "parameter": 3,
                        "position": 1,
                        "name": "Slow",
                        "uid": 8
                    }
                ],
                "position": 2,
                "excluded": [],
                "excluded_by": [],
                "name": "Speed",
                "parameter_set": 1,
                "uid": 3
            },
            {
                "values": [
                    {
                        "parameter": 4,
                        "position": 0,
                        "name": "80s",
                        "uid": 9
                    },
                    {
                        "parameter": 4,
                        "position": 1,
                        "name": "20s",
                        "uid": 10
                    }
                ],
                "position": 3,
                "excluded": [],
                "excluded_by": [],
                "name": "Music",
                "parameter_set": 1,
                "uid": 4
            }
        ],
        "position": null,
        "name": null,
        "uid": 1
    },
    "parameter_set_url": "/tconfig/api/v1/parameterset/"
}
```

