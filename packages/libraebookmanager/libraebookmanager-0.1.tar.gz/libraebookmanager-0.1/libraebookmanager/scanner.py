import os
import json
import magic
from PIL import Image
from PyPDF2 import PdfReader
from ebooklib import epub


def get_file_metadata(file_path):
    """Extract metadata from a file."""
    file_type = magic.from_file(file_path, mime=True)
    metadata = {
        'size': os.path.getsize(file_path),
        'format': file_type,
        'metadata': {}
    }

    try:
        if file_type == 'application/pdf':
            try:
                reader = PdfReader(file_path)
                metadata['metadata'] = {
                    'title': reader.metadata.title or os.path.basename(file_path),
                    'author': reader.metadata.author or 'Unknown',
                    'subject': reader.metadata.subject or '',
                    'creator': reader.metadata.creator or '',
                    'producer': reader.metadata.producer or '',
                    'creation_date': str(reader.metadata.creation_date) if reader.metadata.creation_date else '',
                    'modification_date': str(reader.metadata.modification_date) if reader.metadata.modification_date else ''
                }
            except Exception as e:
                print(f"Error reading PDF file '{file_path}': {e}")
                metadata['metadata'] = {
                    'title': os.path.basename(file_path),
                    'author': 'Unknown',
                    'error': str(e)
                }

        elif file_type == 'application/epub+zip':
            try:
                book = epub.read_epub(file_path)
                metadata['metadata'] = {
                    'title': book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else os.path.basename(file_path),
                    'creator': book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Unknown',
                    'language': book.get_metadata('DC', 'language')[0][0] if book.get_metadata('DC', 'language') else '',
                    'identifier': book.get_metadata('DC', 'identifier')[0][0] if book.get_metadata('DC', 'identifier') else '',
                    'date': book.get_metadata('DC', 'date')[0][0] if book.get_metadata('DC', 'date') else ''
                }
            except Exception as e:
                print(f"Error reading EPUB file '{file_path}': {e}")
                metadata['metadata'] = {
                    'title': os.path.basename(file_path),
                    'creator': 'Unknown',
                    'error': str(e)
                }

    except Exception as e:
        print(f"Unexpected error processing file '{file_path}': {e}")
        metadata['metadata'] = {
            'title': os.path.basename(file_path),
            'error': str(e)
        }

    return metadata


def scan_ebook_folder(folder_path):
    """Scan the folder and collect file information."""
    ebook_data = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, folder_path)

            try:
                metadata = get_file_metadata(file_path)
                ebook_data.append({
                    'name': file,
                    'directory': relative_path,
                    'size': metadata['size'],
                    'format': metadata['format'],
                    'metadata': metadata['metadata']
                })
            except Exception as e:
                print(f"Skipping file '{file_path}' due to error: {e}")

    return ebook_data


def save_to_json(data, output_file):
    """Save the collected data to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)
