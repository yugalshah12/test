# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re

class AppDynamicsJob(unittest.TestCase):
    def setUp(self):
        # AppDynamics will automatically override this web driver
        # as documented in https://docs.appdynamics.com/display/PRO44/Write+Your+First+Script
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.katalon.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_app_dynamics_job(self):
        driver = self.driver
        driver.get("https://frontend.qa.entera.ai/signin")
        driver.find_element_by_css_selector("input[name=\"username\"]").clear()
        driver.find_element_by_css_selector("input[name=\"username\"]").send_keys("tu1@greenletinv.com")
        driver.find_element_by_css_selector("input[name=\"password\"]").clear()
        driver.find_element_by_css_selector("input[name=\"password\"]").send_keys("Test1234")
        driver.find_element_by_css_selector("button[type=\"submit\"]").click()
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, ".col-sm-12 h1"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        try: self.assertEqual("Entry Homes Dashboard", driver.find_element_by_css_selector(".col-sm-12 h1").text)
        except AssertionError as e: self.verificationErrors.append(str(e))
        for i in range(60):
            try:
                if self.is_element_present(By.CSS_SELECTOR, "a[class=\"nav-link\"][href=\"/dashboard\"]"): break
            except: pass
            time.sleep(1)
        else: self.fail("time out")
        driver.find_element_by_css_selector("a[class=\"nav-link\"][href=\"/dashboard\"]").click()
        driver.close()
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        # To know more about the difference between verify and assert,
        # visit https://www.seleniumhq.org/docs/06_test_design_considerations.jsp#validating-results
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
