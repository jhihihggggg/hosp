# Add doctor schedule and timing information to User model
# Each doctor will have specific working days and times

DOCTOR_SCHEDULES = {
    'dr_shakeb_sultana': {
        'days': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        'time': '10:00-18:00',  # 10 AM to 6 PM
        'duration': 15,  # 15 minutes per patient
    },
    'dr_ayesha_siddika': {
        'days': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY', 'SUNDAY'],
        'time': '15:00-20:00',  # 3 PM to 8 PM
        'duration': 20,  # 20 minutes per patient
    },
    'dr_khaja_amirul': {
        'days': ['MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY', 'SATURDAY'],
        'time': '10:00-18:00',  # 10 AM to 6 PM
        'duration': 20,
    },
    'dr_khalid_saifullah': {
        'days': ['THURSDAY'],  # Only Thursday
        'time': '19:00-21:00',  # 7 PM to 9 PM
        'duration': 15,
    },
}
