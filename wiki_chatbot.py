import wikipedia

def fetch_summary(query, lang="en"):
    """
    Gets a summary from Wikipedia for a given query.
    """
    try:
        wikipedia.set_lang(lang)
        summary = wikipedia.summary(query, sentences=3)
        return summary
    except wikipedia.exceptions.DisambiguationError as e:
        return f"⚠️ That topic is ambiguous. Try being more specific.\nOptions: {e.options[:5]}"
    except wikipedia.exceptions.PageError:
        return "❌ Sorry, that topic doesn't exist on Wikipedia."
    except Exception as e:
        return f"❗ An unexpected error occurred: {str(e)}"

























# Main loop
'''if __name__ == "__main__":
    print("🌐 Wikipedia Chatbot (type 'exit' to quit)")
    while True:
        user_input = input("\n🔎 What would you like to know about? ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        result = fetch_summary(user_input)
        print(f"\n📘 Result:\n{result}")'''
