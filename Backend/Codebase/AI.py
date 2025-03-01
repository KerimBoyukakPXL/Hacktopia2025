import streamlit as st
import requests
import json
from collections import defaultdict

LOCAL_JSON_FILE = "data.json"
OLLAMA_ENDPOINT = "http://127.0.0.1:11434"

def load_data_locally():
    """
    Load local JSON data and create a combined list with indexing.
    """
    try:
        with open(LOCAL_JSON_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        st.error(f"Error loading {LOCAL_JSON_FILE}: {e}")
        return [], {}

    combined = []
    if isinstance(data, dict):
        for url, content in data.items():
            headers = content.get("headers", [])
            paragraphs = content.get("paragraphs", [])
            for text in headers + paragraphs:
                if isinstance(text, str):  # Ensure the text is a string
                    combined.append({"text": text, "url": url})
    elif isinstance(data, list):
        combined = [{"text": item, "url": "Unknown"} for item in data if isinstance(item, str)]
    else:
        combined = []

    index = build_index(combined)
    return combined, index

def build_index(clean_data):
    """
    Build an index for fast searching within the JSON data.
    """
    index = defaultdict(list)
    for entry in clean_data:
        if "text" in entry:
            words = entry["text"].lower().split()
            for word in words:
                index[word].append(entry)
    return index

def fast_search(query, index):
    """
    Perform a fast search using the prebuilt index, with basic relevance scoring.
    """
    words = query.lower().split()
    results = defaultdict(int) 

    for word in words:
        for entry in index.get(word, []):
            results[(entry["text"], entry["url"])] += 1

    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    return [{"text": text, "url": url} for (text, url), score in sorted_results[:5]]

def call_llama_via_ollama(user_query, context_list):
    """
    Build a prompt and call the Llama model via Ollama.
    """
    context_block = "\n\n".join([f"- {ctx['text']} (Source: {ctx['url']})" for ctx in context_list])

    json_payload = {
        "model": "llama2:latest",
        "prompt": f"""
You are a volunteer for the Red Cross Netherlands. Answer factually, professionally, and concisely (max 3 sentences).
Never invent information and only use the provided context.

📌 **Context**:
{context_block}

❓ **Question**:
{user_query}

✅ **Answer**:
""",
        "stream": False
    }

    try:
        response = requests.post(
            f"{OLLAMA_ENDPOINT}/api/generate",
            json=json_payload,
            timeout=300
        )
        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()
    except Exception as e:
        return f"Error calling Llama: {str(e)}"

def main():
    st.title("🤖 HIA - Bot (HackTuah!)🔗")

    clean_data, index = load_data_locally()

    user_query = st.text_input("❓")
    if st.button("🔍"):
        context_matches = fast_search(user_query, index)

        answer = call_llama_via_ollama(user_query, context_matches)

        st.write("**✅**")
        st.write(answer)

        st.write("**🔗**")
        displayed_urls = set()
        for match in context_matches:
            if match['url'] not in displayed_urls:
                st.write(f"- {match['url']}")
                displayed_urls.add(match['url'])

if __name__ == "__main__":
    main()
