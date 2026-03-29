from symspellpy import SymSpell, Verbosity
import json
import os

# Initialize SymSpell
sym_spell = SymSpell(max_dictionary_edit_distance=3, prefix_length=7)

# -------------------------
# BUILD CUSTOM DICTIONARY
# -------------------------
def build_dictionary():

    words = set()

    # Load FAQ words
    with open("data/faqs.json", "r", encoding="utf-8") as f:
        faqs = json.load(f)

    for faq in faqs:
        text = (faq["question"] + " " + faq["answer"]).lower()
        for word in text.split():
            words.add(word)

    # Add important custom words manually
    custom_words = [

    # --- Institutions & Programmes ---
    "nust", "nshs", "nums", "pec", "ibcc", "pmdc",

    # --- Programmes & Degrees ---
    "mbbs", "bshnd", "bscs",
    "undergraduate", "ug",
    "engineering", "computing",
    "dietetics", "nutrition",

    # --- Tests & Exams ---
    "mdcat", "net", "act", "sat","sat-i", "sat-1",
    "mcqs", "mcq",
    "sat-ii","sat-2", "ucat", "mcat",

    # --- Admission Terms ---
    "quota", "merit", "eligibility",
    "equivalence", "migration",
    "expatriate", "overseas",
    "weightage", "installment",
    "enrollment", "tuition",
    "scholarship", "scholarships",
    "financial", "assistance",
    "processing", "refundable",
    "non-refundable", "deposit",
    "remedial", "deficient",
    "penalization", "repeater",

    # --- Qualifications ---
    "fsc", "hssc", "ssc",
    "matric", "intermediate",
    "ics", "dae",
    "olevel", "alevel",
    "equivalence",

    # --- Documents ---
    "cnic", "nicop", "poc",
    "passport", "equivalence",
    "ibcc",

    # --- Locations ---
    "islamabad", "rawalpindi",
    "quetta", "karachi", "gilgit",
    "balochistan",

    # --- Fee & Finance Terms ---
    "quarterly", "installments",
    "annually", "semester",
    "discount", "refund",
    "invoice", "1link", "easypaisa",
    "jazzcash",

    # --- Academic Terms ---
    "gpa", "credit", "semester",
    "programme", "programmes",
    "orientation", "hostel",
    "pick-and-drop",

    # --- Abbreviations expanded ---
    "pakistan", "pakistani",
    "nationality", "dual",
    "international", "national",
    "foreign",

    # --- Regulatory Bodies ---
    "bise", "bises", "college",
    "board",

    # --- Common FAQ Slang / Queries users type ---
    "fee", "fees", "structure",
    "seats", "admission", "admissions",
    "apply", "application",
    "result", "results",
    "hostel", "transport",
    "faqs", "contact",
    ]

    words.update(custom_words)

    # Save temporary dictionary file
    with open("data/dictionary.txt", "w", encoding="utf-8") as f:
        high_priority = {
            "nust", "mbbs", "mdcat", "net", "act", "sat", "nums",
            "nshs", "seats", "reserved", "quota", "admission",
            "admissions", "syllabus", "tuition", "installment",
            "scholarship", "hostel", "equivalence", "migration",
            "eligibility", "fee", "fees", "schedule", "criteria",
            "merit", "programme", "programmes"
        }
        for w in words:
            freq = 1000 if w in high_priority else 10
            f.write(f"{w} {freq}\n")


# -------------------------
# LOAD DICTIONARY
# -------------------------
def load_dictionary():
    dict_path = "data/dictionary.txt"

    if not os.path.exists(dict_path):
        build_dictionary()

    sym_spell.load_dictionary(dict_path, term_index=0, count_index=1)


# -------------------------
# SPELL CORRECTION FUNCTION
# -------------------------
def correct_text(text):
    words = text.split()
    corrected = []
    for word in words:
        suggestions = sym_spell.lookup(
            word,
            Verbosity.CLOSEST,
            max_edit_distance=3
        )
        if suggestions:
            corrected.append(suggestions[0].term)
        else:
            corrected.append(word)  # keep original if no match
    return " ".join(corrected)


# Initialize ON IMPORT
load_dictionary()