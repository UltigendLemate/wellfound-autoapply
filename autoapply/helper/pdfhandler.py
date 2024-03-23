import PyPDF2

class PDFHandler:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_links(self):
        links = []
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                if '/Annots' in page:
                    annotations = page['/Annots']
                    for annotation in annotations:
                        annotation_object = annotation.get_object()
                        if annotation_object.get('/Subtype') == '/Link':
                            uri = None
                            if '/A' in annotation_object:
                                if '/URI' in annotation_object['/A']:
                                    uri = annotation_object['/A']['/URI']
                            if uri:
                                links.append(uri)
        return links

    def extract_text(self):
        text = ""
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                text += page.extract_text()
        return text
