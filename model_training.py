import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB

data = [
    ("Theft happened in the area", "Section 378 IPC"),
    ("Murder case registered", "Section 302 IPC"),
    ("Cybercrime fraud reported", "IT Act Section 66"),
]

texts, labels = zip(*data)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(texts)

model = MultinomialNB()
model.fit(X, labels)

with open("legal_nlp_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
