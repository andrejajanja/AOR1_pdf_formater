import requests, zipfile, os, glob
from PyPDF2 import PdfWriter, PdfReader

files_dir = "./temp_files/"

def download_and_unzip():
    domain = "https://rti.etf.bg.ac.rs/rti/ri3aor/rokovi/"

    for year in range(2016, 2025, 1):
        response = requests.get(f"{domain}AOR1_{year}.zip", stream=True)

        with open(f"{files_dir}{year}.zip", 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        unziped_name = f"{files_dir}{year}"
        os.mkdir(unziped_name)
        with zipfile.ZipFile(f"{files_dir}{year}.zip", 'r') as zip_ref:
            zip_ref.extractall(unziped_name)


    zip_files = glob.glob(os.path.join(files_dir, '*.zip'))

    for zip_file in zip_files:
        try:
            os.remove(zip_file)
        except OSError as e:
            print(f"Error: {zip_file} : {e.strerror}")

def merge_pdfs():
    file_pairs = []
    for root, dirs, files in os.walk(files_dir):
        for file in files:
            full_path = os.path.join(root, file)
            file_pairs.append((file[file.find("_")+1:-4], full_path))

    file_pairs.sort(key=lambda tup: tup[0])

    writer = PdfWriter()
    current_page = 0

    for (name, fpath) in file_pairs:
        reader = PdfReader(fpath)

        # Loop through all pages in the reader and add them to the writer
        for page_number in range(len(reader.pages)):
            writer.add_page(reader.pages[page_number])  # Add each page

        # Add an outline entry for the first page of each PDF
        writer.add_outline_item(name, current_page)
        
        # Increment the current page count
        current_page += len(reader.pages)

    with open("AOR1_objedinjeni_rokovi.pdf", 'wb') as f:
        writer.write(f)
    