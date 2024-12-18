from website_scrapers.DISIMwebsiteScraper import DISIMwebsiteScraper
from website_scrapers.ADSUwebsiteScraper import ADSUwebsiteScraper

from SendFilteredAnnouncements import SendFilteredAnnouncements

from model.Announcement import Announcement as AnnouncementModel

import configuration_file as conf

import time

SECONDS_IN_ONE_HOUR = 3600


if __name__ == '__main__':
    disim = DISIMwebsiteScraper()
    adsu = ADSUwebsiteScraper()

    while True:
        # START scrape announcements from "disim" and "adsu" websites
        announcements_to_be_published = disim.get_announcements()
        announcements_to_be_published.extend(adsu.get_announcements())

        # WebsiteScraper.debug_by_printing_prettified_json(announcements_to_be_published)
        # END scrape announcements from "disim" and "adsu" websites

        # START insert announcements into SQLite DB
        announcement_model = AnnouncementModel()
        announcement_model.bulk_insert(announcements_to_be_published)
        # END insert announcements into SQLite DB

        SendFilteredAnnouncements.send_announcements_filtered_by_tags_of_interest_to_user(announcements_to_be_published)

        del announcements_to_be_published  # free up RAM

        time.sleep(conf.HOURS_BETWEEN_SCRAPING * SECONDS_IN_ONE_HOUR)