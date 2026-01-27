# tests.py
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from django.contrib.auth.models import User
from selenium.webdriver.chrome.options import Options


class SimpleSeleniumTest(LiveServerTestCase):
    def setUp(self):
        options = Options()
        options.add_argument("--headless")  # تشغيل Chrome في وضع headless
        # ChromeDriver المناسب لنسخة Chrome الحالية
        self.driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options)
        # إنشاء مستخدم تجريبي لاختبارات login
        User.objects.create_user(username='admin', password='admin')

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        self.driver.get(self.live_server_url)
        # انتظار العنوان يتضمن كلمة Django
        WebDriverWait(self.driver, 10).until(
            EC.title_contains("Hello, world!")
        )
        self.assertIn("Hello, world!", self.driver.title)

    def test_login_page(self):
        # تأكد من URL صفحة login
        self.driver.get(f"{self.live_server_url}/accounts/login/")
        try:
            # انتظار حقول username و password والزر يظهروا
            username_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "username"))
            )
            password_input = self.driver.find_element(By.NAME, "password")
            login_button = self.driver.find_element(By.ID, "submit")

            # إدخال بيانات المستخدم التجريبي
            username_input.send_keys("admin")
            password_input.send_keys("admin")
            login_button.click()

            # انتظار إعادة توجيه بعد تسجيل الدخول
            WebDriverWait(self.driver, 5).until(
                EC.url_contains("/")  # عدّل URL حسب مشروعك
            )
            self.assertIn("Hello, world!", self.driver.title)
            self.assertIn("admin", self.driver.page_source)

        except Exception as e:
            self.fail(f"Login page test failed: {e}")
