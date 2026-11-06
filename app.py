import streamlit as st
from google import genai

# 1. Mengambil API Key (Format AQ) secara aman dari pengaturan Streamlit Secrets
if "GEMINI_API_KEY" in st.secrets:
    api_key_input = st.secrets["GEMINI_API_KEY"]
else:
    st.error("API Key belum terpasang di pengaturan Streamlit Secrets!")
    st.stop()

# 2. Menghubungkan ke Client Google GenAI SDK Terbaru v3.8+
try:
    client = genai.Client(api_key=api_key_input)
except Exception as e:
    st.error(f"Gagal terhubung ke Google AI Studio: {e}")
    st.stop()

# 3. Mengatur Tampilan Halaman Website suaix
st.set_page_config(page_title="suaix - Chat AI Pintar", page_icon="🤖", layout="centered")

st.title("🤖 suaix")
st.write("Selamat datang di **suaix**! Chat AI pintar versi terbaru yang ditenagai oleh Gemini 3.8 Flash. Siap membantu tugas sekolah, merangkum, atau mengobrol santai.")

# 4. Membuat Memori Obrolan (Chat History) agar AI ingat riwayat chat sebelumnya
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 5. Menampilkan riwayat chat yang sudah lewat ke layar website
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Kotak Input Chat utama tempat user mengetik pertanyaan
if user_input := st.chat_input("Tanya suaix di sini..."):
    
    # Tampilkan pesan user ke layar
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # 7. Memproses jawaban dengan model resmi Gemini 3.8 Flash
    with st.chat_message("assistant"):
        with st.spinner("suaix sedang berpikir..."):
            try:
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=user_input
                )
                jawaban = response.text
                
                # Tampilkan jawaban dari aplikasi suaix ke layar web
                st.markdown(jawaban)
                st.session_state.chat_history.append({"role": "assistant", "content": jawaban})
            except Exception as e:
                st.error(f"Waduh, suaix mengalami kendala teknis: {e}")
