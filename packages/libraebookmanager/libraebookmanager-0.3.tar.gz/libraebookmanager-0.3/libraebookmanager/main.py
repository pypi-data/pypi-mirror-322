import os
from scanner import scan_ebook_folder, save_to_json
from html_generator import generate_html


def main():
    folder_path = input("Enter the path to your eBook folder: ")
    # Check if the directory exists
    if not os.path.isdir(folder_path):
        print(
            f"Error: The directory '{folder_path}' does not exist or is not a valid directory.")
        return
    json_file = "libra_ebook_data.json"
    html_file = "libra_ebook_library.html"

    # Scan folder and save JSON
    ebook_data = scan_ebook_folder(folder_path)
    save_to_json(ebook_data, json_file)

    # Generate HTML
    generate_html(json_file, html_file)

    print(f"JSON data saved to {json_file}")
    print(
        f"HTML file generated at {html_file}. Open it in a browser to view your eBook library.")


if __name__ == "__main__":
    main()
