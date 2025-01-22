def generate_html(json_file, output_html):
    """Generate an HTML file to display eBook data with a Google search link."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Ebook Library</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .book-list {{
                display: flex;
                flex-direction: column;
                gap: 20px;
            }}
            .book {{
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .book h3 {{
                margin: 0 0 10px 0;
            }}
            .book p {{
                margin: 5px 0;
            }}
            .book a {{
                color: #1a0dab;
                text-decoration: none;
            }}
            .book a:hover {{
                text-decoration: underline;
            }}
            .search {{
                margin-bottom: 20px;
            }}
            .search input {{
                width: 100%;
                padding: 10px;
                font-size: 16px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }}
        </style>
    </head>
    <body>
        <h1>Ebook Library</h1>
        <div class="search">
            <input type="text" id="searchInput" placeholder="Search by name..." oninput="filterBooks()">
        </div>
        <div class="book-list" id="bookList"></div>

        <script>
            function loadBooks() {{
                fetch('{json_file}')
                    .then(response => response.json())
                    .then(data => {{
                        window.books = data;
                        displayBooks(data);
                    }});
            }}

            function displayBooks(books) {{
                const bookList = document.getElementById('bookList');
                bookList.innerHTML = '';
                books.forEach(book => {{
                    const bookDiv = document.createElement('div');
                    bookDiv.className = 'book';
                    const title = book.metadata.title || book.name;
                    bookDiv.innerHTML = `
                        <h3>${{title}}</h3>
                        <p><strong>Author:</strong> ${{book.metadata.creator || 'Unknown'}}</p>
                        <p><strong>Format:</strong> ${{book.format}}</p>
                        <p><strong>Size:</strong> ${{(book.size / 1024).toFixed(2)}} KB</p>
                        <a href="https://www.google.com/search?q=${{encodeURIComponent(title)}}" target="_blank">Click to Google</a>
                    `;
                    bookList.appendChild(bookDiv);
                }});
            }}

            function filterBooks() {{
                const searchTerm = document.getElementById('searchInput').value.toLowerCase();
                const filteredBooks = window.books.filter(book => 
                    book.name.toLowerCase().includes(searchTerm) || 
                    (book.metadata.title && book.metadata.title.toLowerCase().includes(searchTerm))
                );
                displayBooks(filteredBooks);
            }}
            window.onload = loadBooks;
        </script>
    </body>
    </html>
    """

    with open(output_html, 'w') as f:
        f.write(html_content)
