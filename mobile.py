import sys
import subprocess

from appium import webdriver
import time


class Instabot:

    def __init__(self, username, password):
        desired_caps = {'platformName': 'Android',
                        "appPackage": "com.instagram.android",
                        "deviceName": "android",
                        "appActivity": "activity.MainTabActivity",
                        "noReset": "true",
                        "fullReset": "false"
                        }

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

        self.username = username
        self.password = password
        self.sign_in()

    def sign_in(self):
        time.sleep(1)
        try:
            self.driver.find_element_by_id("log_in_button").click()
            self.driver.find_element_by_id("login_username").click()
            self.driver.find_element_by_id("login_username").send_keys(self.username)
            self.driver.press_keycode(4)  # back key - avoid FB prompt
            self.driver.find_element_by_id("password_input_layout").send_keys(self.password)
            self.driver.find_element_by_id("next_button").click()

        except:
            print("Already logged in!")
            pass

        time.sleep(3)

        try:
            # don't save to  google
            if self.driver.find_element_by_id("autofill_save_no"):
                self.driver.find_element_by_id("autofill_save_no").click()
        except:
            pass

        time.sleep(1)

    def like_posts_in_hastag_list(self, hashtag_list, num_to_like):
        # wait for login
        while len(self.driver.find_elements_by_id("gap_binder_group")) == 0:
            time.sleep(1)

        for tag in hashtag_list:
            # HERE - for each tag
            self.like_posts_in_hashtag(hashtag=tag, num_to_like=num_to_like)

    def like_posts_in_hashtag(self, hashtag, num_to_like):
        # go to explore page
        self.driver.tap([[317, 1723]])
        self.driver.find_element_by_id("action_bar_search_edit_text").click()

        time.sleep(2)

        # deny location permissions
        try:
            try:
                self.driver.find_element_by_id("com.android.permissioncontroller:id/permission_deny_button").click()
            except:
                self.driver.find_element_by_id("com.android.permissioncontroller:id/permission_deny_and_dont_ask_again_button").click()
        except:
            print("Couldn't find it!")

        self.driver.find_element_by_id("action_bar_search_edit_text").send_keys(hashtag)
        self.driver.find_elements_by_id("tab_button_name_text")[2].click()
        time.sleep(1)
        self.driver.find_elements_by_id("row_hashtag_container")[0].click()
        time.sleep(2)
        self.driver.find_elements_by_accessibility_id("Recent")[0].click()
        time.sleep(1)
        self.driver.find_elements_by_class_name("android.widget.ImageView")[0].click()

        count = 0
        while count < num_to_like:
            # like image
            try:
                this_like_button = self.driver.find_elements_by_accessibility_id("Like")[0]
                this_like_button.click()
            except:
                self.driver.swipe(542, 1514, 674, 1214, 3000)
                this_like_button = self.driver.find_elements_by_accessibility_id("Like")[0]
                this_like_button.click()

            # scroll to next
            while len(self.driver.find_elements_by_accessibility_id("Like")) == 0:
                self.driver.swipe(542, 1514, 674, 560, 3000)

            count += 1

        print("Liked " + str(num_to_like) + " posts in #" + hashtag + "!\n")


# set up emulator
# subprocess.Popen(["sudo ~/Android/Sdk//emulator/emulator -avd Pixel_2_API_29"], shell=True)
# time.sleep(5)
# install app if needed
# subprocess.Popen(["adb install apps/instagram.apk"], shell=True)

username = sys.argv[1]
password = sys.argv[2]
num_to_like = 12
hashtag_list = []

if len(sys.argv) >= 3:
    num_to_like = int(sys.argv[3])

for i in range(4, len(sys.argv)):
    hashtag_list.append(sys.argv[i])

bot = Instabot(username, password)
while True:
  bot.like_posts_in_hastag_list(hashtag_list, num_to_like)
  
  count = 0
  minutes_to_wait = 60*5*random.random()
  print("Waiting " + str(minutes_to_wait) + " minutes.")

  while count < minutes_to_wait:
    time.sleep(60)
    count += 1
    print(str(count*100/minutes_to_wait) + "%")
