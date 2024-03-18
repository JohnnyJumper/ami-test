import unittest

from flask import Flask
from document import Document, DocumentError
from server import DocumentAPI

class TestDocumentAPI(unittest.TestCase):

	def setUp(self):
		# Create a Flask application and push an application context
		self.app = Flask(__name__)
		self.ctx = self.app.app_context()
		self.ctx.push()

		# Mock data for testing
		self.documents = [
			Document(1, "Document 1", "pdf", "portrait", "NEEDS_REVIEW", "This is the text representation of Document 1."),
			Document(2, "Document 2", "docx", "landscape", "NEEDS_REVIEW", "This is the text representation of Document 2."),
			Document(3, "Document 3", "pdf", "portrait", "NEEDS_REVIEW", "This is the text representation of Document 3."),
			Document(4, "Document 4", "docx", "landscape", "NEEDS_REVIEW", "This is the text representation of Document 4."),
			# Adding duplicate documents for testing get_duplicate_documents
			Document(5, "Document 5", "pdf", "portrait", "NEEDS_REVIEW", "Duplicate text"),
			Document(6, "Document 6", "docx", "landscape", "NEEDS_REVIEW", "Duplicate text")
		]
		self.api = DocumentAPI(self.documents, is_testing=True)
  
	def tearDown(self):
		# Pop the application context after each test
		self.ctx.pop()

	def test_get_documents_needing_review(self):
		response = self.api.get_documents_needing_review()
		self.assertEqual(response.status_code, 200)
		data = response.json
		self.assertTrue(isinstance(data, list))
		self.assertEqual(len(data), self.documents.__len__())

    # Add more test methods for other endpoints (save_document_changes, get_duplicate_documents, etc.)

	def test_save_document_changes(self):
		# Test saving document changes with valid data
		valid_data = {'documents': [{'id': 1, 'toUpdate': {'name': 'Updated Name'}}]}
		response = self.api.save_document_changes(valid_data)
		self.assertEqual(response.status_code, 200)
		updated_documents = response.json.get('updated_documents')
		self.assertIsNotNone(updated_documents)
		self.assertEqual(len(updated_documents), 1)  # Ensure only one document is updated

		# Test saving document changes with invalid data (no documents provided)
		invalid_data = {}
		with self.assertRaises(DocumentError):
				self.api.save_document_changes(invalid_data)

		# Test saving document changes with invalid data (non-existent document ID)
		invalid_data = {'documents': [{'id': 10, 'toUpdate': {'name': 'Updated Name'}}]}
		with self.assertRaises(DocumentError):
				self.api.save_document_changes(invalid_data)

	def test_get_duplicate_documents(self):
        # Test getting duplicate documents
		response = self.api.get_duplicate_documents()
		self.assertEqual(response.status_code, 200)
		data = response.json
		self.assertTrue(isinstance(data, dict))
		self.assertIn('message', data)
		if data['message'] == 'Duplicates found':
				self.assertIn('duplicates', data)
		else:
				self.assertNotIn('duplicates', data)

if __name__ == '__main__':
    unittest.main()