from document import Document
from server import DocumentAPI

# Mock data (replace with actual data loading from CSV)
documents = [
    Document(1, "Document 1", "pdf", "portrait", "NEEDS_REVIEW", "This is the text representation of Document 1."),
    Document(2, "Document 2", "docx", "landscape", "NEEDS_REVIEW", "This is the text representation of Document 2."),
    Document(3, "Document 3", "pdf", "portrait", "REVIEWED", "This is the text representation of Document 3."),
    Document(4, "Document 3", "pdf", "portrait", "REVIEWED", "This is the text representation of Document 3."),
    Document(5, "Document 3", "pdf", "portrait", "REVIEWED", "This is the text representation of Document 3."),
]


if __name__ == '__main__':
    server = DocumentAPI(documents=documents)
    server.run()