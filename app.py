import os
import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

def extract_text_from_pdf(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def main():
    # SET PAGE CONFIG LAYOUT WIDE
    st.set_page_config(layout="wide")

    # (Opsional) Menampilkan logo di sidebar
    # Jika tidak ada file "logo-jago.png", komentar baris di bawah:
    st.sidebar.image("logo-jago.png")

    st.title("Generative AI - Audit Tools")

    uploaded_pdfs = st.sidebar.file_uploader(
        "Upload dokumen PDF (multi-upload):",
        type=["pdf"],
        accept_multiple_files=True
    )

    # Prompt default di text area
    default_instruction = (
        "Lakukan analisis mendalam terhadap dokumen SOP dan Instruksi Kerja. "
        "Identifikasi dan ekstrak informasi berikut untuk kebutuhan inventarisasi:\n\n"
        "1) Identifikasi Proses & Aktivitas\n"
        "2) Kontrol\n"
        "3) Risiko\n"
        "4) Dokumen dan Data\n"
        "5) Proses Dependensi\n"
        "6) Aplikasi Pendukung\n"
        "7) ICOFR\n\n"
        "Format Tabel: (No, Proses/Aktivitas, Deskripsi, Kontrol, Risiko, "
        "Dokumen & Data, Proses Dependensi, Aplikasi Pendukung, ICOFR)."
    )

    user_instruction = st.text_area(
        "Prompt Instruksi",
        value=default_instruction,
        height=450
    )

    if st.button("Proccess LLM"):
        # Cek apakah ada PDF yang di-upload
        if not uploaded_pdfs:
            st.error("Silakan upload minimal satu file PDF di sidebar.")
            return

        # Ambil API Key dari environment variable (AMAN)
        api_key = os.getenv("GENAI_API_KEY")
        if not api_key:
            st.error("API Key tidak tersedia. Pastikan environment variable GENAI_API_KEY sudah diset.")
            return

        # Konfigurasi ke Google Generative AI
        genai.configure(api_key=api_key)

        # Gabungkan teks dari semua PDF
        all_pdf_text = ""
        for i, pdf_file in enumerate(uploaded_pdfs, start=1):
            try:
                pdf_text = extract_text_from_pdf(pdf_file)
                all_pdf_text += f"\nfilename {i}: {pdf_file.name}\n{pdf_text}\n"
            except Exception as e:
                st.error(f"Gagal membaca {pdf_file.name}: {e}")

        # Susun prompt final
        final_prompt = f"""
Berikut adalah dokumen yang diunggah user:

{all_pdf_text}

---

# Instruksi dari User:
{user_instruction}
"""

        with st.spinner("Memproses prompt..."):
            try:
                generation_config = {'temperature': 0}
                # Contoh model "gemini-1.5-pro-latest" (sesuaikan jika perlu)
                model = genai.GenerativeModel("gemini-1.5-pro-latest")
                response = model.generate_content(
                    final_prompt,
                    generation_config=generation_config
                )

                # Tampilkan hasil di layar
                st.subheader("Hasil Generasi:")
                result_text = response.text
                st.markdown(result_text)

                # Tombol Download hasil dalam format .md
                st.download_button(
                    label="Download Hasil (.md)",
                    data=result_text,
                    file_name="gemini_result.md",
                    mime="text/markdown"
                )
            except Exception as e:
                st.error(f"Terjadi error saat memproses prompt: {e}")

if __name__ == "__main__":
    main()
