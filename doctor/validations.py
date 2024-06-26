import re
from django.contrib import messages
from django.contrib.messages import constants


def validate_doctor_data(request_data):
    validation_errors = {}
    # request post
    required_post_fields = [
        'medical_reservation_registration',
        'doctor_name',
        'address_code',
        'street',
        'neighborhood',
        'house_number',
        'specialty',
        'consultation_fee'
    ]

    data_post = request_data.POST
    data_post_keys = [keys for keys in data_post.keys()]
    numeric_fields = ['house_number', 'consultation_fee', 'specialty']
    # post request validators
    required_post_fields_not_found = [nfpf for nfpf in required_post_fields if nfpf not in data_post_keys]
    empty_post_fields = [epf for epf in required_post_fields if data_post[epf] == '']
    
    invalid_integer_fields = [
        field_name for field_name in numeric_fields if not re.findall((r"^-?\d+\Z"), data_post[field_name])
        ]
    
    
    # request files
    required_file_fields = [
        'profile_picture',
        'medical_identity_card',
        'medical_identification_card',
    ]

    data_files = request_data.FILES
    data_file_keys = data_files.keys()
    
    # files request validators
    required_file_fields_not_found = [nfff for nfff in required_file_fields if nfff not in data_file_keys]
    invalid_file_extensions = [file for file in data_files.values() if not file.name.endswith(('.jpg', '.png', 'jpeg'))]

    validation_errors['required_fields_not_found'] = required_post_fields_not_found + required_file_fields_not_found
    validation_errors['empty_fields'] = empty_post_fields
    validation_errors['invalid_integer_fields'] = invalid_integer_fields
    validation_errors['invalid_file_extension_fields'] = invalid_file_extensions
        
    

    validation_error_checkers = [topic for topic in validation_errors.keys() if not validation_errors[topic] == []]
    
    if not validation_error_checkers:
        return True
    else:
        all_errors = {}
        for topic_error in validation_error_checkers:
            for err in validation_errors[topic_error]:
                if topic_error not in all_errors.keys():
                    all_errors[topic_error] = []
                    all_errors[topic_error].append(str(err).capitalize())
                else:
                    all_errors[topic_error].append(str(err).capitalize())
        topics = [topic for topic in all_errors.keys()]
        for topic in topics:
            messages.add_message(request_data, constants.ERROR, 
                f'{topic.replace('_', ' ')} => {str(all_errors[topic]).replace("'", ' '
                ).replace('[', '').replace(']', ''
                ).replace('_', ' ')}')
            
        return False


def validate_add_document_request_data(request):
    title = request.POST.get('title')
    document = request.FILES.get('document')
    validation_errors = {'title': '', 'document': ''}

    if not title:
        validation_errors['title'] = 'invalid'
    if not document:
        validation_errors['document'] = 'invalid'
    else:
        if not document.name.endswith(('.pdf', '.doc', '.docx', '.txt')):
            validation_errors['document'] = 'invalid'

    if validation_errors['title'] == '' and validation_errors['document'] == '':
        return 'validated'
    return validation_errors
    