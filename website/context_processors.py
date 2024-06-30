from django.conf import settings
from django.http import HttpRequest

def load_global_var(request):
    dr_email = 'parham.davarii@gmail.com'
    dr_phone = '+989033103516'
    dr_instagram = 'https://www.instagram.com/dr.hossein.rabbani/'
    clinic_instagram = 'https://www.instagram.com/dr.hossein.rabbani/'
    clinic_addr = 'Unit 1, 8th Floor, Jaam-e-Jam Complex, East Pahlavan St., Ahvaz, Khuzestan, Iran'
    welcome_msg = "Follow us on social media for updates, personalized care, and to make reservation!"

    return {'dr_email': dr_email,
            'dr_phone': dr_phone,
            'dr_instagram': dr_instagram,
            'clinic_addr': clinic_addr,
            'clinic_instagram': clinic_instagram,
            'welcome_msg': welcome_msg,
            }
 
def google_analytics(request: HttpRequest):
 
    return {
        'GA_KEY': settings.GOOGLE_ANALYTICS_KEY,
    }