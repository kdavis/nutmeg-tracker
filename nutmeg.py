import requests
import re


class Nutmeg():
    LOGIN_FORM = "https://app.nutmeg.com/auth/users/sign_in"
    LOGIN_REDIRECT = "https://app.nutmeg.com/client"
    NUTMEG_PORTFOLIO = "https://app.nutmeg.com/client/portfolio"
    LOGIN_SUCCESS = False

    def __init__(self, email, password):
        self.EMAIL = email
        self.PASSWORD = password
        self.session = requests.session()

        self.session.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'

    def get_authenticity_token(self):
        auth_request = self.session.get(self.LOGIN_FORM)
        matches = re.search(
            'name="authenticity_token" value="([A-z0-9+\/=]+)"', auth_request.content.decode('utf-8'), re.M)
        if matches is None:
            return None
        return matches.group(1)

    def login(self):
        login_attempt = self.session.post(self.LOGIN_FORM, data={
            "user[email]": self.EMAIL,
            "user[password]": self.PASSWORD,
            "utf8": "✓",
            "authenticity_token": self.get_authenticity_token(),
            "commit": "Sign in"
        }, allow_redirects=False)

        if "location" in login_attempt.headers and login_attempt.headers['location'] == self.LOGIN_REDIRECT:
            self.LOGIN_SUCCESS = True

        return self.LOGIN_SUCCESS

    def get_values(self):
        portfolio_data = self.session.get(self.NUTMEG_PORTFOLIO)

        matches = re.findall(
            'data-uuid="([0-9a-f\-]+)" data-fund-type="([A-Za-z]+)".*?&pound;([0-9]+)', portfolio_data.text, re.M | re.DOTALL)

        return matches

    def is_logged_in(self):
        return self.LOGIN_SUCCESS
