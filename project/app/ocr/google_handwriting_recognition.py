from remote_pdb import set_trace as st
import io
import os
from autocorrect import Speller
import requests
import re
import spacy
from spacy.tokenizer import Tokenizer
from nltk.stem import PorterStemmer
import json
import dotenv

nlp = spacy.load("en_core_web_sm")


# initializing object
spell = Speller(lang='en')
dotenv.load_dotenv()

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./key.json"


def environment_vars_jsonify():
    json_dict = dict()
    # st(host='0.0.0.0', port=4444)
    json_dict["type"] = os.getenv("type")
    json_dict["project_id"] = os.getenv("project_id")
    json_dict["private_key_id"] = os.getenv("private_key_id")
    json_dict["private_key"] = os.getenv("private_key")
    json_dict["client_email"] = os.getenv("client_email")
    json_dict["client_id"] = os.getenv("client_id")
    json_dict["auth_uri"] = os.getenv("auth_uri")
    json_dict["token_uri"] = os.getenv("token_uri")
    json_dict["auth_provider_x509_cert_url"] = os.getenv("auth_provider_x509_cert_url")
    json_dict["client_x509_cert_url"] = os.getenv("client_x509_cert_url")

    with open("key.json", "w") as file_obj:
        file_obj.write(json.dumps(json_dict, indent=4))


