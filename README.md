# Document Management API

This repository contains the source code for a Document Management API built with Flask.

## Overview

The Document Management API provides endpoints for managing documents, including retrieving documents needing review, saving document changes, and finding duplicate documents.

## Features

- Retrieve documents needing review
- Save document changes
- Find duplicate documents

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/document-management-api.git
```

Install dependencies:

```bash
cd document-management-api
pip install -r requirements.txt
```

Run the server:
```bash
python app.py
```

Usage
-----

*   **GET /documents/needs\_review**: Retrieve documents needing review.
*   **POST /documents/save\_changes**: Save document changes.
*   **GET /documents/duplicates**: Find duplicate documents.

Testing
-------

Unit tests are included in the `test_document_api.py` file. Run the tests with:

```bash
python -m unittest test_document_api.py
```
