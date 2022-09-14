from app.models import Student
from django.db.models import Q

def etl(csv_file, tutor):
    """Soon to be a class"""

    # InMemoryUploadedFile
    # 
    # for line in csv_file.readlines():
    #     print(line.decode('utf-8').split(',')) 
    # ['first_name', 'last_name', 'address', 'education_level ', 'phone_number ', 'email ', 'discord_nick', 'facebook_profile ', 'facebook_psid \r\n']  
    # ['jan', 'kowalski', 'ul. długa 42', '1 Licuem', ' 123456789 ', 'jk@wp.pl', '', '', '\r\n']
    # ['maciek', 'noob', 'ul. szeroka 23', '2 Liceum', '    123123123   ', 'mk@wp.pl', '  Goblin#1233', '', ''123123123\r\n']
    #  
    # output from algorythm abowe, time to list comprehention


    try:
        # extract 
        dirty_data = [line.decode('utf-8').split(',') for line in csv_file.readlines()]
        clean_headers = strip_remove_rn(dirty_data[0]) # headers

        # transform
        clean_data = []
        for student_info in dirty_data[1:]: 
            # Capitalize data from csv, strip from white space and remove '\r\n'
            clean_info = capitalize_strip_remove_rn(student_info)
            clean_data.append(map_keys_to_headers(zip(clean_headers, clean_info)))

    except:
        return 'Error during extracting CSV'

    feedback = []
    # load
    for student_info in clean_data:

        # check if student exists by email, discord, phone because they are uniqe
        if Student.objects.filter(Q(email=student_info['email']) | Q(discord_nick=student_info['discord_nick']) | Q(phone_number=student_info['phone_number'])).exists():
            feedback.append(f"{student_info['first_name']} {student_info['last_name']} already exists.")
            continue

        Student.objects.create(**student_info, tutor=tutor)
        feedback.append(f"{student_info['first_name']} {student_info['last_name']} created.")

    return feedback


def capitalize_strip_remove_rn(arr: list) -> list:
    return (list(map(lambda x: x.capitalize().strip(), arr)) + [arr[-1].replace('\r\n', '').rstrip()])


def strip_remove_rn(arr: list) -> list:
    return (list(map(lambda x: x.strip(), arr)) + [arr[-1].replace('\r\n', '').rstrip()])

def map_keys_to_headers(zipped_arr: zip) -> dict:
    return {x[0]:x[1] for x in zipped_arr}
