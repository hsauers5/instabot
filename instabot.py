from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options
import datetime, time
from selenium.webdriver.common.keys import Keys
import sys
import random
from xvfbwrapper import Xvfb

class InstagramBot():
	def __init__(self, email, password):
		profile = webdriver.FirefoxProfile()
		user_agent = "Mozilla/5.0 (iPhone; U; CPU like Mac OS X; en) AppleWebKit/420+ (KHTML, like Gecko) Version/3.0 Mobile/1A543a Safari/419.3"
		profile.set_preference("general.useragent.override", user_agent)
		options = Options()
		options.headless = False
		self.browser = webdriver.Firefox(profile, options=options, executable_path="geckodriver")
		self.browser.set_window_size(920, 1280)
		self.email = email
		self.password = password


	def sign_in(self):
		self.browser.get('https://www.instagram.com/accounts/login/')
		
		time.sleep(3)
		if self.browser.current_url != "https://www.instagram.com/accounts/login/":
			return
		
		print("Signing in...")
		
		while True:
			try:
				tmp = self.browser.find_elements_by_css_selector('form input')[0]
				break
			except:
				time.sleep(1)

		email_input = self.browser.find_elements_by_css_selector('form input')[0]
		password_input = self.browser.find_elements_by_css_selector('form input')[1]

		email_input.send_keys(self.email)
		password_input.send_keys(self.password)
		password_input.send_keys(Keys.ENTER)
		time.sleep(5)

		# need security code!
		if len(self.browser.find_elements_by_css_selector("button[class='_5f5mN       jIbKX KUBKM      yZn4P   ']")) != 0:
			time.sleep(2)
			self.security_code_required()


	# likes N posts in hashtag
	def like_posts_in_hashtag(self, hashtag="food", num_to_like=12):
		self.browser.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
		posts = []
		time.sleep(1)
		posts = self.browser.find_elements_by_css_selector("div[class='v1Nh3 kIKUG  _bz0w']")[9:num_to_like+9]
		for post in posts:
			try:
				post.click()
			except:
				continue
			time.sleep(1)
			pic = None
			try:
				pic = self.browser.find_element_by_css_selector("button[class='dCJp8 afkep _0mzm-']")
			except:
				continue

			if 'Unlike' in str(pic.get_attribute('innerHTML')):
				print("Already liked!")
			else:
				pic.click()
				print("Liked media.")
			time.sleep(10)
			self.browser.back()


	def like_posts_in_hashtags(self, hashtag_list=["food", "ilovetheburg"], num_to_like=12):
		for tag in hashtag_list:
			self.like_posts_in_hashtag(hashtag=tag, num_to_like=num_to_like)
			print("Liked posts in hashtag: " + tag)

	def wait(self, site="https://www.instagram.com/"):
		self.browser.get(site)

	def security_code_required(self):
		print("Security code required!")
		security_button = self.browser.find_elements_by_css_selector("button[class='_5f5mN       jIbKX KUBKM      yZn4P   ']")[0]
		security_button.click()
		time.sleep(1)
		code_field = self.browser.find_element_by_id("security_code")
		code_field.click()
		your_code = input("Please enter the code sent to your email: ").strip()
		code_field.send_keys(your_code)
		time.sleep(1)
		code_field.send_keys(Keys.ENTER)
		# self.browser.find_elements_by_css_selector("button[class='_5f5mN       jIbKX KUBKM      yZn4P   ']")[0].click()
		time.sleep(10)
		while True:
			print(self.browser.current_url)
			if self.browser.current_url != "https://www.instagram.com":
				break
			else:
				time.sleep(5)


def run_forever():
	bot = InstagramBot(username, password)
	
	while True:
		bot.sign_in()  # now detects if logged in or not
		try:
			bot.like_posts_in_hashtags(hashtag_list=hashtag_list, num_to_like=num_to_like)
		except:
			try:
				bot.like_posts_in_hashtags(hashtag_list=hashtag_list, num_to_like=num_to_like)
			except:
				# bot.sign_in()
				bot.like_posts_in_hashtags(hashtag_list=hashtag_list, num_to_like=num_to_like)
				continue

		count = 0
		minutes_to_wait = 60*5*random.random()
		bot.wait()
		print("Waiting " + str(minutes_to_wait) + " minutes.")

		while count < minutes_to_wait:
			time.sleep(60)
			count += 1
			print(str(count*100/minutes_to_wait) + "%")

username = sys.argv[1]
password = sys.argv[2]
num_to_like = 12
hashtag_list = []

if len(sys.argv) >= 3:
	num_to_like = int(sys.argv[3])

for i in range(4, len(sys.argv)):
	hashtag_list.append(sys.argv[i])

# bot = InstagramBot(username, password)
# bot.sign_in()

with Xvfb() as xvfb:
	run_forever()
# run_forever()
