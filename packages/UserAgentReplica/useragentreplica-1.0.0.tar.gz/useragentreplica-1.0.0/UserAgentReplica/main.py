import random


class UserAgent:
    def __init__(self):
        self.browsers = ["Chrome", "Firefox", "Safari"]
        self.os_list = [
            "Windows NT 10.0; Win64; x64",
            "Linux; Android 10",
            "iPhone; CPU iPhone OS 14_6 like Mac OS X",
        ]
        self.browser_versions = {
            "Chrome": "Chrome/131.0.0.0",
            "Firefox": "Firefox/87.0",
            "Safari": "Safari/537.36",
        }

    def _generate_user_agent(self, browser):
        if browser not in self.browser_versions:
            raise ValueError(f"Browser '{browser}' is not supported.")
        os = random.choice(self.os_list)
        version = self.browser_versions[browser]
        return f"Mozilla/5.0 ({os}) AppleWebKit/537.36 (KHTML, like Gecko) {version} Safari/537.36"

    def chrome(self):
        return self._generate_user_agent("Chrome")

    def firefox(self):
        return self._generate_user_agent("Firefox")

    def safari(self):
        return self._generate_user_agent("Safari")

    def random_browser(self):
        browser = random.choice(self.browsers)
        return self._generate_user_agent(browser)
