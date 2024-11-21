import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coderr_project.settings')
django.setup()

import random
from django.contrib.auth.models import User
from auth_app.models import CustomerProfile, BusinessProfile
from freelancer_platform_app.models import Offer, OfferDetail, Order, Review

def add_dummy_data():

    users = [
        User.objects.create_user(username='andrey', password='asdasd', email='andreyk@gast.de', first_name='Andrey', last_name='Kaufmann'),
        User.objects.create_user(username='MaxM', password='123456789', email='max@mail.com', first_name='Max', last_name='Mustermann'),
        User.objects.create_user(username='SofiaM', password='123456789', email='sofiam@gmail.com', first_name='Sofia', last_name='Müller'),
        User.objects.create_user(username='AntonM', password='123456789', email='antom@gmail.com', first_name='Anton', last_name='Mayer'),
        User.objects.create_user(username='AnjaS', password='123456789', email='schulz@hotmail.com', first_name='Anja', last_name='Schulz'),
        User.objects.create_user(username='kevin', password='asdasd', email='kevint@gast.de', first_name='Kevin', last_name='Theisen'),
        User.objects.create_user(username='BenediktZ', password='123456789', email='benedikt@gmail.com', first_name='Benedikt', last_name='Ziegler'),
        User.objects.create_user(username='DavidE', password='123456789', email='davidberg@gmail.com', first_name='David', last_name='Eisenberg'),
        User.objects.create_user(username='EvaF', password='123456789', email='eva@gmail.com', first_name='Eva', last_name='Fischer'),
        User.objects.create_user(username='EmmanuelM', password='123456789', email='emmanuelma@gmail.com', first_name='Emmanuel', last_name='Mauer'),
        User.objects.create_user(username='MarcelB', password='123456789', email='bauer@gmail.com', first_name='Marcel', last_name='Bauer'),
        User.objects.create_user(username='TatjanaW', password='123456789', email='wolf@gmail.com', first_name='Tatjana', last_name='Wolf'),
    ]

    print('Users added to database.')

    customer_profiles = [
        CustomerProfile.objects.create(user=users[0]),
        CustomerProfile.objects.create(user=users[1]),
        CustomerProfile.objects.create(user=users[2]),
        CustomerProfile.objects.create(user=users[3]),
        CustomerProfile.objects.create(user=users[4]),
    ]

    print('Customer-Profiles added to database.')

    business_profiles = [
        BusinessProfile.objects.create(user=users[5], location='Koblenz', tel='03284561', description='Wir entwickeln Ihre Unternehmens-Webseite inklusive modernem Design.', working_hours='9-17'),
        BusinessProfile.objects.create(user=users[6], location='Mayen', tel='06516546', description='Ein kleines aber feines Web-Entwicklungs-Unternehmen.', working_hours='7-15'),
        BusinessProfile.objects.create(user=users[7], location='Cochem', tel='035416841', description='IT-Engineering und Service', working_hours='8-16'),
        BusinessProfile.objects.create(user=users[8], location='Koblenz', tel='03541681', description='IT-Spezialisten entwerfen Ihre ansprechende und benutzerfreundliche Web-App', working_hours='9-17'),
        BusinessProfile.objects.create(user=users[9], location='Berlin', tel='068443', description='Wir kreieren Ihre digitale Welt.', working_hours='10-18'),
        BusinessProfile.objects.create(user=users[10], location='München', tel='06876413', description='Wir bauen die Zukunft der IT.', working_hours='8-16'),
        BusinessProfile.objects.create(user=users[11], location='Osnabrück', tel='064874613', description='Exzellente Software Entwicklung', working_hours='9-17'),
    ]

    print('Business-Profiles added to database.')

    offers = [
        Offer.objects.create(user=users[5], title='Webdesign', description='Ansprechendes Design für Ihre professionelle Webseite.'),
        Offer.objects.create(user=users[5], title='Komplettpaket Webseite', description='Ihre professionelle Webseite mit ansprechendem Design.'),
        Offer.objects.create(user=users[6], title='Website Design A', description='Professionelles Website-Design Vorlage A.'),
        Offer.objects.create(user=users[6], title='Website Design B', description='Professionelles Website-Design Vorlage B.'),
        Offer.objects.create(user=users[7], title='Webseite', description='Entwicklung Ihrer persönlichen Webseite.'),
        Offer.objects.create(user=users[7], title='Hosting und Wartung', description='Hosting und Wartung Ihrer Webseite.'),
        Offer.objects.create(user=users[8], title='Web-App', description='Ihre professionelle Web-App.'),
        Offer.objects.create(user=users[8], title='Web-App Zusatzfunktionen', description='Zusatzfunktionen für Ihre Web-App.'),
        Offer.objects.create(user=users[9], title='Frontend', description='Ihre persönliche Webseite.'),
        Offer.objects.create(user=users[9], title='Backend', description='Ein Backend zu Ihrer Webseite.'),
        Offer.objects.create(user=users[10], title='Design & Frontend', description='Design und Frontend für Ihre Unternehmens-Website.'),
        Offer.objects.create(user=users[10], title='Hosting & Backend', description='Hosting und Backend für Ihre Unternehmens-Website.'),
        Offer.objects.create(user=users[11], title='Professionelles Design', description='Designvorlage für Ihre Webseite.'),
        Offer.objects.create(user=users[11], title='Professionelle Webseite', description='Komplette Webseite mit Design und Frontend.'),
    ]

    print('Offers added to database.')

    basic_prices = []
    basic_delivery_time = []
    revisions_data = []
    offer_details_ids = []

    for offer in offers:
        basic_prices.append(random.randrange(5, 30) * 10)
        basic_delivery_time.append(random.randrange(1, 7))
        revisions_data.append([random.randrange(-1, 9), random.randrange(-1, 9), random.randrange(-1, 9)])
        offer_details_ids.append(random.randrange(1, len(offers) * 3 + 1))


    details_data = [
        # Webdesign
        [
            {"title": "Basis-Webseiten-Design", "features": ["Basis-Design"]},
            {"title": "Standard-Webseiten-Design", "features": ["Basis-Design", "Responsive-Design"]},
            {"title": "Premium-Webseiten-Design", "features": ["Basis-Design", "Responsive-Design", "Besondere Designwünsche"]}
        ],
        # Komplettpaket Webseite
        [
            {"title": "Basis-Webseiten-Entwicklung", "features": ["Homepage", "Design"]},
            {"title": "Standard-Webseiten-Entwicklung", "features": ["Homepage", "Hosting", "Design", "Responsive-Design"]},
            {"title": "Premium-Webseiten-Entwicklung", "features": ["Homepage", "Hosting", "Wartung", "Design", "Responsive-Design", "Besondere Designwünsche"]}
        ],
        # Website Design A
        [
            {"title": "Basis-Webseite A", "features": ["Design nach Vorlage A"]},
            {"title": "Standard-Webseite A", "features": ["Design nach Vorlage A", "Responsive-Design"]},
            {"title": "Premium-Webseite A", "features": ["Design nach Vorlage A", "Responsive-Design", "Änderungen zur Vorlage"]}
        ],
        # Website Design B
        [
            {"title": "Basis-Webseite B", "features": ["Design nach Vorlage B"]},
            {"title": "Standard-Webseite B", "features": ["Design nach Vorlage B", "Responsive-Design"]},
            {"title": "Premium-Webseite B", "features": ["Design nach Vorlage B", "Responsive-Design", "Änderungen zur Vorlage"]}
        ],
        # Webseite
        [
            {"title": "Homepage-Entwicklung", "features": ["Design nach Kundenwunsch", "Frontend"]},
            {"title": "Homepage-Entwicklung Plus", "features": ["Design nach Kundenwunsch", "Frontend", "Responsive-Design"]},
            {"title": "Homepage-Entwicklung Ultra", "features": ["Design nach Kundenwunsch", "Frontend", "Responsive-Design", "Backend"]}
        ],
        # Hosting und Wartung
        [
            {"title": "Basis-Hosting", "features": ["Frontend bis 1000 gleichzeitige Benutzer"]},
            {"title": "Hosting Plus", "features": ["Frontend bis 10000 gleichzeitige Benutzer", "Wartung und Service"]},
            {"title": "Hosting Ultra", "features": ["Frontend bis 10000 gleichzeitige Benutzer", "Backend", "Wartung und Service"]}
        ],
        # Web-App
        [
            {"title": "Design only", "features": ["Design"]},
            {"title": "Website", "features": ["Design", "Frontend", "Backend"]},
            {"title": "with Mobile", "features": ["Design", "Frontend", "Backend", "Mobile-Optimization"]}
        ],
        # Web-App Zusatzfunktionen
        [
            {"title": "Hosting", "features": ["Hosting"]},
            {"title": "Service", "features": ["Maintenance", "Service"]},
            {"title": "Hosting and Service", "features": ["Hosting", "Maintenance", "Service"]}
        ],
        # Frontend
        [
            {"title": "Basis-Frontend", "features": ["Design", "Frontend"]},
            {"title": "Standard-Frontend", "features": ["Design", "Frontend", "Responsive"]},
            {"title": "Premium-Frontend", "features": ["Design", "Frontend", "Responsive", "Hosting"]}
        ],
        # Backend
        [
            {"title": "Basis-Backend", "features": ["Backend", "Authentication"]},
            {"title": "Standard-Backend", "features": ["Backend", "Authentication", "Eigene Funktionen"]},
            {"title": "Premium-Backend", "features": ["Backend", "Authentication", "Eigene Funktionen", "Hosting"]}
        ],
        # Design & Frontend
        [
            {"title": "Design", "features": ["Design"]},
            {"title": "Komplettes Frontend", "features": ["Design", "Frontend", "Responsive"]},
            {"title": "Premium-Frontend", "features": ["Design", "Frontend", "Responsive", "SEO", "Wartung und Updates"]}
        ],
        # Hosting & Backend
        [
            {"title": "Hosting", "features": ["Hosting Frontend"]},
            {"title": "Backend", "features": ["Backend"]},
            {"title": "Premium-Paket", "features": ["Hosting Frontend", "Backend", "Hosting Backend", "Premium-Service"]}
        ],
        # Professionelles Design
        [
            {"title": "Design-Upgrade", "features": ["Upgrade von bestehendem Design"]},
            {"title": "Standard-Design", "features": ["neues Design nach Absprache"]},
            {"title": "Premium-Design", "features": ["neues Design nach Absprache", "Responsive-Design"]}
        ],
        # Professionelle Webseite
        [
            {"title": "Webseiten-Upgrade", "features": ["Upgrade von bestehender Webseite"]},
            {"title": "Standard-Webseite", "features": ["neue Webseite nach Absprache"]},
            {"title": "Premium-Webseite", "features": ["neue Webseite nach Absprache", "Mobile-Optimierung"]}
        ],
    ]

    for offer_idx, offer_details in enumerate(details_data):
        offer = offers[offer_idx]
        basic_price = basic_prices[offer_idx]
        for details_idx, details in enumerate(offer_details):
            if details_idx == 0:
                price = basic_price
                delivery_time_in_days = basic_delivery_time[offer_idx]
                revisions = revisions_data[offer_idx][details_idx]
                offer_type = "basic"
            if details_idx == 1:
                price = basic_price * 2
                delivery_time_in_days = basic_delivery_time[offer_idx] * 2
                revisions = revisions_data[offer_idx][details_idx]
                offer_type = "standard"
            if details_idx == 2:
                price = basic_price * 2 + 200
                delivery_time_in_days = basic_delivery_time[offer_idx] * 3
                revisions = revisions_data[offer_idx][details_idx]
                offer_type = "premium"
            OfferDetail.objects.create(offer=offer, price=price, delivery_time_in_days=delivery_time_in_days, revisions=revisions, offer_type=offer_type, **details)

    print('Offer-Details added to database.')

    orders = [
        Order.objects.create(customer_user=users[0], status='in_progress', offer_details=OfferDetail.objects.get(pk=offer_details_ids[0])),
        Order.objects.create(customer_user=users[0], status='completed', offer_details=OfferDetail.objects.get(pk=offer_details_ids[1])),
        Order.objects.create(customer_user=users[0], status='cancelled', offer_details=OfferDetail.objects.get(pk=offer_details_ids[2])),
        Order.objects.create(customer_user=users[1], status='in_progress', offer_details=OfferDetail.objects.get(pk=offer_details_ids[3])),
        Order.objects.create(customer_user=users[1], status='completed', offer_details=OfferDetail.objects.get(pk=offer_details_ids[4])),
        Order.objects.create(customer_user=users[1], status='cancelled', offer_details=OfferDetail.objects.get(pk=offer_details_ids[5])),
        Order.objects.create(customer_user=users[2], status='in_progress', offer_details=OfferDetail.objects.get(pk=offer_details_ids[6])),
        Order.objects.create(customer_user=users[2], status='completed', offer_details=OfferDetail.objects.get(pk=offer_details_ids[7])),
        Order.objects.create(customer_user=users[2], status='cancelled', offer_details=OfferDetail.objects.get(pk=offer_details_ids[8])),
        Order.objects.create(customer_user=users[3], status='in_progress', offer_details=OfferDetail.objects.get(pk=offer_details_ids[9])),
        Order.objects.create(customer_user=users[3], status='completed', offer_details=OfferDetail.objects.get(pk=offer_details_ids[10])),
        Order.objects.create(customer_user=users[3], status='cancelled', offer_details=OfferDetail.objects.get(pk=offer_details_ids[11])),
        Order.objects.create(customer_user=users[4], status='in_progress', offer_details=OfferDetail.objects.get(pk=offer_details_ids[12])),
        Order.objects.create(customer_user=users[4], status='completed', offer_details=OfferDetail.objects.get(pk=offer_details_ids[13])),
        Order.objects.create(customer_user=users[4], status='cancelled', offer_details=OfferDetail.objects.get(pk=offer_details_ids[0])),
    ]

    print('Orders added to database.')

    reviews = [
        Review.objects.create(reviewer=users[0], business_user=users[5], rating=3, description='Gute Arbeit, es hat leider 3 Tage länger gedauert, als angegeben.'),
        Review.objects.create(reviewer=users[0], business_user=users[6], rating=5, description='Sehr guter Job. Rundum zufrieden'),
        Review.objects.create(reviewer=users[1], business_user=users[5], rating=5, description='Super umgesetzt und pünktlich geliefert.'),
        Review.objects.create(reviewer=users[1], business_user=users[7], rating=4, description='Im großen und Ganzen sehr gut gelungen, nur bei der Einhaltung unserer Designvorgaben ist noch etwas Luft nach oben.'),
        Review.objects.create(reviewer=users[2], business_user=users[5], rating=3, description='Die Webseite wurde anfangs nicht ganz so umgesetzt, wie besprochen. Nacharbeit war nötig.'),
        Review.objects.create(reviewer=users[2], business_user=users[8], rating=5, description='Unsere Web-App ist sehr gelungen und hat alle Features, die wir bestellt haben.'),
        Review.objects.create(reviewer=users[3], business_user=users[9], rating=1, description='Auf Nachfrage stellte sich heraus, dass die Bestellung untergegangen ist. Wir mussten sie dann stornieren und bei einem anderen Anbieter als Eilauftrag bestellen.'),
        Review.objects.create(reviewer=users[3], business_user=users[10], rating=3,
                              description='Das Ergebnis war gut und kam pünktlich. Die Kommunikation mit dem Unternehmen gestaltete sich jedoch schwierig und mein Ansprechpartner wurde über die Zeit der Umsetzung des Projektes zunehmend unfreundlicher.'),
        Review.objects.create(reviewer=users[4], business_user=users[11], rating=5, description='Nichts zu meckern, unser Projekt wurde sehr schön umgesetzt.'),
        Review.objects.create(reviewer=users[4], business_user=users[9], rating=4, description='Top Job!')
    ]

    print('Reviews added to database.')

    print('Job done.')


if __name__ == '__main__':
    add_dummy_data()