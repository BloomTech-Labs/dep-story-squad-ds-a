from ipdb import set_trace as st
import io


def set_endpoint(path):
    """Change your endpoint"""
    # [START vision_set_endpoint]
    from google.cloud import vision
    client_options = {'api_endpoint': 'eu-vision.googleapis.com'}
    client = vision.ImageAnnotatorClient(client_options=client_options)
    # [END vision_set_endpoint]

    # image_source = vision.types.ImageSource(
    #     image_uri=path)
    # image = vision.types.Image(source=image_source)
    with io.open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)

    st()
    print(response.full_text_annotation.text.replace("\n", " "))
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

if __name__ == '__main__':
    set_endpoint('./weird_page_2.jpg')
    # url=r"https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/52--/5205/Photo%205205%20pg3.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEF4aCXVzLWVhc3QtMSJHMEUCIQD%2FpbNQcSJZ9J9vZ%2BudRiuxnmH%2FRbhTDJd1J5GxtJQhrAIgRSGrwRAr1flqzvVCXnAjaGu177pokj%2BYrTpnZDQHaYYq2wIIZxABGgwxODI1OTczMzk4OTkiDFhmeEylcX%2BDpFMxQCq4AqR%2BvskXD2zDsOKjFQ86oS8nt8xEJFoO%2B1im6JBVwpl9gW7BxFxxAoWSr1jj2uQrEgAF9k6UhAxHErtq6cVUOWmdw96dMKEQOdSFHmjjb%2BvRJ6WS7OzxgIOEYYXml9Dv7h5SG6BmMejVwnlc0%2BpdDSX45Hi9s%2FiuYLFgdjxYvodKPYDX4YxGm7CJkdd87ZF4dlS85hwijp3qPqX7rsLgSUcpbGpCR6D9rArIZP2NHdE%2B%2BP1TVIDOI57AQJrUYQbj9kFp8q66YiVG%2BXHgCVB2i3u1YDzEag99AaawQuG8n3i5wTBWx6SnMZsDEp2ZB31WMRH5LNVawb8zQIChQ5mBiD3gcIFS3lb0zw0C1ykYrs%2BM4gYV%2B4Ds3Nd6xB%2BruKRhCBkGhnz6nlBXSM0Z%2F8fbNKRuAJXp7iCKFDDeuur6BTqwAgAic9a69kn8nWtVs7ylS2TdxZMjD4o7tZTMWF47zqF%2FSjSTLaIPYf0u%2FO%2BobBgIRJqxcRvkJ50fmIcyzQuXzzsPOs%2B5L10%2FcyyF%2BNM%2BKWgiotiTeDbcYbRmXHGZJXXAgENtQPUQ%2Bv7LFjVwrr56jDWB3EDBJWjo1vdwHlMq2ySrVUY2suGLSxfE4XV6TR8AiiY8k4aug%2FqVWJC2VfG4JXEIhn97%2F00fhnV4RKY6Mc4JFw4bxfeA%2Fq7WEaNrjXE%2FSAUkpzcSeiezNpVUzUytIbd80TWE6SCkVyavPqMXjHPfIGeAnkYNTLy6Akbjo9Ia104ikiMGAD%2BHIdq6rs8AIB0oPwUXEG00IMr0PlCX4j%2F6X2NaQkNGmxYZzqc4kIIbSlCn1hQ3fn8Z5VsrXhjDFEI%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200910T223022Z&X-Amz-SignedHeaders=host&X-Amz-Expires=300&X-Amz-Credential=ASIASVA5GJL5QEFTLG43%2F20200910%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=a2e06793152e6509702fffc738441769e1d3bca2d3aad9f960fdd2f58d016f22"
    # url=r"https://training-images-team-a.s3.us-east-1.amazonaws.com/Stories%20Dataset/Transcribed%20Stories/52--/5205/Photo%205205%20pg1.jpg?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEF4aCXVzLWVhc3QtMSJHMEUCIQD%2FpbNQcSJZ9J9vZ%2BudRiuxnmH%2FRbhTDJd1J5GxtJQhrAIgRSGrwRAr1flqzvVCXnAjaGu177pokj%2BYrTpnZDQHaYYq2wIIZxABGgwxODI1OTczMzk4OTkiDFhmeEylcX%2BDpFMxQCq4AqR%2BvskXD2zDsOKjFQ86oS8nt8xEJFoO%2B1im6JBVwpl9gW7BxFxxAoWSr1jj2uQrEgAF9k6UhAxHErtq6cVUOWmdw96dMKEQOdSFHmjjb%2BvRJ6WS7OzxgIOEYYXml9Dv7h5SG6BmMejVwnlc0%2BpdDSX45Hi9s%2FiuYLFgdjxYvodKPYDX4YxGm7CJkdd87ZF4dlS85hwijp3qPqX7rsLgSUcpbGpCR6D9rArIZP2NHdE%2B%2BP1TVIDOI57AQJrUYQbj9kFp8q66YiVG%2BXHgCVB2i3u1YDzEag99AaawQuG8n3i5wTBWx6SnMZsDEp2ZB31WMRH5LNVawb8zQIChQ5mBiD3gcIFS3lb0zw0C1ykYrs%2BM4gYV%2B4Ds3Nd6xB%2BruKRhCBkGhnz6nlBXSM0Z%2F8fbNKRuAJXp7iCKFDDeuur6BTqwAgAic9a69kn8nWtVs7ylS2TdxZMjD4o7tZTMWF47zqF%2FSjSTLaIPYf0u%2FO%2BobBgIRJqxcRvkJ50fmIcyzQuXzzsPOs%2B5L10%2FcyyF%2BNM%2BKWgiotiTeDbcYbRmXHGZJXXAgENtQPUQ%2Bv7LFjVwrr56jDWB3EDBJWjo1vdwHlMq2ySrVUY2suGLSxfE4XV6TR8AiiY8k4aug%2FqVWJC2VfG4JXEIhn97%2F00fhnV4RKY6Mc4JFw4bxfeA%2Fq7WEaNrjXE%2FSAUkpzcSeiezNpVUzUytIbd80TWE6SCkVyavPqMXjHPfIGeAnkYNTLy6Akbjo9Ia104ikiMGAD%2BHIdq6rs8AIB0oPwUXEG00IMr0PlCX4j%2F6X2NaQkNGmxYZzqc4kIIbSlCn1hQ3fn8Z5VsrXhjDFEI%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20200910T223259Z&X-Amz-SignedHeaders=host&X-Amz-Expires=299&X-Amz-Credential=ASIASVA5GJL5QEFTLG43%2F20200910%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=f3708068520ee437525a422464ece9a85332e18ec13d44ab4b19d71416dc9172"
    # set_endpoint(url)
