import os
import pandas as pd
import re
from io import StringIO
from PyPDF2 import PdfReader
import google.generativeai as genai

class PDFProcessor:
    """Handles PDF text extraction."""
    
    @staticmethod
    def extract_text(uploaded_file) -> str:
        reader = PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text

class MarkdownProcessor:
    """Handles Markdown parsing and conversion to structured format."""

    @staticmethod
    def extract_text_and_tables(md_content):
        lines = md_content.split("\n")
        tables = []
        texts = []
        current_table = []
        current_text = []

        for line in lines:
            if "|" in line:  # Likely a table row
                if current_text:
                    texts.append("\n".join(current_text).strip())
                    current_text = []
                current_table.append(line)
            else:  # Regular text
                if current_table:
                    tables.append(current_table)
                    current_table = []
                current_text.append(line)

        if current_table:
            tables.append(current_table)
        if current_text:
            texts.append("\n".join(current_text).strip())

        return texts, tables

    @staticmethod
    def convert_md_to_csv(md_content):
        texts, tables = MarkdownProcessor.extract_text_and_tables(md_content)
        combined_data = []

        for text in texts:
            combined_data.append([text])  # Add text as a single row

            # Check if there is a corresponding table
            if tables:
                table = tables.pop(0)
                table_io = StringIO("\n".join(table))
                df = pd.read_csv(table_io, sep="|", skipinitialspace=True).dropna(axis=1, how="all")

                # Remove any header separators (e.g., "---", "----")
                df = df[~df.iloc[:, 0].str.contains("---", na=False, regex=True)]

                # Clean column names
                df.columns = [col.strip() for col in df.columns]

                # Append table content row by row
                combined_data.append(df.columns.tolist())  # Add table headers
                combined_data.extend(df.values.tolist())   # Add table rows

        # Convert to DataFrame
        combined_df = pd.DataFrame(combined_data)

        # Convert DataFrame to CSV format
        csv_buffer = StringIO()
        combined_df.to_csv(csv_buffer, index=False, header=False)
        return csv_buffer.getvalue()

class GeminiAI:
    """Handles interaction with Google Generative AI (Gemini)."""

    API_KEY = os.getenv("GENAI_API_KEY")


    @staticmethod
    def generate_response(prompt):
        if not GeminiAI.API_KEY:
            raise ValueError("API Key tidak tersedia.")

        genai.configure(api_key=GeminiAI.API_KEY)
        generation_config = {'temperature': 0}
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text
