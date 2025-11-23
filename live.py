# live.py
import os
import google.generativeai as genai

# --- Configuration ---
# Netlify will inject your API key from the environment variables.
# os.environ.get() is the standard way to securely access secrets in production.
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    # Use the key you provided for local testing only
    print("Warning: GEMINI_API_KEY environment variable not found. Using hardcoded key for local testing.")
    # NOTE: In a real app, do NOT commit this key.
    GEMINI_API_KEY = "AIzaSyDL3i0fCKkSnxnTG4-FLvfUxudtD4rKlos"

# --- Gemini Logic ---
def generate_and_save_site():
    """Connects to Gemini, generates a poem, and saves it to an HTML file."""
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-pro')

        # The prompt asks the model to generate the final HTML structure.
        prompt = (
            "Write a complete, single-page HTML document. "
            "The content should be a short, uplifting poem about Python and open-source code. "
            "Use modern CSS for a clean, centered design with a dark background."
        )

        print("Generating site content with Gemini 2.5 Pro...")
        
        response = model.generate_content(prompt)
        html_content = response.text

        # Netlify needs the output to be in the designated build folder.
        # We will configure Netlify to use a 'dist' folder.
        output_path = "dist/index.html"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        print(f"✅ Successfully generated site and saved to {output_path}")

    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        # In case of an error, write a simple error page
        with open("dist/index.html", "w") as f:
            f.write(f"<h1>Deployment Error</h1><p>Failed to generate content: {e}</p>")

if __name__ == "__main__":
    generate_and_save_site()
y
