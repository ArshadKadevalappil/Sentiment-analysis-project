#!/usr/bin/env python
# coding: utf-8

# # Step 1: Importing necessary packages

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas
import re
import nltk
nltk.download('opinion_lexicon')
nltk.download('stopwords')
from nltk.tokenize import sent_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.corpus import stopwords
from nltk.corpus import opinion_lexicon
import pandas as pd


# #### Changing the working directory

# In[2]:


pwd


# In[3]:


cd "C:\Users\arshad\Downloads"


# # Step 2: Loading the input data

# In[4]:


data=pd.read_excel('input.xlsx')


# In[5]:


headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0'}
r=requests.get('https://insights.blackcoffer.com/what-if-the-creation-is-taking-over-the-creator/',headers=headers)


# # Step 3: Data extraction
# re package from RegEx module and the BeutifulSoup library is used here 

# # 3.1: Extracting article titles and texts into a list

# In[6]:


c=BeautifulSoup(r.text,'html.parser')


# In[7]:


corpus=[]
for i in data['URL']:
    url=i
    request=requests.get(url,headers=headers)
    content=BeautifulSoup(request.content,'html.parser')
    article=str(content.find_all('p'))
    title=str(content.find_all('h1'))
    x=title+article
    corpus.append(x)


# In[8]:


# checking an element of the list
corpus[1]


# # Step 4: Text processing

# # Step 4.1 Removing the unnecessary html language from the texts

# In[9]:


a=0
for i in corpus:
    corpus[a]=i.replace('<h1 class="entry-title">',"").replace('</h1><p>',"").replace('h1',"").replace('</p>',"").replace('</strong>',"").replace('<strong>',"").replace('<sup>',"").replace('<img alt="" class="size-full wp-image-2969 aligncenter" height="225" loading="lazy" sizes="(max-width: 225px) 100vw, 225px" src="https://insights.blackcoffer.com/wp-content/uploads/2021/04/i01.jpg" srcset="https://insights.blackcoffer.com/wp-content/uploads/2021/04/i01.jpg 225w, https://insights.blackcoffer.com/wp-content/uploads/2021/04/i01-150x150.jpg 150w" width="225">',"").replace('\xa0',"").replace('style=textalign center',"").replace('pimg alt=dataexfiltrationindepth class=sizefull wpimage993 aligncenter height=359 loading=lazy sizes=maxwidth 638px 100vw 638px src=httpsinsights.blackcoffer.comwpcontentuploads201705dataexfiltrationindepth.jpg srcset=httpsinsights.blackcoffer.comwpcontentuploads201705dataexfiltrationindepth.jpg 638w httpsinsights.blackcoffer.comwpcontentuploads201705dataexfiltrationindepth300x169.jpg 300w width=638 p style=textalign centeremsourcehttpsurlzs.coml7bfem pimg alt=dataexfiltration class=sizefull wpimage994 aligncenter height=359 loading=lazy sizes=maxwidth 638px 100vw 638px src=httpsinsights.blackcoffer.comwpcontentuploads201705dataexfiltration.jpg srcset=httpsinsights.blackcoffer.comwpcontentuploads201705dataexfiltration.jpg 638w httpsinsights.blackcoffer.comwpcontentuploads201705dataexfiltration300x169.jpg 300w width=638 p style=textalign centeremsourcehttpsurlzs.comgijxem',"")
    a=a+1


# # Step 4.2: Removing all punctuations except 'full stops'

# In[10]:


punc='''!()-[]{};:'"\,<>/?@#$%^&*_~’—'''
b=0
for x in corpus:
    for i in x:
        corpus[b]=corpus[b].replace(i,i.lower())
        if i in punc:
            corpus[b]=corpus[b].replace(i,"")
    b=b+1   


# In[11]:


#Checking the preprocessed text
corpus[0]


# # Step 4.3: Tokenizing the sentences in each article
# sent_tokenize from nltk library is used here

# In[12]:


