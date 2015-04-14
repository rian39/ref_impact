import pandas as pd
import json
import gensim
import nltk
from nltk.corpus import stopwords
f = open('data/DownloadAllJSON')
s = f.read()
j = json.loads(s)
df = pd.DataFrame(j['DownloadAllJSONResult'])
all = df.Title + df.ImpactSummary + df.ImpactDetails
all_clean = all.map(nltk.clean_html).str.lower()
all_texts = all_clean.tolist()
stoplist = set('for a of the and to in'.split())
stop = stopwords.words('english')
stop.append('research')
stop.append('impact')
stemmer = nltk.stem.PorterStemmer()
texts = [[stemmer.stem(word) for word in
          text.split() if word not in stop] for text in all_texts]
dictionary = gensim.corpora.Dictionary(texts)
dictionary.save('data/all_texts.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
model = gensim.models.ldamodel.LdaModel(corpus,
                                        id2word=dictionary, num_topics=65)
model.print_topic(1)
model.print_topics(10)
