import datetime
from secrets import wifi_pswd
from time import sleep

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def save_to_history(problem_type, info=None):
    date = datetime.datetime.now().strftime('%d.%m')
    file = f'./wifi_history/wifi_history_{date}.txt'
    f = open(file, 'a+')
    if info:
        f.write(f'{problem_type} - ' + datetime.datetime.now().strftime('%d/%m - %H:%M') + ' - ' + str(info) + '\n')
    else:
        f.write(f'{problem_type} - ' + datetime.datetime.now().strftime('%d/%m - %H:%M') + '\n')
    f.close()


class WiFiBot:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.get('http://tplinkmodem.net')
        self.login()

    def wait_for_element(self, xpath):
        counter = 0
        while counter < 60:
            el = self.driver.find_elements_by_xpath(xpath)
            if el:
                break
            else:
                sleep(0.5)
                counter += 1

    def login(self):
        # main page login
        self.wait_for_element('//*[@id="pc-login-password"]')
        log = self.driver.find_element_by_xpath('//*[@id="pc-login-password"]')
        log.click()
        log.send_keys(wifi_pswd)
        log_btn = self.driver.find_element_by_xpath('//*[@id="pc-login-main"]/div[3]/div')
        log_btn.click()

        self.wait_for_element('//*[@id="confirm-yes"]')

        # confirm popup
        popup = self.driver.find_element_by_xpath('//*[@id="confirm-yes"]')
        popup.click()

    def check(self):
        self.wait_for_element('//*[@id="map_icon_internet"]')

        while True:
            globe_btn = self.driver.find_element_by_xpath('//*[@id="map_icon_internet"]')
            connected = self.driver.find_elements_by_class_name('map-icon-internet-status')
            disconnected = self.driver.find_elements_by_class_name('disconn')
            connection_error = self.driver.find_elements_by_class_name('dnserr')

            status_icon = any([connected, disconnected, connection_error])
            status_problem = any([disconnected, connection_error])

            if status_icon:
                if status_problem:
                    return False
                else:
                    globe_btn.click()
            else:
                pass

    def reset(self):

        def wait_for_status_change():
            while True:
                display = self.driver.find_element_by_id('mask').get_attribute('style')
                if display == 'display: block;':
                    pass
                else:
                    return False

        int_btn = self.driver.find_element_by_xpath('//*[@id="menuTree"]/li[2]/a')
        int_btn.click()
        self.wait_for_element('//*[@id="b_mobileDataSwitch"]/div/div[1]/ul[2]')
        switch_btn = self.driver.find_element_by_xpath('//*[@id="b_mobileDataSwitch"]/div/div[1]/ul[2]')
        switch_btn.click()  # turn off
        wait_for_status_change()
        switch_btn.click()  # turn on
        wait_for_status_change()

    def check_and_reset(self):
        save_to_history('START')
        while True:
            if self.check():
                pass
            else:
                self.reset()
                save_to_history('RESET')

                # back to 'check' page
                self.wait_for_element('//*[@id="menuTree"]/li[1]/a')
                back_btn = self.driver.find_element_by_xpath('//*[@id="menuTree"]/li[1]/a')
                back_btn.click()

    def take_care_of_wifi(self):
        while True:
            try:
                try:
                    self.check_and_reset()
                except NoSuchElementException:
                    log = self.driver.find_elements_by_xpath('//*[@id="pc-login-password"]')
                    if log:
                        save_to_history('LOGIN')
                        sleep(10)  # time for some actions
                        self.login()
                    else:
                        raise ValueError('Unknown NSE problem')

            except Exception as e:
                save_to_history('ERROR', e)

                # open new window and start again
                self.driver.get('http://tplinkmodem.net')
                log = self.driver.find_elements_by_xpath('//*[@id="pc-login-password"]')
                if log:
                    self.login()
                else:
                    pass


bot = WiFiBot()
bot.take_care_of_wifi()
