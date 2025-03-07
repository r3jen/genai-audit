import streamlit as st
from utils import PDFProcessor, MarkdownProcessor, GeminiAI

def main():
    st.set_page_config(layout="wide")
    st.sidebar.image("logo-jago.png")
    st.title("Generative AI - Audit Tools")

    uploaded_pdfs = st.sidebar.file_uploader(
        "Upload dokumen PDF (multi-upload):",
        type=["pdf"],
        accept_multiple_files=True
    )

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

    user_instruction = st.text_area("Prompt Instruksi", value=default_instruction, height=450)

    if st.button("Proccess LLM"):
        if not uploaded_pdfs:
            st.error("Silakan upload minimal satu file PDF di sidebar.")
            return

        all_pdf_text = ""
        for i, pdf_file in enumerate(uploaded_pdfs, start=1):
            try:
                pdf_text = PDFProcessor.extract_text(pdf_file)
                all_pdf_text += f"\nfilename {i}: {pdf_file.name}\n{pdf_text}\n"
            except Exception as e:
                st.error(f"Gagal membaca {pdf_file.name}: {e}")

        final_prompt = f"""
Berikut adalah dokumen yang diunggah user:

{all_pdf_text}

---

# Instruksi dari User:
{user_instruction}
"""

        with st.spinner("Memproses prompt..."):
            try:
                result_text = GeminiAI.generate_response(final_prompt)

                st.subheader("Hasil Generasi:")
                st.markdown(result_text)

                st.download_button(
                    label="Download Hasil (.md)",
                    data=result_text,
                    file_name="gemini_result.md",
                    mime="text/markdown"
                )

                csv_data = MarkdownProcessor.convert_md_to_csv(result_text)

                st.download_button(
                    label="Download Hasil (.csv)",
                    data=csv_data,
                    file_name="gemini_result.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Terjadi error saat memproses prompt: {e}")

if __name__ == "__main__":
    main()