def google_handwriting_recognizer(local_path=None, url=None) -> str:
    """
        Will return the text of a handwritten text.
        Only one parameter should be set, otherwise the second one will be ignored.

        Args:
            -local_path:
            local .jpg file name

            -URL:
            .jpg file URL
    """
    
    # [START vision_set_endpoint]
    from google.cloud import vision
    client_options = {'api_endpoint': 'eu-vision.googleapis.com'}
    client = vision.ImageAnnotatorClient(client_options=client_options)
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
        # import urllib.request
        # urllib.request.urlretrieve(url, "downloaded_img.jpg")

        # 2. passing it to the google's local file handrwiting recognition module
        with io.open("downloaded_img.jpg", 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

        # 3. delete the extra image file
        # os.remove("downloaded_img.jpg")

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


def spellcheck(input_str: str) -> str:


    """
    Will scroll through string, correct spelling error words,
    and return the entire string
     """
    textcorrected = spell(input_str)
    return textcorrected

def tokenize(input_str: str) -> str:
    '''
    Will return all individual words in an array, ignores NLP stop words
    '''
    tokens = re.sub('[^a-zA-Z 0-9]', '', input_str)
    tokens = tokens.lower().split()
    STOP_WORDS = nlp.Defaults.stop_words
    arr = []
    for token in tokens:
        if token not in STOP_WORDS:
            arr.append(token)

    
    return arr

def spellchecked_words(input_str: str) -> int:
    '''
    Takes a string, runs spellcheck on string, compares different words after spellcheck to before,
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
    '''
    finds length of original string after tokenization, divides # of spellchecked words
    by that length to find efficiency rating
    '''
    original = len(tokenize(input_str))
    difference = spellchecked_words(input_str)

    percentage = difference / original
    return percentage 

def unique_words(input_str: str) -> int:
    '''
    finds percentage of total words in tokenized string that are unique words
    '''
    arr = []
    arr2 = set()
    words = tokenize(input_str)
    for word in words:
        arr.append(word)
        arr2.add(word)
        x = len(arr2) / len(arr)
    return x  

def avg_len_words(input_str: str) -> int:
    '''
    finds the average length of words after tokenization in the text
    '''
    arr = []
    words = tokenize(input_str)
    for word in words:
        x = len(word)
        arr.append(x)
        y = sum(arr) / len(arr)
    return y     





if __name__ == '__main__':
    # set_endpoint('./weird_page_2.jpg')
    #random_image = "https://s.imgur.com/images/logo-1200-630.jpg?2"
    #url = r'https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/51--/5101/Photo%205101.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC6YjAXwYe04FDe2uDN4oYS604ldor5G3BOxWROCzYgvAIhAKIwEvEfXdk17xFZ4RPqYddNNdhmDyDAZM1PoXnRBvQRKuQCCMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMTgyNTk3MzM5ODk5Igxe25VTGEWW%2BoPCaLsquAJl9zk2VZ6rJiK%2FQ11omMOqI5eT5JOATYKFng%2FNTmiCh73QyN0tUEN%2BaEy9cT%2F3BtXVM8Bwy9NE7jmGsQKX3SyE5lJNkaVPEcwPsw8axzxCG82fj9zzcHLwOx%2FjuohATf0wuuGSZkBrFhWG07OSphaAVOvEeu1HqTrVJ7a8znWEuWpsfqldimgizxUPnhBbrMQGiHgLaOHsZ45IVxTJgAJ5T3LmaBjyFsGkKWfjNLKqOFjVP6X7QbyzERpfslUWt8nNSQzfnO5XmPVBbh7P9ArDS5CsZjXMmwomX3UoQOyDmzgqqKEyx4GEBbP60snlpmDd9%2FxvK0RLTEgZcQvS90Z%2BJrFWHuFQmCa2uEUQQKgF7Qpq8qqSjeq6IAGBYIDe9p6dZUelO3WUeBs3LIYhJiAqWC5QHch%2FiHkwh6T%2F%2BgU6rwJOXHMXojdMoiOi7c5oERGxk7kd4eURK1CO6f90YeuVLKrvAkG9a9vlBO4wA7kGgF%2B4viMEBObGfSM1MXG2cNO%2FdH1LMh%2Bq7VMSZ%2B2PVwvPDxrDie4SHO4gsTyK0U1XgP8R9z95ti7SwTWuzBqE%2FzWG2azVnpt8wLcdF3HsqlK9MLzLnyw2j%2FY5oh6LLEgEECRpIpYX05d8zraQUCc%2FdY%2BJZcAq6Ec741Ath%2Bgdvq%2BHcd8ZhkMmJZAFKtysT15ZFuHCU%2BS2vw4sFE%2Fae4L8Ku4uIuQ8qb%2BiX5IQ8Ybpab26SBhlWB7jpVAY9IT2r2ZF0ViBx5LaNo1n6IJhMP1fNMCn64WRxsT6O9Exq6ZRUhMut9UPQUyysAMBlzG9UOOvgh1OniHK2%2BEuOU1xd2jXR1I%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200914T203428Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5UWWGGEGM%2F20200914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b258d09c203bd63162062a410de93592f567c025888905336be23ff5a6e2ad43'
    #url = r'https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/31--/3104/Photo%203104%20pg1.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC6YjAXwYe04FDe2uDN4oYS604ldor5G3BOxWROCzYgvAIhAKIwEvEfXdk17xFZ4RPqYddNNdhmDyDAZM1PoXnRBvQRKuQCCMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMTgyNTk3MzM5ODk5Igxe25VTGEWW%2BoPCaLsquAJl9zk2VZ6rJiK%2FQ11omMOqI5eT5JOATYKFng%2FNTmiCh73QyN0tUEN%2BaEy9cT%2F3BtXVM8Bwy9NE7jmGsQKX3SyE5lJNkaVPEcwPsw8axzxCG82fj9zzcHLwOx%2FjuohATf0wuuGSZkBrFhWG07OSphaAVOvEeu1HqTrVJ7a8znWEuWpsfqldimgizxUPnhBbrMQGiHgLaOHsZ45IVxTJgAJ5T3LmaBjyFsGkKWfjNLKqOFjVP6X7QbyzERpfslUWt8nNSQzfnO5XmPVBbh7P9ArDS5CsZjXMmwomX3UoQOyDmzgqqKEyx4GEBbP60snlpmDd9%2FxvK0RLTEgZcQvS90Z%2BJrFWHuFQmCa2uEUQQKgF7Qpq8qqSjeq6IAGBYIDe9p6dZUelO3WUeBs3LIYhJiAqWC5QHch%2FiHkwh6T%2F%2BgU6rwJOXHMXojdMoiOi7c5oERGxk7kd4eURK1CO6f90YeuVLKrvAkG9a9vlBO4wA7kGgF%2B4viMEBObGfSM1MXG2cNO%2FdH1LMh%2Bq7VMSZ%2B2PVwvPDxrDie4SHO4gsTyK0U1XgP8R9z95ti7SwTWuzBqE%2FzWG2azVnpt8wLcdF3HsqlK9MLzLnyw2j%2FY5oh6LLEgEECRpIpYX05d8zraQUCc%2FdY%2BJZcAq6Ec741Ath%2Bgdvq%2BHcd8ZhkMmJZAFKtysT15ZFuHCU%2BS2vw4sFE%2Fae4L8Ku4uIuQ8qb%2BiX5IQ8Ybpab26SBhlWB7jpVAY9IT2r2ZF0ViBx5LaNo1n6IJhMP1fNMCn64WRxsT6O9Exq6ZRUhMut9UPQUyysAMBlzG9UOOvgh1OniHK2%2BEuOU1xd2jXR1I%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200914T213100Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5UWWGGEGM%2F20200914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=cdddb0b711c13f3bd5f32842bd6548a3ff9ddbb01fa8d415c6c28d26eeb858c6'
    # url = r'https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/51--/5102/Photo%205102%20pg1.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC6YjAXwYe04FDe2uDN4oYS604ldor5G3BOxWROCzYgvAIhAKIwEvEfXdk17xFZ4RPqYddNNdhmDyDAZM1PoXnRBvQRKuQCCMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMTgyNTk3MzM5ODk5Igxe25VTGEWW%2BoPCaLsquAJl9zk2VZ6rJiK%2FQ11omMOqI5eT5JOATYKFng%2FNTmiCh73QyN0tUEN%2BaEy9cT%2F3BtXVM8Bwy9NE7jmGsQKX3SyE5lJNkaVPEcwPsw8axzxCG82fj9zzcHLwOx%2FjuohATf0wuuGSZkBrFhWG07OSphaAVOvEeu1HqTrVJ7a8znWEuWpsfqldimgizxUPnhBbrMQGiHgLaOHsZ45IVxTJgAJ5T3LmaBjyFsGkKWfjNLKqOFjVP6X7QbyzERpfslUWt8nNSQzfnO5XmPVBbh7P9ArDS5CsZjXMmwomX3UoQOyDmzgqqKEyx4GEBbP60snlpmDd9%2FxvK0RLTEgZcQvS90Z%2BJrFWHuFQmCa2uEUQQKgF7Qpq8qqSjeq6IAGBYIDe9p6dZUelO3WUeBs3LIYhJiAqWC5QHch%2FiHkwh6T%2F%2BgU6rwJOXHMXojdMoiOi7c5oERGxk7kd4eURK1CO6f90YeuVLKrvAkG9a9vlBO4wA7kGgF%2B4viMEBObGfSM1MXG2cNO%2FdH1LMh%2Bq7VMSZ%2B2PVwvPDxrDie4SHO4gsTyK0U1XgP8R9z95ti7SwTWuzBqE%2FzWG2azVnpt8wLcdF3HsqlK9MLzLnyw2j%2FY5oh6LLEgEECRpIpYX05d8zraQUCc%2FdY%2BJZcAq6Ec741Ath%2Bgdvq%2BHcd8ZhkMmJZAFKtysT15ZFuHCU%2BS2vw4sFE%2Fae4L8Ku4uIuQ8qb%2BiX5IQ8Ybpab26SBhlWB7jpVAY9IT2r2ZF0ViBx5LaNo1n6IJhMP1fNMCn64WRxsT6O9Exq6ZRUhMut9UPQUyysAMBlzG9UOOvgh1OniHK2%2BEuOU1xd2jXR1I%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200914T211040Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5UWWGGEGM%2F20200914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=d53969b05bfabab49dae6cbc79b833338a68e1fb42fe86c4979d481c3d185891'

    # print(
    #     set_endpoint(local_path="./weird_page_2.jpg")
    # )
    #normal = google_handwriting_recognizer(url=url)
    #corrected = spellcheck(normal)
    #print("normal:", normal)
    #print()
    #print("corrected:", corrected)
    environment_vars_jsonify()

    string = "After a long toalk ith the was Summer seperated Then side April was over. Suddenly before them. He mad at April that they diffeent sidles. from the on. Summer came running strong muscular mon stood a genie. I three wishes. was. onto completely a huge fla sh a Said, am here to grant you am made 2 w "
    x = (string)
    
    #print(len(x))
    #print(len(y))
    print(spellchecked_words(x))
    print(efficiency(x))
    print(unique_words(x))
    print(avg_len_words(x))
     
