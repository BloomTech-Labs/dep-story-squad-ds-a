# from remote_pdb import set_trace as st
# from pdb import set_trace as st
import io
import os
from autocorrect import Speller
import requests
import re
import spacy
from spacy.tokenizer import Tokenizer
from nltk.stem import PorterStemmer
import json
from pdf2image import convert_from_path
from typing import List
import boto3
from google.cloud import vision
from google.oauth2 import service_account


# initializing object
nlp = spacy.load("en_core_web_sm")
spell = Speller(lang='en')


def google_handwriting_recognizer(
        local_path: str = None, url: str = None, s3_obj: str = None) -> str:
    """
        Will return the text of a handwritten text.
        Only one parameter should be set, otherwise
        the second one will be ignored.

        Args:
            -local_path:
            local .jpg file name

            -URL:
            .jpg file URL
    """

    # [START vision_set_endpoint]

    # removing '$' from first character of the environment variable
    google_credentiaol_dict = os.getenv("GOOGLE_CREDENTIALS_DICT")
    google_credentiaol_dict = google_credentiaol_dict[1:]

    # reading google credential
    json_acct_info = json.loads(google_credentiaol_dict)
    credentials = service_account.Credentials.from_service_account_info(
        json_acct_info)

    client_options = {'api_endpoint': 'eu-vision.googleapis.com'}
    client = vision.ImageAnnotatorClient(
        client_options=client_options,
        credentials=credentials
    )
    # [END vision_set_endpoint]

    if local_path is not None:
        # image is a local file on the drive
        with io.open(local_path, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

    elif url is not None:
        # image is stored online, and it should be downloaded first

        # 1. downloading the image
        response = requests.get(url)
        with open("downloaded_img.jpg", "wb") as file_obj:
            file_obj.write(response.content)

        # 2. pass the image to the google's local file handrwiting
        # recognition module
        with io.open("downloaded_img.jpg", 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

        # 3. delete the extra image file
        os.remove("downloaded_img.jpg")

    elif s3_obj is not None:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket('training-images-team-a')

        output_file_name = s3_obj.split("/")[-1]
        bucket.download_file(s3_obj, output_file_name)
        with io.open(output_file_name, 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

        os.remove(output_file_name)

    else:
        return "No parameters were set!"

    response = client.text_detection(image=image)
    # text = response.text_annotations.text.replace("\n", " ")
    return_str = response.full_text_annotation.text.replace("\n", " ")

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

    return return_str


def google_pdf_handwriting_recognizer(
        local_path: str = None, url: str = None
        ) -> str:
    """
        Will return the text of a handwritten pdf file.
        Only one parameter should be set, otherwise
        the second one will be ignored.

        Args:
            -local_path:
            local .pdf file name

            -URL:
            .pdf file URL
    """

    ocr_text_list = []
    
    # 1. see if pdf is local or online
    if url is not None:
        # pdf is stored online, and it should be downloaded first

        # 1.1. downlaod the pdf
        response = requests.get(url)
        with open("downloaded_pdf.pdf", "wb") as file_obj:
            file_obj.write(response.content)

        # 1.2. convert pdf to a series of jpg files
        pdf_to_jpg("downloaded_pdf.pdf")

    if local_path is not None:
        # pdf is a local file on the drive

        # 2.2. convert pdf to a series of jpg files
        pdf_to_jpg(local_path)

    # 2. get the name of all .jpg files
    jpg_file_names = \
        [file_name for file_name in os.listdir() if file_name.endswith(".jpg")]

    for jpg_file in jpg_file_names:
        # 3. call google_handwriting_recognizer on each file
        ocr_text_list.append(
            google_handwriting_recognizer(local_path=jpg_file)
            )
        print(f"Done with {jpg_file} ocr")

    # 4. delete all jpgs and pdfs files
    delete_all_file_types(file_types=["jpg", "pdf"])

    return ocr_text_list


def pdf_to_jpg(pdf_local_file: str) -> None:
    """
    Will create a series of .jpg files named 1.jpg to n.jpg
    (n=number of pages).
    Args:
        pdf_local_file:
            pdf local file address
    """

    pages = convert_from_path(pdf_local_file, 500)

    for index, page in enumerate(pages):
        page.save(f'{index+1}.jpg', 'JPEG')


def delete_all_file_types(file_types: List[str], dir: str = "./") -> None:
    """
    Will delete all file types disclosed in file_types.
    Args:
        file_types:
            list of file types to be deleted without
            the starting '.' .
                -example:
                ["pdf", "jpg"]
        dir:
            The directory to look to delete files
    """
    for file_name in os.listdir(dir):
        if file_name.split(".")[-1].lower() in file_types:
            os.remove(file_name)


def spellcheck(input_str: str) -> str:
    """
    Will scroll through string, correct spelling error words,
    and return the entire string
    """
    textcorrected = spell(input_str)

    return textcorrected


def tokenize(input_str: str) -> str:
    """
    Will return all individual words in an array, ignores NLP stop words
    """
    tokens = re.sub('[^a-zA-Z 0-9 \.]', '',  input_str)
    tokens = tokens.lower().split()
    STOP_WORDS = nlp.Defaults.stop_words
    arr = []
    for token in tokens:
        if token not in STOP_WORDS:
            arr.append(token)

    return arr


def spellchecked_words(input_str: str) -> int:
    '''
    Takes a string, runs spellcheck on string, compares
    different words after spellcheck to before,
    returns number of words spellchecked
    '''
    arr = []
    words1 = tokenize(input_str)
    words2 = tokenize(spellcheck(input_str))

    for word in words1:
        if word not in words2:
            arr.append(word)

    return len(arr)


def efficiency(input_str: str) -> int:
    """
    finds length of original string after tokenization,
    divides # of non-spellchecked words
    by # of total words
    """
    original = len(tokenize(input_str))
    difference = original - spellchecked_words(input_str)

    percentage = difference / original

    return percentage


def unique_words(input_str: str) -> int:
    """
    finds percentage of total words in tokenized string that are unique words
    """
    arr = []
    arr2 = set()
    words = tokenize(input_str)
    for word in words:
        arr.append(word)
        arr2.add(word)
        x = len(arr2) / len(arr)

    return x


def avg_sentence_length(input_str: str) -> int:
    """
    finds average sentence length after tokenization
    by taking total tokens / tokens containing .
    """

    arr = []
    words = tokenize(input_str)
    count = 0
    for word in words:
        if '.' in word:
            count += 1

    for word in words:
        arr.append(word)
        x = (len(arr) / 10)

    return x / count


def avg_len_words(input_str: str) -> int:
    """
    finds the average length of words after tokenization in the text
    """
    arr = []
    words = tokenize(input_str)
    for word in words:
        x = len(word)
        arr.append(x)
        y = (sum(arr) / len(arr)) /10  

    return y


def evaluate(input_str: str) -> int:
    # tokenize and spellcheck the input string, add words to set,
    score = \
        (.2 * unique_words(input_str)) +\
        (.3 * avg_len_words(input_str)) +\
        (.3 * avg_sentence_length(input_str)) +\
        (.2 * efficiency(input_str))

    return score


if __name__ == '__main__':
    # corrected = spellcheck(normal)
    # print("normal:", normal)
    # print()
    # print("corrected:", corrected)
    #x = google_pdf_handwriting_recognizer(local_path="./test_pdfs/test_pdf_1.pdf")
    #x = " ".join(x)
    string = "After a long toalk. ith the was Summer seperated Then side April was over. Suddenly before them. He mad at April that they diffeent sidles. from the on. Summer came running strong muscular mon stood a genie. I three wishes. was. onto completely a huge fla sh a Said. am here to grant you am made 2 w "
    x = (string)
    print(tokenize(x))
    print(avg_sentence_length(x))
    print(spellchecked_words(x))
    print(efficiency(x))
    print(unique_words(x))
    print(avg_len_words(x))
    print(evaluate(x))
