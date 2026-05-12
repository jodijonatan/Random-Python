"""
AI Sederhana menggunakan Google Gemini API
Instalasi: pip install google-generativeai
Jalankan: python ai_sederhana.py
"""

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Konfigurasi API Key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Inisialisasi model
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction="Kamu adalah asisten AI yang helpful, ramah, dan selalu menjawab dalam Bahasa Indonesia."
)

# Memulai sesi chat untuk manajemen riwayat otomatis
chat_session = model.start_chat(history=[])

def chat(user_message: str) -> str:
    """Kirim pesan ke Gemini dan dapatkan balasan."""
    response = chat_session.send_message(user_message)
    return response.text

def main():
    print("=" * 50)
    print("   AI Sederhana - Powered by Gemini")
    print("=" * 50)
    print("Ketik 'keluar' atau 'exit' untuk berhenti.")
    print("Ketik 'reset' untuk menghapus riwayat percakapan.")
    print("-" * 50)
    
    while True:
        user_input = input("\nKamu: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() in ["keluar", "exit", "quit"]:
            print("\nSampai jumpa! 👋")
            break
        
        if user_input.lower() == "reset":
            # Reset sesi chat
            global chat_session
            chat_session = model.start_chat(history=[])
            print("✅ Riwayat percakapan telah dihapus.")
            continue
        
        print("\nAI: ", end="", flush=True)
        try:
            response_text = chat(user_input)
            print(response_text)
        except Exception as e:
            # Penanganan error generik untuk API Google
            if "API_KEY_INVALID" in str(e):
                print("❌ API key tidak valid.")
                break
            else:
                print(f"❌ Terjadi kesalahan: {e}")

if __name__ == "__main__":
    main()