import hashlib

class Document:
	def __init__(self, id, name, format, orientation, status, text_representation):
		self.id = id
		self.name = name
		self.format = format
		self.orientation = orientation
		self.status = status
		self.text_representation = text_representation
		self._calculate_hash()

	def _calculate_hash(self):
		self.hash = hashlib.sha256(self.text_representation.encode()).hexdigest()

	def to_dict(self):
		return {
			"id": self.id,
			"name": self.name,
      "format": self.format,
      "orientation": self.orientation,
      "status": self.status,
      "text_representation": self.text_representation
    }
	
	def update(self, **kwargs):
		for key, value in kwargs.items():
			if hasattr(self, key):
				setattr(self, key, value)
		self._calculate_hash()

class DocumentError(Exception):
    def __init__(self, message, status_code):
        super().__init__(message)
        self.status_code = status_code