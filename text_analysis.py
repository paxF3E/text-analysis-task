import os
import re
import nltk
from nltk import word_tokenize
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

swf = os.listdir('StopWords/')
stopwords = []
for sw in swf:
    swfloc = 'StopWords/' + sw
    with open(swfloc, 'r') as f:
        stopwords.extend(f.read().split('\n'))
    f.close()

def count_complex(doc):
    count = 0
    totalsyllable = 0
    vowels = ['a', 'e', 'i', 'o', 'u']
    for word in doc:
        syllable = 0
        if any(vowel in word.lower() for vowel in vowels): syllable += 1
        if syllable > 2:
            count += 1
        totalsyllable += syllable
    return count, totalsyllable
    
POSITIVE = 1
NEGATIVE = -1

outf = open('Output.csv', 'a')
outf.writelines("URL_ID,URL,POSITIVE SCORE,NEGATIVE SCORE,POLARITY SCORE,SUBJECTIVITY SCORE,AVG SENTENCE LENGTH,PERCENTAGE OF COMPLEX WORDS,FOG INDEX,AVG NUMBER OF WORDS PER SENTENCE,COMPLEX WORD COUNT,WORD COUNT,SYLLABLE PER WORD,PERSONAL PRONOUNS,AVG WORD LENGTH\n")

docs = os.listdir('Input/')
for doc in docs:
    floc = 'Input/'+ doc
    with open(floc, 'r') as f:
        fcontent = f.read()
    f.close()

    ## tokenization and lemmatization
    tokens = nltk.word_tokenize(fcontent)
    lemmas = [lemmatizer.lemmatize(tok) for tok in tokens]
    filtered_lemmas = [lemma for lemma in lemmas if not lemma in stopwords]
    # print(f"percent stopwords found: {round(((len(lemmas)-len(filtered_lemmas))/len(lemmas))*100)}%")


    ## sentiment analysis
    pscore = 0; nscore = 0
    fpos = open('MasterDictionary/positive-words.txt').read().split('\n') 
    fneg = open('MasterDictionary/negative-words.txt').read().split('\n')
    for flem in filtered_lemmas:
        if flem in fpos: pscore += POSITIVE
        elif flem in fneg: nscore += NEGATIVE
    nscore *= -1 

    # measures computation
    polarity = (pscore - nscore)/((pscore + nscore) + 0.000001)
    subjectivity = (pscore + nscore)/(len(filtered_lemmas) + 0.000001)

    totalwordcount = len(fcontent.split())
    totalsentencecount = len(nltk.sent_tokenize(fcontent))
    avg_sentence_len = totalwordcount / totalsentencecount
    avgword_per_sent = totalwordcount / totalsentencecount

    complexwordcount, _ = count_complex(lemmas)
    percentcomplex = (complexwordcount / totalwordcount) * 100

    fog_index = 0.4 * (avg_sentence_len + percentcomplex)
    wordcount = len(filtered_lemmas)

    _, totalsyllablecount = count_complex(lemmas)
    syllable_per_word = totalsyllablecount / len(lemmas)
    
    ppronouns = ['I', 'We', 'My', 'Ours', 'Us', 'we', 'my', 'ours', 'us']
    ppronoun_count = len(re.findall(r'|'.join(ppronouns), fcontent))

    avg_word_len = len(fcontent.replace("\n", '').replace("\t", '').replace(" ", '')) / totalwordcount
    # print(f'{pscore}  {nscore}  {polarity}  {subjectivity}  {avg_sentence_len}  {percentcomplex}  {fog_index}  {avgword_per_sent}  {complexwordcount}  {wordcount}  {syllable_per_word}  {ppronoun_count}  {avg_word_len}')


    ## writing ready
    inp_list = open('Input.csv', 'r').readlines()
    for line in inp_list:
        if re.findall(''.join(doc.split('.')[0]), line):
            line2write = line[:-1]
            break
    line2write += f",{pscore},{nscore},{polarity},{subjectivity},{avg_sentence_len},{percentcomplex},{fog_index},{avgword_per_sent},{complexwordcount},{wordcount},{syllable_per_word},{ppronoun_count},{avg_word_len}\n"
    outf.writelines(line2write)

    print(f"output written to Output.csv for article #{doc.split('.')[0]}")

outf.close()
