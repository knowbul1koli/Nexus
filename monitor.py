import requests
from models import db, Site

def check_sites(app):
    with app.app_context():
        sites = Site.query.filter_by(is_approved=True).all()
        for site in sites:
            try:
                response = requests.get(site.url, timeout=5)
                if response.status_code == 200:
                    site.status = 'online'
                else:
                    site.status = 'offline'
            except requests.RequestException:
                site.status = 'offline'
        db.session.commit()