# wordle-attendant
Program that is designed for ~~solving on his own~~ helping user guess daily word in [wordle](https://www.nytimes.com/games/wordle/index.html) game.
  Works only with Firefox webbrowser.


## Example:
![demo](https://github.com/P4llix/wordle-attendant/blob/main/doc/demo.gif)

## Requirements:

- python v3.8+
- geckodriver (with path added to system variables)
- libraries: Selenium (v3.141), json, time


## How to start

Simply just download it and run *main.py* file

## Explanation
The creation process consists of 3 parts:

### 1. Create list of words
Reprocessed dictionary so searching word doesn't take lots of time. File *create_dictionaries.py* in assets folder splits raw txt like *robot* or *train* into structure that contains number of each char and index where char occurs.
```
    "robot": {
        "char_amount": {
            "r": 1,
            "o": 2,
            "b": 1,
            "t": 1
        },
        "char_index": {
            "0": "r",
            "1": "o",
            "2": "b",
            "3": "o",
            "4": "t"
        }
    },
    "trail": {
        "char_amount": {
            "t": 1,
            "r": 1,
            "a": 1,
            "i": 1,
            "l": 1
        },
        "char_index": {
            "0": "t",
            "1": "r",
            "2": "a",
            "3": "i",
            "4": "l"
        }
    }
```
Later on, using above word structure are created *prepeared_list.json* file, where words are assigned to specific alphabetic letter
```
    "a": {
        "index": {
            "0": ["aback", "abase", "abate", ...],
            "1": ["bacon", "badge", "badly", ...],
            "2": ["aback", "abase", "abate", ...],
            "3": ["ahead", "algae", "allay", ...],
            "4": ["agora", "alpha", "aorta", ...]
         },
       "present": {
            "1": ["abbey", "abbot", "abhor", ...],
            "2": ["aback", "abase", "abate", ...],
            "3": [],
            "4": [],
            "5": []
        }
    },
    ...
```
There is a redundancy of many words, however program doesn't need to loop thru dictionary. Every join/exclude action does intersection or union of two sets.

### 2. Scrapp data from website
Easiest part. When user confirm his choice, char and state of each tile in current round is collected.
