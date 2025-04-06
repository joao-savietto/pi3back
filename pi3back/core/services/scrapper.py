import random

from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# List of user agents to rotate through for request randomization
user_agents = [
    (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    ),
    (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
        "(KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    ),
    # Add more user agents here as needed
]


class TalentScrapper:
    """Scrapes LinkedIn profile data using Selenium WebDriver.

    Handles login and extracts profile information including about section,
    experiences, education, interests, accomplishments and contacts.
    Implements anti-detection measures to avoid bot detection.
    """

    def __init__(
        self, linkedin_url_profile: str, username: str, password: str
    ):
        """Initialize the scraper with target profile and credentials.

        Args:
            linkedin_url_profile: URL of LinkedIn profile to scrape
            username: LinkedIn account username for login
            password: LinkedIn account password for login
        """
        self.linkedin_url_profile = linkedin_url_profile
        self.username = username
        self.password = password

        # Configure Chrome options for headless browsing and anti-detection
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")  # Run without GUI
        self.chrome_options.add_argument(
            f"user-agent={random.choice(user_agents)}"
        )  # Randomize user agent
        self.chrome_options.add_argument(
            "--disable-blink-features=AutomationControlled"
        )  # Disable automation flags
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"]
        )  # Hide automation switches
        self.chrome_options.add_experimental_option(
            "useAutomationExtension", False
        )  # Disable automation extension

        # Initialize WebDriver with configured options
        self.driver = webdriver.Chrome(options=self.chrome_options)

        # Execute JavaScript to hide WebDriver flag
        self.driver.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument",
            {
                "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
            """
            },
        )

        # Initialize data storage attributes
        self.about = ""
        self.name = ""
        self.experiences = []
        self.educations = []
        self.interests = []
        self.accomplishments = []
        self.contacts = []

    def run(self):
        """Execute the scraping process.

        Logs into LinkedIn, scrapes profile data, and stores results.
        Closes the WebDriver when complete.
        """
        # Login to LinkedIn
        actions.login(self.driver, self.username, self.password)

        # Scrape profile data using linkedin-scraper
        person = Person(self.linkedin_url_profile, driver=self.driver)

        # Store scraped data as dictionaries
        self.about = person.about
        self.experiences = [x.__dict__ for x in person.experiences]
        self.educations = [x.__dict__ for x in person.educations]
        self.interests = [x.__dict__ for x in person.interests]
        self.accomplishments = [x.__dict__ for x in person.accomplishments]
        self.contacts = [x.__dict__ for x in person.contacts]

        # Store additional profile information
        self.person = person
        self.name = person.name

        # Clean up - close browser
        self.driver.quit()
