# Word Occurences

This program parses a website using BeautifulSoup4 and urllib and finds the 5 words with the most occurences.
It then plots the words along with the amount of occurences on a graph using the matplotlib library

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them. I am using pip for windows, a simple google search will give
you results on what to do for your operating system or how to install and use pip.

```
pip install beautifulsoup4
pip install matplotlib
```

### Screenshots
Running the program from the command prompt
<img src="https://github.com/Throupy/My-Coding-Projects/blob/master/WORD%20OCCURENCES/screenshots/command_promt.png">

<img src="https://github.com/Throupy/My-Coding-Projects/blob/master/WORD%20OCCURENCES/screenshots/graph.png" width=300 height=270>


### Argparse information
Argparse only takes one command from the command prompt which is `--url` which is the URL to parse </br>
an example would be: `python word_times_finder.py --url "https://www.youtube.com"`

