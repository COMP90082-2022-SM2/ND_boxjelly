# This file downloads asgmts and save them to local address

from canvasapi import Canvas
import webbrowser as web
import io
import requests
from tqdm import tqdm
from .utils import is_windows

API_URL = "https://canvas.lms.unimelb.edu.au" # an example of unimelb
API_KEY = "KEY"
course_name = "EXMAPLE"
assignment_name = "EXAMPLE"

canvas = Canvas(API_URL, API_KEY)

user = canvas.get_user(212369) # an example of mine

courses = user.get_courses() # get all course
#for i in courses:
#    try:
#        print(i)
#    except:       # some course do not have course_code or course_name
#        continue

# find the course
#for i in courses:
#    if i.name == course_name:
#        course = i
#        break

course = courses[4]
course_id = str(course.id)
asgmts = course.get_assignments() # get all asgmts
# find the asgmt
#for i in asgmts:
#    print(i)
#for i in asgmts:
#    if i.name == assignment_name:
#        asgmt = i
#        break

asgmt = asgmts[1]
asgmt_id = str(asgmt.id)

files = course.get_files() # get all files for this asgmt

#zip_url = "https://canvas.lms.unimelb.edu.au/courses/"+course_id+"/assignments/"+asgmt_id+"/submissions?zip=1"
test_url = "https://canvas.lms.unimelb.edu.au/courses/126771/assignments/318533/submissions/212369?download=12554482"

web.open(test_url, autoraise = False) # open the website and download the file

#def download_pdf(save_path,pdf_name,pdf_url):
#    send_headers = {
#        "User-Agent": "PostmanRuntime/7.20.1",
#        "Connection": "keep-alive",
#        "Accept": "*/*"}
#    response = requests.get(pdf_url, headers=send_headers)
#    bytes_io = io.BytesIO(response.content)
#    with open(save_path + "%s.html" % pdf_name, mode='wb') as f:
#        f.write(bytes_io.getvalue())

#if __name__ == '__main__':
#    save_path = '/Users/sy/Desktop/'
#    pdf_name='asgmt'
#    pdf_url=test_url
#    download_pdf(save_path, pdf_name, pdf_url)


def download_file(url, desc, filename, file_size):
    with requests.get(url, stream=True) as r:

        with open(filename + '.canvas_tmp', 'wb') as fp:
            tqdm(
                total=file_size, unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=desc, bar_format='{l_bar}{bar}{r_bar}', ascii=is_windows(),
                leave=False
            )