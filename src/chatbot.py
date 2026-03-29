from llama_cpp import Llama
import re
from embed_and_search import search
from spell_corrector import correct_text

import json
with open("data/smalltalk.json", "r", encoding="utf-8") as f:
    SMALLTALK_DATA = json.load(f)

# Load Qwen model
llm = Llama(
    model_path="models/qwen.gguf",
    n_ctx=2048,
    n_threads=6
)

# -------------------------
# CONFIG
# -------------------------
TOP_K_THRESHOLD = 1.0


# -------------------------
# SAFE NORMALIZATION (NO WORD BREAKING)
# -------------------------
def normalize(text):
    text = text.lower().strip()

    # remove extra punctuation
    text = re.sub(r'[^\w\s]', ' ', text)

    # collapse spaces
    text = re.sub(r'\s+', ' ', text)

    return text


# -------------------------
# PROMPT
# -------------------------
def build_prompt(query, contexts):
    context_text = "\n\n".join(
        [f"{c['faq']['answer']}" for c in contexts]
    )

    return f"""
    You are a STRICT NUST FAQ assistant.

    INSTRUCTIONS:
    - Answer ONLY using the information given below.
    - Keep the answer SHORT (max 2–3 sentences).
    - Do NOT repeat information.
    - Do NOT add explanations, notes, or commentary.
    - Do NOT say "based on context" or anything meta.
    - If multiple points exist → combine cleanly.
    - If answer not clearly present → say:
        I don't know based on the available FAQs.
    - Answer like a helpful university assistant (clear and direct).

    FAQ INFORMATION:
    {context_text}

    Question: {query}

    Answer:
    """

# -------------------------
# RELEVANCE CHECK
# -------------------------
def is_relevant(results):
    if not results:
        return False

    # accept if ANY of top results is good
    for r in results[:3]:
        if r["score"] < TOP_K_THRESHOLD:
            return True

    return False


# -------------------------
# CLEAN OUTPUT
# -------------------------
def clean_output(text):
    text = text.strip().split("\n\n\n")[0]
    cut_markers = [
        "Q:","Question: ","Answer: ", "Q &", "\nA:", "Note:", "Based on this",
        "Therefore,", "dialogue", "The user should",
        "For more information", "Please note",
        "Please visit:", "The user's question",  
        "whats", "The answer is:", "Final Answer:",
        "Question 0", "You should check", "I don't know based", "The user should", "You should check",
        "For more information", "Please note", "Please visit:",
        "The user's question", "Based on this", "Therefore,",
        "Q:", "Q &", "\nA:", "Note:", "dialogue", "whats"  ,"Answer Type","Therefore" ,"I don't know if",
"Based solely"        
    ]
    
    for marker in cut_markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx].strip()
    
    return " ".join(text.split()).strip(" \n\t.,;:")

# -------------------------
# SMALLTALK (FIXED PROPERLY)
# -------------------------
def handle_smalltalk(query):
    q = normalize(query)

    words = q.split()

    # Only allow short casual messages
    if len(words) > 6:
        return None

    for item in SMALLTALK_DATA:
        for phrase in item["inputs"]:
            phrase_norm = normalize(phrase)

            # exact match OR full phrase match
            if q == phrase_norm:
                return item["response"]

            if q.startswith(phrase_norm):
                return item["response"]

    return None


# -------------------------
# MULTI-QUESTION SPLIT
# -------------------------
def split_query(query):
    queries = [query.strip()]  # always include full query first

    # Split on '?' for multi-question strings
    q_parts = [p.strip() for p in query.split('?') if len(p.strip()) > 6]
    if len(q_parts) > 1:
        queries.extend(q_parts)

    # Split on 'and' only when both sides are substantial (5+ words each)
    for part in q_parts if q_parts else [query]:
        if ' and ' in part:
            sides = part.split(' and ', 1)
            if (len(sides[0].strip().split()) >= 3 and 
                len(sides[1].strip().split()) >= 3):
                queries.extend([s.strip() for s in sides])

    # Deduplicate while preserving order
    seen = set()
    return [q for q in queries if not (q in seen or seen.add(q))]

# -------------------------
# MAIN FUNCTION
# -------------------------
def ask_bot(query):

    # STEP 1: smalltalk
    smalltalk = handle_smalltalk(query)
    if smalltalk:
        return smalltalk

    # ✅ STEP 2: spell correction
    corrected_query = correct_text(query)

    # DEBUG (optional)
    # print("Corrected:", corrected_query)

    # STEP 3: normalize AFTER correction
    query = normalize(corrected_query)

    # STEP 4: split
    queries = split_query(query)

    answers = []

    for q in queries:
        results = search(q)

        if not is_relevant(results):
            continue

        results = results[:3]  # top 3 only

        prompt = build_prompt(q, results)

        output = llm(
            prompt,
            max_tokens=220,
            temperature=0.0,
            top_p=0.7,
            repeat_penalty=1.4,
            stop=[
                "User Question:", "FAQ CONTEXT:",
                "\nQ:", "Q & A:", "Q &", "\nA:",
                "Question 0", "Based on this",
                "Therefore,", "Answer 3", "dialogue",
                "Note:", "The user should",
                "For more information",
                "Please note", "whats"
            ]
        )

        ans = clean_output(output["choices"][0]["text"])

        # basic validity checks
        if not ans or len(ans) < 8:
            continue
        if ans.startswith("The user") or ans.startswith("This question"): 
            continue
        # final add
        if ans not in answers:
            answers.append(ans)

    if not answers:
        return (
            "I couldn't find that in the NUST FAQs. "
            "For further help, contact the Admissions Directorate:\n"
            "📞 Phone: +92 51-90856878\n"
            "📧 Email: ugadmissions@nust.edu.pk"
        )

    return " ".join(answers)


# -------------------------
# CLI
# -------------------------
if __name__ == "__main__":
    print("NUST FAQ Chatbot (STABLE RAG MODE)")
    print("Type 'exit' to quit\n")

    while True:
        q = input("You: ")
        if q.lower() == "exit":
            break

        answer = ask_bot(q)
        print("\nBot:", answer, "\n")