tokenized_sentences=[]
for i in corpus:
    sentences=sent_tokenize(i)
    tokenized_sentences.append(sentences)


# In[13]:


# Checking tokenized sentences in an article
tokenized_sentences[1]


# # Step 4.4:Tokenizing the words in each article
# WordPunctTokenizer from l=nltk library is used here

# In[14]:


tokenizer=WordPunctTokenizer()


# In[15]:


tokenized_words=[]
for i in corpus:
    words=tokenizer.tokenize(i)
    tokenized_words.append(words)


# In[16]:


# Checking the tokenized words in a article
tokenized_words[2]


# # Step 4.5:Removing the stopwords from all articles

# In[17]:


stop=stopwords.words('english')


# In[18]:


b=0
for a in tokenized_words:
    for i in a:
        if i in stop:
            tokenized_words[b].remove(i)
    b=b+1


# # Step 4.6: Removing  all the numbers from all articles

# In[19]:


b=0
for a in tokenized_words:
    for i in a:
        if i.isdigit()==True:
            tokenized_words[b].remove(i)
    b=b+1            


# # Step 4.7: Removing one-letter words except 'i' which is counted as a personal pronoun

# In[20]:


import string
alphabets=list(string.ascii_lowercase)
alphabets.remove('i')


# In[21]:


b=0
for a in tokenized_words:
    for i in a:
        if i in alphabets:
            tokenized_words[b].remove(i)
    b=b+1            


# # Step 4.8: Removing all full stops from the articles

# In[22]:


b=0
for a in tokenized_words:
    for i in a:
        if i=='.':
            tokenized_words[b].remove(i)
    b=b+1           


# # Step 5: Text analysis

# #### Making lists of positive and negative words

# In[23]:


p=list(opinion_lexicon.positive())


# In[24]:


n=list(opinion_lexicon.negative())


# # Step 5.1: Calculating the positive score, negative score,polarity score and subjectivity score for each articles and adding them to respective lists

# In[25]:


positive_scores=[]
negative_scores=[]
polarity_scores=[]
subjectivity_scores=[]
for x in tokenized_words:
    p_score=0
    n_score=0
    for i in x:
        if i in p:
            p_score=p_score+1
        elif i in n:
            n_score=n_score+1
    pol_score=(p_score-n_score)/((p_score+n_score)+0.000001)
    sub_score=(p_score+n_score)/((len(x))+0.000001)
    positive_scores.append(p_score)
    negative_scores.append(n_score)
    polarity_scores.append(pol_score)
    subjectivity_scores.append(sub_score)


# In[26]:


scores_lists=[positive_scores,negative_scores,polarity_scores,subjectivity_scores]


# In[27]:


for i in scores_lists:
    print(len(i))


# In[28]:


scores=['positive_scores','negative_scores','polarity_scores','subjectivity_scores']
a=0
for i in scores_lists:
    print(scores[a])
    print(len(i))
    print(i)
    a=a+1


# # Step 5.2:Calculating word counts and sentence counts in all articles and adding them to a list

# In[29]:


word_counts=[]
sentence_counts=[]
for i in tokenized_words:
    count=len(i)
    word_counts.append(count)
for i in tokenized_sentences:
    count=len(i)
    sentence_counts.append(count)


# In[30]:


print(len(word_counts))
print(word_counts)


# In[31]:


print(len(sentence_counts))
print(sentence_counts)


# # Step 5.3: Calculating average sentence lenghts for each article and adding them to a list

# In[32]:


count_list=list(zip(word_counts,sentence_counts))


# In[33]:


average_sentence_lengths=[]
for i,v in count_list:
    avg_sent_len=i/v
    average_sentence_lengths.append(avg_sent_len)


# In[34]:


print(len(average_sentence_lengths))
print(average_sentence_lengths)


# # Step 5.4: Calculating the total syllable and complex word counts in each article and adding them to respective lists

# In[35]:


vowels=['a','e','i','o','u']


# In[36]:


