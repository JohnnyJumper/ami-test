
from flask import Flask, jsonify, make_response, request
from document import DocumentError

class DocumentAPI:
	app = Flask(__name__)

	def __init__(self, documents, is_testing = False):
		self.documents = documents
		if not is_testing:
			self.setup_routes()

	def run(self):
		self.app.run()

	def setup_routes(self):
		self.app.register_error_handler(DocumentError, self.handle_document_error)
		self.app.add_url_rule('/documents/needs_review', methods=['GET'], view_func=self.get_documents_needing_review)
		self.app.add_url_rule('/documents/save_changes', methods=['POST'], view_func=self.save_document_changes)
		self.app.add_url_rule('/documents/duplicates', methods=['GET'], view_func=self.get_duplicate_documents)


	def get_documents_needing_review(self):
		result = [vars(doc) for doc in self.documents if doc.status == "NEEDS_REVIEW"]
		return jsonify(result)

	def save_document_changes(self, data=None):
		if data is None:
			data = request.json

		if not data:
			raise DocumentError("No data provided", 400)
		
		if 'documents' not in data:
			raise DocumentError("No documents provided", 400)

		updated_documents = []
		for doc_data in data['documents']:
			doc_id = doc_data.get('id')
			to_update = doc_data.get('toUpdate')

			if not doc_id:
				raise DocumentError("Document ID is missing", 400)
      
			if not to_update:
				raise DocumentError("Fields to update are missing", 400)

			document = next((doc for doc in self.documents if doc.id == doc_id), None)
			if not document:
				raise DocumentError(f"Document with ID {doc_id} not found", 404)
			
			document.update(**to_update)
			updated_documents.append(document)

		if not updated_documents:
			raise DocumentError("No documents were updated", 404)
    
		return make_response(jsonify({"message": "Documents have been successfully updated", "updated_documents": [doc.to_dict() for doc in updated_documents]}), 200)
	
	def get_duplicate_documents(self):
		duplicate_documents = self._find_duplicate_documents(self.documents)
		duplicates_info = []
		for docs in duplicate_documents:
			duplicates_info.append([doc.to_dict() for doc in docs])

		return jsonify({"message": "Duplicates found" if duplicate_documents else "No duplicates found", "duplicates": duplicates_info})

	def handle_document_error(self, error):
		response = jsonify({"error": error.args[0]})
		response.status_code = error.status_code
		return response
	
	def _find_duplicate_documents(self, documents):
		duplicates = {}
    
		for doc in documents:
			if doc.hash in duplicates:
				duplicates[doc.hash].append(doc)
			else:
				duplicates[doc.hash] = [doc]
		
		return [d for d in duplicates.values() if len(d) > 1]
