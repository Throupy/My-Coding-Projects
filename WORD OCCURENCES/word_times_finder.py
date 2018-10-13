from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request
import collections
import re
import matplotlib.pyplot as plt
import sys
import argparse
#ArgParse config
def parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--url',
                        type=str,
                        default='https://www.google.com', #Change this to URL if you're executing through script
                        help='Enter site URL to parse')
    args = parser.parse_args()
    sys.stdout.write(str(main(args)))

def main(args):
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']: #If there is a HTML tag with data that user can see
            return False #False
        if isinstance(element, Comment): #Or if it's a comment
            return False #False
        return True 

    def text_from_html(body):
        soup = BeautifulSoup(body, 'html.parser') #give base html
        texts = soup.findAll(text=True) 
        visible_texts = filter(tag_visible, texts) #filter to visable text
        return u" ".join(t.strip() for t in visible_texts) #readable version (kind of!!)

    html = urllib.request.urlopen(args.url).read() #get data from a html site
    raw = text_from_html(html).lower() #get the visible words
    words = re.findall(r"\w[\w'’]*", raw) #find all words
    #your you're
    most_common = collections.Counter(words).most_common(20) #find most common occurences
    #you

    final = [] 
    for x in range(1,len(most_common)+1):
        try:
            if len(most_common[x][0]) < 2: #If it's a single letter word
                pass
            else:
                final.append(most_common[x])
        except IndexError:
            pass

    words = [final[0][0],final[1][0], final[2][0], final[3][0], final[4][0]] #dataset
    times = [final[0][1],final[1][1], final[2][1], final[3][1], final[4][1]] #dataset
    plt.bar(words, times ,label="Bar Chart", color="orange") #plot
    plt.xlabel('Word', color='c') #metadata
    plt.ylabel('Occurrences', color='c') #metadata
    plt.title('Word Occurrences') #metasdata
    plt.show() #show graph

if __name__ == '__main__':
    parse()









    
