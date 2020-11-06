#!python3

# ThesisWC.py - does some cleaning of a text file and makes it into a wordcloud
# Shivan Sivakumaran - 06/11/2020

def main():
    return

def ThesisWC(file):
    """
    file: this a file to be made into a wordcloud - must be in .txt format
    """
    
    # importing and setting up libraries
    import random as r
    import pandas as pd
    import re

    import matplotlib.pyplot as plt
    #%matplotlib inline
    plt.rcParams.update({'font.size': 22})

    from wordcloud import WordCloud, STOPWORDS

    import spacy

    spacy.prefer_gpu()
    nlp = spacy.load("en_core_web_sm")
    
    # opening text file
    with open(file, 'r') as f:
        text = f.read()
        
    print('Text Length (char): ', len(text))
    
    # tokenisation and cleaning text
    doc = nlp(text)
    exclude_list = ['-', '/', '&']
    clean_doc = [_.lemma_.lower() for _ in doc if _.pos_ != 'PUNCT' 
                                            and '\n' not in _.text 
                                            and not _.is_stop
                                            and _.text not in exclude_list
                                            and not bool(re.search(r'^\w\.$', _.text))]

    wordcloud = WordCloud(width = 3000, height = 2000,
                        random_state=1, background_color='#3F3F3F',
                        colormap='rainbow', collocations=False).generate(' '.join(clean_doc))


    fig = plt.figure(figsize=(20, 15))
    imshow = plt.imshow(wordcloud)
    axis = plt.axis('off')

if __name__ == '__main__':
    main()
