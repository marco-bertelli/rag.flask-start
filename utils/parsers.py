from llama_index.schema import Document
from llmsherpa.readers import LayoutPDFReader

import pandas as pd

llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"


def parse_source_item(item):
    documents = []

    if item['type'] == 'csv':
        data = pd.read_csv(item['path'])

        questions = data[data.columns[0]].tolist()
        answers = data[data.columns[1]].tolist()

        for index, question in enumerate(questions):
            text = question + " " + answers[index]

            documents.append(Document(text=text, id_=f"{item['_id']}_{index}"))

    if item['type'] == 'pdf':
        pdf_reader = LayoutPDFReader(llmsherpa_api_url)

        doc = pdf_reader.read_pdf(item['path'])

        for index, chunk in enumerate(doc.chunks()):
            documents.append(Document(text=chunk.to_context_text(), id_=f"{item['_id']}_{index}"))

    if item['type'] == 'qa':
        text = item['question'] + " " + item['answer']

        documents.append(Document(text=text, id_=f"{item['_id']}"))

    return documents


def parse_items_to_delete(item):
    documents_to_delete = []

    if item['type'] == 'csv':
        data = pd.read_csv(item['path'])

        questions = data[data.columns[0]].tolist()

        for index in enumerate(questions):
            documents_to_delete.append(f"{item['_id']}_{index}")

    if item['type'] == 'pdf':
        pdf_reader = LayoutPDFReader(llmsherpa_api_url)
    
        doc = pdf_reader.read_pdf(item['path'])

        for index in enumerate(doc.chunks()):
            documents_to_delete.append(f"{item['_id']}_{index}")

    if item['type'] == 'qa':
        documents_to_delete.append(f"{item['_id']}")

    return documents_to_delete
