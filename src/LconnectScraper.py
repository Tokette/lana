#!/bin/python2
#
#   Lconnect Scraper
#
#   An implementation of ClassDataScraper. Scrapes ClassData from Lconnect
#
#

from ClassDataScraper import ClassDataScraper
from mechanize import Browser, URLError, _http
from cookielib import LWPCookieJar


class LconnectScraper(ClassDataScraper):
    LCONNECT_URL = 'http://leopardweb.wit.edu/'
    USERAGENT = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.1) ' \
                + 'Gecko/20100122 firefox/3.6.1'

    def __init__(self):
        # Create a cookie jar and a browser
        self._cookieJar = LWPCookieJar()
        self._browser = Browser()
        self._browser.set_cookiejar(self._cookieJar)

        # Set Browser options
        self._browser.set_handle_equiv(True)
        self._browser.set_handle_gzip(True)
        self._browser.set_handle_redirect(True)
        self._browser.set_handle_referer(True)
        self._browser.set_handle_robots(False)
        self._browser.set_handle_refresh(_http.HTTPRefreshProcessor(),
                                         max_time=1)
        self._browser.addheaders = [('User-agent', LconnectScraper.USERAGENT)]

        # Debugging
        self._browser.set_debug_http(True)
        self._browser.set_debug_redirects(True)
        self._browser.set_debug_responses(True)

    def getName(self):
        return "Lconnect Scraper"

    def connect(self):
        """
        Attempts to connect to the data source
        """
        try:
            # Try to open a connection. 8 Second timeout
            self._browser.open(LconnectScraper.LCONNECT_URL, timeout=8)
            return True
        except URLError:
            return False

    def disconnect(self):
        """
        Disconnects from the data source
        """

        self._browser.close()

    def requiresAuthentication(self):
        """
        Returns whether or not the scraper requires authentication information
        """

        return True

    def authenticate(self, username, password):
        """
        Attempts to authenticate the scraper using username and password
        """

        # If we're on the sign in page, try to sign in
        if self._browser.title() == 'Sign In':
            for form in self._browser.forms():
                if form.name is None:
                    self._browser.form = list(self._browser.forms())[0]
                    self._browser['username'] = username
                    self._browser['password'] = password

                    self._browser.submit()

        # If the browser's title is 'Main Menu',
        # we've either successfully logged in, or we were already
        if self._browser.title() == 'Main Menu':
            return True
        else:
            return False

    def getClassData(self):
        """
        Returns a list of ClassData objects
        """

        return []
