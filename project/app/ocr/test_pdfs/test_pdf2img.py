from pdf2image import convert_from_path
pages = convert_from_path('./test_pdf_1.pdf', 500)

for index, page in enumerate(pages):
    page.save(f'{index+1}.jpg', 'JPEG')