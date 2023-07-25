from webdriver_auto_update import check_driver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
from selenium.webdriver.chrome.service import Service
import time
import allure
import pytest
from tkinter import StringVar
import main


class Tests(unittest.TestCase):

    def login(self):
        # Wait for "Sign in" to be visible
        print("Locating Sign in.")
        self.find_and_click("class", "authorization-link")
        self.find_and_input("css", 'input[name="login[username]"]', self.email)
        self.find_and_input("css", 'input[name="login[password]"]', self.password)
        self.find_and_click("id", "send2")
        time.sleep(5)

    def setUp(self):
        # Access the selected environment from main.py
        selected_env = main.selected_env
        self.first = main.first
        self.last = main.last
        self.email = main.email
        self.password = main.password

        self.service = Service(executable_path="E:\\chromewebdriver\\chromedriver.exe")
        self.driver = webdriver.Chrome(service=self.service)
        self.dev = "https://magento.softwaretestingboard.com/"
        self.stage = "https://magento.softwaretestingboard.com/"
        self.prod = "https://magento.softwaretestingboard.com/"
        self.wait = WebDriverWait(self.driver, 5)

        # Update the persistent variable based on the selected checkbox
        if selected_env == "dev":
            print("Starting Dev environment: " + self.dev)
            self.driver.get(self.dev)
            env_url = self.dev
        elif selected_env == "stage":
            print("Starting Stage environment: " + self.stage)
            self.driver.get(self.stage)
            env_url = self.stage
        elif selected_env == "prod":
            print("Starting Prod environment: " + self.prod)
            self.driver.get(self.prod)
            env_url = self.prod
        else:
            print("No environment selected.")
        self.env_url = env_url

    # find and input/click use locators to define the approach and send the input or click
    def find_and_input(self, locator_type, locator_value, value):
        print(f"Locating element with {locator_type}: {locator_value}")
        locator = (self.get_locator_type(locator_type), locator_value)
        time.sleep(1)
        input_box = self.wait.until(EC.visibility_of_element_located(locator))
        print(f"Element found with {locator_type}: {locator_value}")
        time.sleep(1)
        input_box.send_keys(value)
        time.sleep(2)
        print(f"Inputted value: {value}")

    def find_and_click(self, locator_type, locator_value):
        print(f"Locating element with {locator_type}: {locator_value}")
        locator = (self.get_locator_type(locator_type), locator_value)
        time.sleep(1)
        element = self.wait.until(EC.element_to_be_clickable(locator))
        print(f"Element found with {locator_type}: {locator_value}")
        time.sleep(1)
        element.click()
        time.sleep(2)
        print("Element clicked")

    def get_locator_type(self, locator_type):
        if locator_type == "id":
            return By.ID
        elif locator_type == "class":
            return By.CLASS_NAME
        elif locator_type == "xpath":
            return By.XPATH
        elif locator_type == "css":
            return By.CSS_SELECTOR
        else:
            raise ValueError("Invalid locator type. Supported types are 'id', 'class', 'css', and 'xpath'.")

    def tearDown(self):
        self.driver.quit()
        self.service.stop()

    def test_create_account(self):
        print("Test started for account creation.")
        print("Locating 'Create an Account' button..")
        # Use find and click method to set locator and click the locator
        self.find_and_click("xpath", "//li/a[text()='Create an Account']")
        time.sleep(5)
        current_url = self.driver.current_url
        expected_url = "https://magento.softwaretestingboard.com/customer/account/create/"

        try:
            assert current_url == current_url, f"Failed: URL does not match the expected URL {expected_url}. Actual: {current_url}"
        except AssertionError as e:
            print(e)
        # Print assertion
        print("Assertion passed for URL comparison.")
        print("Current URL: " + current_url + " Expected URL: " + expected_url)

        # first name input
        print("Locating first name input box.")
        self.find_and_input("id", "firstname", self.first)

        # last name input
        print("Locating last name input box.")
        self.find_and_input("id", "lastname", self.last)

        # email input
        print("Locating email name input box.")
        self.find_and_input("id", "email_address", self.email)

        # password input
        print("Locating password input box.")
        self.find_and_input("id", "password", self.password)
        print("Locating confirm password input box.")
        self.find_and_input("id", "password-confirmation", self.password)

        # Click Create an Account
        print("Locating Create an Account button.")
        self.find_and_click("xpath", "//button[@title='Create an Account']")
        time.sleep(10)

        alert_message = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//div[contains(text(), 'Thank you for registering with Main Website Store.')]")))

        # Assert that the alert message text is correct
        expected_message = "Thank you for registering with Main Website Store."
        assert alert_message.text == expected_message, f"Expected message: '{expected_message}' but got: '{alert_message.text}'"

    def test_login(self):
        self.login()
        time.sleep(3)
        # Find the <span> element using a CSS selector
        span_element = self.driver.find_element(By.CSS_SELECTOR, "span.logged-in")

        # Get the text inside the <span> element
        welcome_message = span_element.text

        try:
            assert welcome_message == f"Welcome, {self.first} {self.last}!"
        except AssertionError as e:
            print(e)
        # Print assertion
        print("Assertion passed for user login.")


