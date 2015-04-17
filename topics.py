import pandas as pd
import gensim

//topic model analysis
all = df.Title + df.ImpactSummary + df.ImpactDetails
all_clean = all.map(html_strip).str.lower()
all_texts = all_clean.tolist()

stop = stopwords.words('english')
stop.append('research')
stop.append('impact')
stop.append('also')
stop.append('new')
stemmer = nltk.stem.PorterStemmer()
texts = [[stemmer.stem(word) for word in
          text.split() if word not in stop] for text in all_texts]
dictionary = gensim.corpora.Dictionary(texts)
dictionary.save('data/all_texts.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
model = gensim.models.ldamodel.LdaModel(corpus,
                                        id2word=dictionary, num_topics=65)
model2 = gensim.models.LdaMulticore(corpus, id2word = dictionary, num_topics = 40)

model.print_topic(1)
model.print_topics(10)

//topic model analysis
all = df.Title + df.ImpactSummary + df.ImpactDetails
all_clean = all.map(html_strip).str.lower()
all_texts = all_clean.tolist()

stop = stopwords.words('english')
stop.append('research')
stop.append('impact')
stop.append('also')
stop.append('new')
stemmer = nltk.stem.PorterStemmer()
texts = [[stemmer.stem(word) for word in
          text.split() if word not in stop] for text in all_texts]
dictionary = gensim.corpora.Dictionary(texts)
dictionary.save('data/all_texts.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
model = gensim.models.ldamodel.LdaModel(corpus,
                                        id2word=dictionary, num_topics=65)
model2 = gensim.models.LdaMulticore(corpus, id2word = dictionary, num_topics = 40)

model.print_topic(1)
model.print_topics(10)
