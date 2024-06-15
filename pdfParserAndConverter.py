import fitz
import nltk
nltk.download('punkt')

file_path = 'Инструкция D-1C1-1.10.39 Сверка взаиморасчетов с контрагентами.pdf'

def extract_text_from_pdf(file_path):
    text = ''
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text += page.get_text()

    return text

pdf_text = extract_text_from_pdf(file_path)

# Токенизация текста на абзацы с использованием NLTK
paragraphs = nltk.sent_tokenize(pdf_text)

document_name = "Сверка взаиморасчетов с контрагентами"
source = "https://docs.yandex.ru/docs/view?url=ya-disk-public%3A%2F%2FlNlYrbYuvsFdjP11D1wNTUumD9YGmlrdn8D3k5YQ2t2nCLSr6y31er5%2FDQo3fJj4q%2FJ6bpmRyOJonT3VoXnDag%3D%3D%3A%2FИнструкция%20D-1C1-1.10.39%20Сверка%20взаиморасчетов%20с%20контрагентами.pdf&name=Инструкция%20D-1C1-1.10.39%20Сверка%20взаиморасчетов%20с%20контрагентами.pdf&nosw=1"
with (open('file-test.csv', 'a', encoding='utf-8') as f):
    for i, paragraph in enumerate(paragraphs):
        without_quotes = paragraph.replace('"', '«')
        f.write("\"" + document_name + "\",")
        f.write("\"" + source + "\",")
        f.write('"' + without_quotes + '"' + '\n')
