# Libra Ebook Manager

A Python package to scan a directory of eBooks, extract metadata, and generate an HTML file to display the eBook library with search functionality and Google search links.

---

## Features

- **Scan eBook Directory**: Recursively scans a directory for eBook files (PDF, EPUB, etc.).
- **Extract Metadata**: Extracts metadata such as title, author, format, and size.
- **Generate HTML**: Creates an HTML file to display the eBook library in a clean, searchable format.
- **Google Search Links**: Adds a "Click to Google" link below each book's title to search for the book on Google.
- **Search Functionality**: Allows users to search for books by name or title.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/arazshah/libra.git
   cd libra
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Install the Package**:
   ```bash
   pip install .
   ```

---

## Usage

### Command-Line Interface

Run the `libra` command to scan a directory and generate the HTML file:

```bash
libra
```

You will be prompted to enter the path to your eBook folder. After processing, the script will generate two files:

1. **`libra_ebook_data.json`**: Contains metadata for all eBooks.
2. **`libra_ebook_library.html`**: Displays the eBook library in a browser.

### Example

```bash
$ libra
Enter the path to your eBook folder: /path/to/your/ebook/folder
JSON data saved to libra_ebook_data.json
HTML file generated at libra_ebook_library.html. Open it in a browser to view your eBook library.
```

---

## HTML Output

The generated `libra_ebook_library.html` file will display the eBooks in a clean, searchable format. Each book entry includes:

- **Title**: The title of the book (or the file name if the title is unavailable).
- **Author**: The author of the book (or "Unknown" if unavailable).
- **Format**: The file format (e.g., PDF, EPUB).
- **Size**: The file size in KB.
- **Click to Google**: A link to search for the book on Google.

---

## Customization

### HTML Template

You can customize the HTML template in the `html_generator.py` file to change the layout, styling, or functionality.

---

## Dependencies

- **Pillow**: For image manipulation (optional for thumbnails).
- **PyMuPDF (fitz)**: For extracting PDF and EPUB pages as images (optional for thumbnails).
- **ebooklib**: For handling EPUB metadata.
- **python-magic**: For detecting file types.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/yourusername/libra/issues).

---

## Acknowledgments

- Thanks to the developers of `Pillow`, `PyMuPDF`, `ebooklib`, and `python-magic` for their excellent libraries.
- Inspired by the need for a simple eBook library manager.

---

Enjoy managing your eBook collection with **Ebook Manager**! 📚
