from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.common.keys import Keys
import sys
import random


class InstagramBot():
	def __init__(self, email, password):
		profile = webdriver.FirefoxProfile()
		user_agent = "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3"
		profile.set_preference("general.useragent.override", user_agent)
		options = Options()
		options.headless = True
		self.browser = webdriver.Firefox(profile, options=options, executable_path=r"geckodriver")
		self.email = email
		self.password = password


	# fix camelcase style
	def signIn(self):
		self.browser.get('https://www.instagram.com/accounts/login/')

		while True:
			try:
				tmp = self.browser.find_elements_by_css_selector('form input')[0]
				break
			except:
				time.sleep(1)

		emailInput = self.browser.find_elements_by_css_selector('form input')[0]
		passwordInput = self.browser.find_elements_by_css_selector('form input')[1]

		emailInput.send_keys(self.email)
		passwordInput.send_keys(self.password)
		passwordInput.send_keys(Keys.ENTER)
		time.sleep(2)


	# likes N posts in hashtag
	def like_posts_in_hashtag(self, hashtag="food", num_to_like=12):
		self.browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
		posts = []
		time.sleep(1)
		posts = self.browser.find_elements_by_css_selector("div[class='v1Nh3 kIKUG  _bz0w']")[9:num_to_like+9]
		for post in posts:
			post.click()
			time.sleep(1)
			pic = self.browser.find_element_by_css_selector("button[class='dCJp8 afkep _0mzm-']")
			pic.click()
			time.sleep(1)
			self.browser.back()


	def like_posts_in_hashtags(self, hashtag_list=[], num_to_like=12):
		for tag in hashtag_list:
			self.like_posts_in_hashtag(hashtag=tag, num_to_like=num_to_like)
			print("Liked posts in hashtag: " + tag)


username = sys.argv[1]
password = sys.argv[2]
num_to_like = 12
hashtag_list = ["food", "ilovetheburg"]

if len(sys.argv) >= 3:
	num_to_like = int(sys.argv[3])

for i in range(4, len(sys.argv)):
	hashtag_list.append(sys.argv[i])

bot = InstagramBot(username, password)
bot.signIn()

while True:
	bot.like_posts_in_hashtags(hashtag_list=hashtag_list, num_to_like=num_to_like)
	sleep_length = random.random() * 43200
	time.sleep(sleep_length)