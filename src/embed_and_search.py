import json
import faiss
import numpy as np
import re
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load FAQs
with open("data/faqs.json", "r", encoding="utf-8") as f:
    faqs = json.load(f)

# Combine question + answer
texts = []
for faq in faqs:
    combined = faq["question"] + " " + faq["answer"]
    texts.append(combined)

# Generate embeddings
embeddings = model.encode(texts)

# Create FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

print(f"✅ Indexed {len(texts)} FAQs")

# ---- TEST SEARCH ----
def search(query, k=5, threshold=1.2):
    q = query.lower()

    # better normalization
    q = re.sub(r'[^\w\s]', ' ', q)
    q = re.sub(r'\s+', ' ', q)

    query_vec = model.encode([q])
    distances, indices = index.search(np.array(query_vec), k)

    results = []

    for dist, idx in zip(distances[0], indices[0]):
        if dist < threshold:
            results.append({
                "faq": faqs[idx],
                "score": float(dist)
            })

    return results

if __name__ == "__main__":
    print("This file is only a module. Run chatbot.py instead.")
# ---- CLI TEST LOOP ----
'''while True:
    user_query = input("\nAsk a question (or 'exit'): ")
    if user_query.lower() == "exit":
        break

    results = search(user_query)

    if not results:
        print("\nNo reliable answer found in FAQs.")
        continue

    print("\nTop Matches:")
    for r in results:
        print(f"- {r['faq']['question']} (score: {r['score']:.4f})")
        '''