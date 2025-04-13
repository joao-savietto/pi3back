from celery import shared_task
from celery.exceptions import MaxRetriesExceededError
from django.core.exceptions import ObjectDoesNotExist
from .scrapper import TalentScrapper
from ..models import Applicant
import traceback


@shared_task(bind=True, max_retries=3)
def scrape_and_update_applicant(
    self, linkedin_url_profile, username, password, applicant_id
):
    try:
        # Initialize the scraper
        print("Starting scrapper task with params:")
        print("linkedin_url_profile:", linkedin_url_profile)
        print("username:", username)
        print("password:", password)
        print("applicant_id:", applicant_id)
        scraper = TalentScrapper(linkedin_url_profile, username, password)
        scraper.run()
        print("Completed scrap for:", scraper.name)
        # Get the applicant instance
        applicant = Applicant.objects.get(id=applicant_id)

        # Update applicant data
        applicant.about = scraper.about
        applicant.name = scraper.name
        applicant.experiences = scraper.experiences
        applicant.educations = scraper.educations
        applicant.interests = scraper.interests
        applicant.accomplishments = scraper.accomplishments
        applicant.contacts = scraper.contacts

        # Save the updated applicant
        applicant.save()
        print("saved")
    except ObjectDoesNotExist:
        # If applicant doesn't exist, no need to retry
        raise
    except Exception as exc:
        try:
            print(traceback.format_exc())
            # Retry the task with exponential backoff
            # self.retry(exc=exc, countdown=2 ** self.request.retries)
        except MaxRetriesExceededError:
            # Log the failure after max retries
            raise
