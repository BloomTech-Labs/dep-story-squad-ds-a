from ipdb import set_trace as st
import io
import os
from autocorrect import Speller
import requests

# initializing object
spell = Speller(lang='en')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./key.json"


def set_endpoint(local_path=None, url=None) -> str:
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

        # 2. passing it to the google's local file handrwiting recognition module
        with io.open("downloaded_img.jpg", 'rb') as image_file:
            content = image_file.read()
        image = vision.types.Image(content=content)

        # 3. delete the extra image file
        os.remove("downloaded_img.jpg")

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
    textcorrected = spell(input_str)
    return textcorrected


if __name__ == '__main__':
    # set_endpoint('./weird_page_2.jpg')
    random_image = "https://s.imgur.com/images/logo-1200-630.jpg?2"
    # url = r'https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/51--/5101/Photo%205101.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC6YjAXwYe04FDe2uDN4oYS604ldor5G3BOxWROCzYgvAIhAKIwEvEfXdk17xFZ4RPqYddNNdhmDyDAZM1PoXnRBvQRKuQCCMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMTgyNTk3MzM5ODk5Igxe25VTGEWW%2BoPCaLsquAJl9zk2VZ6rJiK%2FQ11omMOqI5eT5JOATYKFng%2FNTmiCh73QyN0tUEN%2BaEy9cT%2F3BtXVM8Bwy9NE7jmGsQKX3SyE5lJNkaVPEcwPsw8axzxCG82fj9zzcHLwOx%2FjuohATf0wuuGSZkBrFhWG07OSphaAVOvEeu1HqTrVJ7a8znWEuWpsfqldimgizxUPnhBbrMQGiHgLaOHsZ45IVxTJgAJ5T3LmaBjyFsGkKWfjNLKqOFjVP6X7QbyzERpfslUWt8nNSQzfnO5XmPVBbh7P9ArDS5CsZjXMmwomX3UoQOyDmzgqqKEyx4GEBbP60snlpmDd9%2FxvK0RLTEgZcQvS90Z%2BJrFWHuFQmCa2uEUQQKgF7Qpq8qqSjeq6IAGBYIDe9p6dZUelO3WUeBs3LIYhJiAqWC5QHch%2FiHkwh6T%2F%2BgU6rwJOXHMXojdMoiOi7c5oERGxk7kd4eURK1CO6f90YeuVLKrvAkG9a9vlBO4wA7kGgF%2B4viMEBObGfSM1MXG2cNO%2FdH1LMh%2Bq7VMSZ%2B2PVwvPDxrDie4SHO4gsTyK0U1XgP8R9z95ti7SwTWuzBqE%2FzWG2azVnpt8wLcdF3HsqlK9MLzLnyw2j%2FY5oh6LLEgEECRpIpYX05d8zraQUCc%2FdY%2BJZcAq6Ec741Ath%2Bgdvq%2BHcd8ZhkMmJZAFKtysT15ZFuHCU%2BS2vw4sFE%2Fae4L8Ku4uIuQ8qb%2BiX5IQ8Ybpab26SBhlWB7jpVAY9IT2r2ZF0ViBx5LaNo1n6IJhMP1fNMCn64WRxsT6O9Exq6ZRUhMut9UPQUyysAMBlzG9UOOvgh1OniHK2%2BEuOU1xd2jXR1I%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200914T203428Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5UWWGGEGM%2F20200914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=b258d09c203bd63162062a410de93592f567c025888905336be23ff5a6e2ad43'
    # url = r'https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/51--/5119/Photo%205119%20pg1.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC6YjAXwYe04FDe2uDN4oYS604ldor5G3BOxWROCzYgvAIhAKIwEvEfXdk17xFZ4RPqYddNNdhmDyDAZM1PoXnRBvQRKuQCCMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMTgyNTk3MzM5ODk5Igxe25VTGEWW%2BoPCaLsquAJl9zk2VZ6rJiK%2FQ11omMOqI5eT5JOATYKFng%2FNTmiCh73QyN0tUEN%2BaEy9cT%2F3BtXVM8Bwy9NE7jmGsQKX3SyE5lJNkaVPEcwPsw8axzxCG82fj9zzcHLwOx%2FjuohATf0wuuGSZkBrFhWG07OSphaAVOvEeu1HqTrVJ7a8znWEuWpsfqldimgizxUPnhBbrMQGiHgLaOHsZ45IVxTJgAJ5T3LmaBjyFsGkKWfjNLKqOFjVP6X7QbyzERpfslUWt8nNSQzfnO5XmPVBbh7P9ArDS5CsZjXMmwomX3UoQOyDmzgqqKEyx4GEBbP60snlpmDd9%2FxvK0RLTEgZcQvS90Z%2BJrFWHuFQmCa2uEUQQKgF7Qpq8qqSjeq6IAGBYIDe9p6dZUelO3WUeBs3LIYhJiAqWC5QHch%2FiHkwh6T%2F%2BgU6rwJOXHMXojdMoiOi7c5oERGxk7kd4eURK1CO6f90YeuVLKrvAkG9a9vlBO4wA7kGgF%2B4viMEBObGfSM1MXG2cNO%2FdH1LMh%2Bq7VMSZ%2B2PVwvPDxrDie4SHO4gsTyK0U1XgP8R9z95ti7SwTWuzBqE%2FzWG2azVnpt8wLcdF3HsqlK9MLzLnyw2j%2FY5oh6LLEgEECRpIpYX05d8zraQUCc%2FdY%2BJZcAq6Ec741Ath%2Bgdvq%2BHcd8ZhkMmJZAFKtysT15ZFuHCU%2BS2vw4sFE%2Fae4L8Ku4uIuQ8qb%2BiX5IQ8Ybpab26SBhlWB7jpVAY9IT2r2ZF0ViBx5LaNo1n6IJhMP1fNMCn64WRxsT6O9Exq6ZRUhMut9UPQUyysAMBlzG9UOOvgh1OniHK2%2BEuOU1xd2jXR1I%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200914T210827Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5UWWGGEGM%2F20200914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=87d7f3ef7ffade2dfb8c8e76fee5f162fbd7481c1b1ac675a2e901fdd237b65c'
    url = r'https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/51--/5102/Photo%205102%20pg1.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEL3%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLXdlc3QtMSJIMEYCIQC6YjAXwYe04FDe2uDN4oYS604ldor5G3BOxWROCzYgvAIhAKIwEvEfXdk17xFZ4RPqYddNNdhmDyDAZM1PoXnRBvQRKuQCCMb%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQARoMMTgyNTk3MzM5ODk5Igxe25VTGEWW%2BoPCaLsquAJl9zk2VZ6rJiK%2FQ11omMOqI5eT5JOATYKFng%2FNTmiCh73QyN0tUEN%2BaEy9cT%2F3BtXVM8Bwy9NE7jmGsQKX3SyE5lJNkaVPEcwPsw8axzxCG82fj9zzcHLwOx%2FjuohATf0wuuGSZkBrFhWG07OSphaAVOvEeu1HqTrVJ7a8znWEuWpsfqldimgizxUPnhBbrMQGiHgLaOHsZ45IVxTJgAJ5T3LmaBjyFsGkKWfjNLKqOFjVP6X7QbyzERpfslUWt8nNSQzfnO5XmPVBbh7P9ArDS5CsZjXMmwomX3UoQOyDmzgqqKEyx4GEBbP60snlpmDd9%2FxvK0RLTEgZcQvS90Z%2BJrFWHuFQmCa2uEUQQKgF7Qpq8qqSjeq6IAGBYIDe9p6dZUelO3WUeBs3LIYhJiAqWC5QHch%2FiHkwh6T%2F%2BgU6rwJOXHMXojdMoiOi7c5oERGxk7kd4eURK1CO6f90YeuVLKrvAkG9a9vlBO4wA7kGgF%2B4viMEBObGfSM1MXG2cNO%2FdH1LMh%2Bq7VMSZ%2B2PVwvPDxrDie4SHO4gsTyK0U1XgP8R9z95ti7SwTWuzBqE%2FzWG2azVnpt8wLcdF3HsqlK9MLzLnyw2j%2FY5oh6LLEgEECRpIpYX05d8zraQUCc%2FdY%2BJZcAq6Ec741Ath%2Bgdvq%2BHcd8ZhkMmJZAFKtysT15ZFuHCU%2BS2vw4sFE%2Fae4L8Ku4uIuQ8qb%2BiX5IQ8Ybpab26SBhlWB7jpVAY9IT2r2ZF0ViBx5LaNo1n6IJhMP1fNMCn64WRxsT6O9Exq6ZRUhMut9UPQUyysAMBlzG9UOOvgh1OniHK2%2BEuOU1xd2jXR1I%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200914T211040Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5UWWGGEGM%2F20200914%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=d53969b05bfabab49dae6cbc79b833338a68e1fb42fe86c4979d481c3d185891'

    # print(
    #     set_endpoint(local_path="./weird_page_2.jpg")
    # )
    print(
        set_endpoint(url=url)
    )

