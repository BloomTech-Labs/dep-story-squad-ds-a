# from remote_pdb import set_trace as st
# from pdb import set_trace as st
import io
import os
import requests
import json
from pdf2image import convert_from_path
from typing import List
import boto3
from google.cloud import vision
from google.oauth2 import service_account


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
        # image is stored in an S3 bucket

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
        local_path: str = None, url: str = None, s3_obj: str = None
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

    elif local_path is not None:
        # pdf is a local file on the drive

        # 2.2. convert pdf to a series of jpg files
        pdf_to_jpg(local_path)

    elif s3_obj is not None:
        # pdf is stored in an S3 bucket

        s3 = boto3.resource('s3')
        bucket = s3.Bucket('training-images-team-a')

        output_file_name = s3_obj.split("/")[-1]
        bucket.download_file(s3_obj, output_file_name)

        pdf_to_jpg(output_file_name)

    else:
        return "No parameters were set!"

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