a=0
syllable_counts=[]
complex_word_counts=[]
while a in range(170):
    complex_words=[]
    word_syllables=[]
    for i in tokenized_words[a]:
        count=0
        for v in i:
            if v in vowels:
                count=count+1
            word_syllables.append(count)
        if count>2:
            complex_words.append(1)
        total_syllable_count=sum(word_syllables)
        total_complex_count=sum(complex_words)
    syllable_counts.append(total_syllable_count)
    complex_word_counts.append(total_complex_count)
    a=a+1


# In[37]:


print(len(syllable_counts))
print(syllable_counts)


# In[38]:


print(len(complex_word_counts))
print(complex_word_counts)


# # Step 5.5:Calculating complex word percentages of all articles and adding them to a list

# In[39]:


i=0
complex_words_percents=[]
while i in range(170):
    percent=complex_word_counts[i]/len(tokenized_words[i])
    complex_words_percents.append(percent)
    i=i+1    


# In[40]:


print(len(complex_words_percents))
print(complex_words_percents)


# # Step 5.6:Calculating the fog indices of all articles and adding them to a list

# In[41]:


i=0
fog_indices=[]
while i in range(170):
    fog_index=0.4*(average_sentence_lengths[i]+complex_words_percents[i])
    fog_indices.append(fog_index)
    i=i+1


# In[42]:


print(len(fog_indices))
print(fog_indices)


# # Step 5.7: Calculating average word lenghts in all articles and adding them to a list

# In[43]:


a=0
total_character_counts=[]
while a in range(170):
    character_counts=[]
    for i in tokenized_words[a]:
        character_counts.append(len(i))
    total=sum(character_counts)
    total_character_counts.append(total)
    a=a+1   


# In[44]:


average_word_lengths=[]
a=0
while a in range(170):
    avg_word_len=(total_character_counts[a]/len(tokenized_words[a]))
    average_word_lengths.append(avg_word_len)
    a=a+1


# In[45]:


print(len(average_word_lengths))
print(average_word_lengths)


# # Step 5.8: Counting the personal pronouns in each article and adding them to a list

# In[46]:


personal_pronouns=['i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them ']


# In[47]:


personal_pronoun_counts=[]
a=0
while a in range(170):
    count=0
    for i in tokenized_words[a]:
        if i in personal_pronouns:
            count=count+1
    personal_pronoun_counts.append(count)
    a=a+1           


# In[48]:


print(len(personal_pronoun_counts))
print(personal_pronoun_counts)


# # Step 5.9: Calculating syllable per word in each article and adding them to a list

# In[49]:


syllable_per_word=[]
a=0
while a in range(170):
    avg_syllable_no=(syllable_counts[a]/len(tokenized_words[a]))
    syllable_per_word.append(avg_syllable_no)
    a=a+1


# In[50]:


print(len(syllable_per_word))
print(syllable_per_word)


# # Step 6: Creating the output dataframe using pandas and saving it as an excel sheet

# In[51]:


details={'URL_ID':list(data['URL_ID']),
         'URL':list(data['URL']),
         'POSITIVE SCORE':positive_scores,
         'NEGATIVE SCORE':negative_scores,
         'POLARITY SCORE':polarity_scores,
         'SUBJECTIVITY SCORE':subjectivity_scores,
         'AVG SENTENCE LENGTH':average_sentence_lengths,
         'PERCENTAGE OF COMPLEX WORDS':complex_words_percents,
         'FOG INDEX':fog_indices,
         'AVG NUMBER OF WORDS PER SENTENCE':average_sentence_lengths,
         'COMPLEX WORD COUNT':complex_word_counts,
         'WORD COUNT':word_counts,
         'SYLLABLE PER WORD':syllable_per_word,
         'PERSONAL PRONOUNS':personal_pronoun_counts,
         'AVG WORD LENGTH':average_word_lengths
        }


# In[52]:


output=pd.DataFrame(details)


# In[53]:


output


# In[54]:


output.to_excel('Output Data Structure.xlsx')

