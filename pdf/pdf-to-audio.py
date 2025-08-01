import os
import pyttsx3
import PyPDF2


def extract_text_from_pdf(pdf_path: str) -> str:
    if not os.path.isfile(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    text = []
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text.append(content)
    return "\n".join(text)


def convert_text_to_audio(text: str, output_path: str) -> None:
    if not text.strip():
        raise ValueError("No text found to convert to audio.")

    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()


def main() -> None:
    pdf_file = "sample-file.pdf"
    audio_file = "sample-file.mp3"

    try:
        print(f"Reading from: {pdf_file}")
        text = extract_text_from_pdf(pdf_file)

        print(f"Converting to audio: {audio_file}")
        convert_text_to_audio(text, audio_file)

        print("Conversion completed successfully.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
