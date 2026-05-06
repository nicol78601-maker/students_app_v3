import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from selenium.webdriver.support.ui import Select

BASE_URL = "http://127.0.0.1:5000"


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    time.sleep(5)
    driver.quit()


def test_students_table_exists(driver):
    driver.get(BASE_URL)
    table = driver.find_element(By.TAG_NAME, "table")
    assert table is not None


def test_add_students(driver):
    driver.get(BASE_URL)

    # 1. מילוי פרטים (חובה לעשות זאת לפני הלחיצה!)
    driver.find_element(By.ID, "idBox").send_keys("101")
    driver.find_element(By.ID, "nameBox").send_keys("Yossi Cohen")  # וודא שה-ID תואם ל-HTML שלך
    driver.find_element(By.ID, "ageBox").send_keys("25")

    # 2. לחיצה על כפתור ההוספה
    # במקום "By.TAG_NAME", עדיף להשתמש ב-ID ספציפי כדי לא ללחוץ על כפתור אחר בטעות
    driver.find_element(By.ID, "btAdd").click()

    # 3. עכשיו אפשר להמשיך לבדיקת ה-Theme ללא הפרעה של Alert
    theme_dropdown = driver.find_element(By.ID, "themeSelect")
    # ... המשך הקוד שלך

def test_select_student(driver):
    driver.get(BASE_URL)
    # 1. איתור האלמנט של התפריט הנגלל (Select)
    theme_dropdown = driver.find_element(By.ID, "themeSelect")
    select = Select(theme_dropdown)

    # 2. בחירה באופציית "Forest" לפי ה-Value שלה ב-HTML
    select.select_by_value("theme-forest")

    # בדיקת ה-Class
    body = driver.find_element(By.TAG_NAME, "body")
    assert "theme-forest" in body.get_attribute("class")

    # בדיקה מחמירה יותר - האם צבע הרקע באמת השתנה?
    background_color = body.value_of_css_property("background-color")
    print(f"The new background color is: {background_color}")

# הגדרת ה-driver בצורה פשוטה - סלניום יטפל בהורדה לבד
@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # כאן סלניום 4.6+ מוצא ומוריד את הדרייבר אוטומטית
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()

def test_theme_and_screenshots(driver):
    driver.get("http://127.0.0.1:5000")

    # צילום מסך ראשוני - מצב ברירת מחדל
    driver.save_screenshot("step1_default_theme.png")

    # שינוי ה-Theme ל-Forest
    theme_select = Select(driver.find_element(By.ID, "themeSelect"))
    theme_select.select_by_value("theme-forest")

    # המתנה קצרה לרינדור
    time.sleep(1)

    # וידוא שה-Class עודכן
    body_class = driver.find_element(By.TAG_NAME, "body").get_attribute("class")
    assert "theme-forest" in body_class

    # צילום מסך של העיצוב החדש
    driver.save_screenshot("step2_forest_theme.png")

    print("Test passed: Theme changed and screenshots saved!")


