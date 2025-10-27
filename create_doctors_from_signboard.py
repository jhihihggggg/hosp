#!/usr/bin/env python
"""
Create doctors matching the Universal Health Services & Diagnostic Center signboard
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diagcenter.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Doctor data from the signboard images
doctors_data = [
    {
        'first_name': 'শাকেব',
        'last_name': 'সুলতানা',
        'username': 'dr_shakeb_sultana',
        'specialization': 'ক্যান্সার বিশেষজ্ঞ',
        'qualification': '''এমবিবিএস, এম. ফিল (রেডিয়েশন অনকোলাজ)
পিজিটি (মেডিসিন), ডিএমইউ (ঢাকা)''',
        'email': 'dr.shakeb@universalhealthbd.com',
        'timing': 'প্রতিদিন সকাল ১০টা হইতে রাত ৬টা পর্যন্ত',
    },
    {
        'first_name': 'আয়েশা',
        'last_name': 'ছিদ্দিকা',
        'username': 'dr_ayesha_siddika',
        'specialization': 'প্রসূতি, গাইনী, মেডিসিন, হরমোন ও ডায়াবেটিস রোগ চিকিৎসক',
        'qualification': '''এমবিবিএস (রাজ), বি.সি.এস (স্বাস্থ্য)
এফ সি জি পি (এফপি), মেডিসিন (এন্ডোক্রাইনোলজি)
মেডিকেল অফিসার, উপজেলা স্বাস্থ্য কমপ্লেক্স, পত্নীতলা, নওগাঁ।''',
        'email': 'dr.ayesha@universalhealthbd.com',
        'timing': 'প্রতিদিন বিকাল ৩টা থেকে রাত ৮টা পর্যন্ত',
    },
    {
        'first_name': 'খাজা আমিরুল',
        'last_name': 'ইসলাম',
        'username': 'dr_khaja_amirul',
        'specialization': 'থ্যালাসেমিয়া ও রক্ত রোগ বিশেষজ্ঞ',
        'qualification': '''এমবিবিএস, এমডি
ফেলো- ইউরোপিয়ান হেমাটোলজি এসোসিয়েশন মাস্টার কোর্স
সহকারী অধ্যাপক ও বিভাগীয় প্রধান
টিএমএসএস হেমাটোলজি ও বোন ম্যারো ট্রান্সপ্লান্ট সেন্টার''',
        'email': 'dr.khaja@universalhealthbd.com',
        'timing': 'প্রতিদিন সকাল ১০টা হইতে রাত ৬টা পর্যন্ত',
    },
    {
        'first_name': 'এস.এম. খালিদ',
        'last_name': 'সাইফূল্লাহ',
        'username': 'dr_khalid_saifullah',
        'specialization': 'মেডিসিন, হাড়জোড়া, বাত-ব্যাথা, সার্জারি ও ডায়াবেটিস রোগ অভিজ্ঞ এবং সোনোলোজিস্ট',
        'qualification': '''এমবিবিএস (রাজ), বি.সি.এস (স্বাস্থ্য)
এফ.সি.পি.এস (সার্জারী ট্রেনি), সি.পি.ডি (বারডেম)
আই, এম, সি, আই (শিশু) পিজিটি (অর্থো-সার্জারী)
উপজেলা স্বাস্থ্য ও পঃপঃ কর্মকর্তা, পত্নীতলা, নওগাঁ।''',
        'email': 'dr.khalid@universalhealthbd.com',
        'timing': 'নিয়মিত প্রতি বৃহস্পতিবার সন্ধ্যা ৭টা হইতে রাত ৯টা পর্যন্ত',
    },
]

def create_doctors():
    """Create doctor users"""
    print("Creating doctors from Universal Health Services signboard...\n")
    
    for doctor_data in doctors_data:
        username = doctor_data['username']
        
        # Check if doctor already exists
        if User.objects.filter(username=username).exists():
            print(f"✓ Doctor {username} already exists, updating...")
            doctor = User.objects.get(username=username)
        else:
            print(f"+ Creating new doctor: {username}")
            doctor = User.objects.create_user(
                username=username,
                password='doctor123',  # Default password
                email=doctor_data['email'],
            )
        
        # Update fields
        doctor.first_name = doctor_data['first_name']
        doctor.last_name = doctor_data['last_name']
        doctor.role = 'DOCTOR'
        doctor.specialization = doctor_data['specialization']
        doctor.qualification = doctor_data['qualification']
        doctor.is_active = True
        doctor.save()
        
        print(f"  Name: ডাঃ {doctor.get_full_name()}")
        print(f"  Specialty: {doctor.specialization}")
        print(f"  Email: {doctor.email}")
        print()
    
    print(f"\n✅ Successfully created/updated {len(doctors_data)} doctors!")
    print("\nAll doctors are ready to see patients at:")
    print("📍 Universal Health Services & Diagnostic Center")
    print("📍 ইউনিভার্সাল হেলথ সার্ভিসেস এন্ড ডায়াগনস্টিক সেন্টার")
    print("📍 সাদিয়া প্যালেস, বাজার রোড, নজিপুর সরদারপাড়া মোড়, নজিপুর পৌরসদ, পত্নীতলা, নওগাঁ")
    print("📞 মোবাইল: ০১৭৩২-৮৫৩৩০৩")
    print("\n⏰ রোগী দেখার সময় (প্রতিটি ডাক্তারের জন্য আলাদা):")
    for doctor_data in doctors_data:
        print(f"   - ডাঃ {doctor_data['first_name']} {doctor_data['last_name']}: {doctor_data['timing']}")

if __name__ == '__main__':
    create_doctors()
