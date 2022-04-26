from cgi import test
from ipaddress import summarize_address_range
import feedparser
import json
import csv
import pandas as pd

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk.stem.lancaster import LancasterStemmer
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.naive_bayes import MultinomialNB

import string
from tqdm import tqdm


# #Known
# dataset1 = open('valid.csv',"r", newline='')
# reader1 = list(csv.reader(dataset1, delimiter=','))
# dataset2 = open('invalid.csv',"r", newline='')
# reader2 = list(csv.reader(dataset2, delimiter=','))
# #unknown
# dataset3 = open('mix.csv',"r", newline='')
# reader3 = list(csv.reader(dataset3, delimiter=','))



# for item in reader1:
#     print(item[2])

#known
dataset1 = pd.read_csv('valid.csv')
dataset2 = pd.read_csv('invalid.csv')

#unknown
dataset3 = pd.read_csv('mix.csv')


working_data = pd.concat([dataset1, dataset2]).reset_index(drop=True)
y = [1 for i in range(dataset1.shape[0])] + [0 for i in range(dataset2.shape[0])]
y = pd.Series(y)

def transform(set):
    return set["title"] + " " + set["summary"] 


working_data = working_data.apply(transform, axis=1)

test_data = dataset3.apply(transform, axis=1)



lemmatizer = WordNetLemmatizer()
stemmer = SnowballStemmer(language="english")
stemmer2 = PorterStemmer()
stemmer3 = LancasterStemmer()
stop_words = set(stopwords.words('english'))
vectorizer = CountVectorizer()


def process(text):
    for p in string.punctuation:
        text = text.replace(p, '')
    text = text.lower()
    text = word_tokenize(text)
    text = [w for w in text if not w in stop_words] #optional
    text = [stemmer.stem(word) for word in text]
    return text


number_of_samples = working_data.shape[0]

for i in tqdm(range(number_of_samples)):
    working_data[i] = process(working_data[i])


for i in tqdm(range(number_of_samples)):
    working_data[i] = " ".join(working_data[i])



#for unlabeled data
for i in tqdm(range(test_data.shape[0])):
    test_data[i] = process(test_data[i])
for i in tqdm(range(test_data.shape[0])):
    test_data[i] = " ".join(test_data[i])

vectorizer_test = TfidfVectorizer(max_features=5000)
test_data = vectorizer_test.fit_transform(test_data).toarray()
features__test_data = vectorizer_test.get_feature_names_out()
test_data = pd.DataFrame(test_data, columns=features__test_data)

#for labeled data
vectorizer = CountVectorizer(max_features=features__test_data.shape[0])
bow_data = vectorizer.fit_transform(working_data).toarray()
features = vectorizer.get_feature_names_out()
bow_data = pd.DataFrame(bow_data, columns=features)

vectorizer = TfidfVectorizer(max_features=features__test_data.shape[0])
tfidf_data = vectorizer.fit_transform(working_data).toarray()
features = vectorizer.get_feature_names_out()
tfidf_data = pd.DataFrame(tfidf_data, columns=features)

nb = MultinomialNB()


def train_and_evaluate(x, y):
    xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)
    nb.fit(xtrain, ytrain)
    ypred_tr = nb.predict(xtrain)
    ypred_ts = nb.predict(xtest)
    print("Training Results:\n")
    print(classification_report(ytrain, ypred_tr))
    print("\n\nTesting Results:\n")
    print(classification_report(ytest, ypred_ts))


#train_and_evaluate(bow_data, y)


#train_and_evaluate(tfidf_data, y)

nb.fit(tfidf_data, y)




#Verified set
verifyed_news = open('verifyed.csv',"w", newline='')
writer4 = csv.writer(verifyed_news, delimiter=',')
#needs human verification
unverifyed_news = open('unverifyed.csv',"a", newline='')
writer5 = csv.writer(unverifyed_news, delimiter=',')

# print(test_data)
verified_set = nb.predict(test_data)
print(verified_set)
for i in range(test_data.shape[0]):
    if verified_set[i] == 1:
        writer4.writerow(dataset3.iloc[i])
    else:
        writer5.writerow(dataset3.iloc[i])


