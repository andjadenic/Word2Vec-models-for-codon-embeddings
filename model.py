from gensim.models import Word2Vec


sentences = [
    ["king", "queen", "ruler", "country"],
    ["happy", "joy", "sad", "angry"],
    ["computer", "science", "data", "machine"],
]
model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)
model.train()

# Find similar words to "king"
similar_words = model.most_similar(positive=["king"], topn=3)
print("Words similar to 'king':", similar_words)

# Find analogy: king is to queen as father is to ?
#analogy_result = model.most_similar(positive=["king", "queen"], negative=["father"], topn=1)