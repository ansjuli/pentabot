from difflib import get_close_matches
import os

def normalize(text):
    return text.lower().replace("-", " ").replace("_", " ").strip()

def find_best_match(query, files):
    if not files:
        return None

    query = normalize(query)

    names = [normalize(os.path.basename(f)) for f in files]

    matches = get_close_matches(query, names, n=1, cutoff=0.5)

    if matches:
        index = names.index(matches[0])
        return files[index]

    return None