from scrape import BDOaccesslink
from util import *
import time

access = BDOaccesslink(URL, BASE_URL)
access.access_wiki()
access.show_characters()
access.access_driver()
access.character_selection()
time.sleep(20)