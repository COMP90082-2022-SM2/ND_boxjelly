from canvasapi import Canvas
import webbrowser as web

# connect to Canvas Api
API_URL = "https://canvas.lms.unimelb.edu.au" # an example of unimelb
API_KEY = "KEY"
canvas = Canvas(API_URL, API_KEY)

#get the user id
user_id = canvas.get_current_user().id
user = canvas.get_user(user_id)

# get the course name and the assignment name from the keyboard
course_name = input("The course name is:")
assignment_name = input("The assignment name is:")

# get the course id
courses = user.get_courses() # get all course
course = None
for i in courses:
    try:
        if course_name in i.name:
            course = i
            break
    except:       # some course do not have course_code or course_name
        continue
if course == None:
    print("Wrong course name!")
course_id = str(course.id)

# get the asgmt id
asgmts = course.get_assignments() # get all asgmts
# find the asgmt
asgmt = None
for i in asgmts:
    if assignment_name in i.name:
        asgmt = i
        break
if asgmt == None:
    print("Wrong assignment name!")
asgmt_id = str(asgmt.id)

print(asgmt.submissions_download_url)

zip_url = "https://canvas.lms.unimelb.edu.au/courses/"+course_id+"/assignments/"+asgmt_id+"/submissions?zip=1"

# web.open(zip_url, autoraise = False) # open the website and download the file

redirection_url = ""
annotated_pdf_url = redirection_url[0:-5]+'annotated.pdf'
print(annotated_pdf_url)
r = requests.post(annotated_pdf_url)
check_url = annotated_pdf_url+'/is_ready'
while requests.get(check_url).content == '{"ready":false}':
    sleep(1)
r = requests.get(annotated_pdf_url)
open('annotated.pdf', 'wb').write(r.content)
