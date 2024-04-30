from .models import Doctor
import re

def is_doctor(user):
    if user.is_authenticated:
        return Doctor.objects.filter(user=user).exists()
    else:
        return None
    
def validate_doctor_data(request_data):
    
    validation_errors = {}
    print(request_data.POST)
    print(request_data.FILES)
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
    required_post_fields_not_found = [nfpf for nfpf in required_post_fields if nfpf not in data_post_keys]
    empty_post_fields = [epf for epf in required_post_fields if data_post[epf] == '']
    numeric_fields = ['house_number', 'consultation_fee', 'specialty']
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
    required_file_fields_not_found = [nfff for nfff in required_file_fields if nfff not in data_file_keys]
    invalid_file_extensions = []

    for file in data_files.values():
        if not file.name.endswith(('.jpg', '.png', 'jpeg')):
            invalid_file_extensions.append(file.name)

    validation_errors['required_fields_not_found'] = required_post_fields_not_found + required_file_fields_not_found
    validation_errors['empty_fields'] = empty_post_fields
    validation_errors['invalid_integer_fields'] = invalid_integer_fields
    validation_errors['invalid_file_extension_fields'] = invalid_file_extensions
        
    if validation_errors['required_fields_not_found'] == [] \
          and validation_errors['empty_fields'] == []  \
          and validation_errors['invalid_integer_fields'] == [] \
          and validation_errors['invalid_file_extension_fields'] == []:
        return None
    
    return validation_errors
