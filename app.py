from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the initial page
driver.get("https://www.onthesnow.com/canada/ski-resorts")

# Wait for the button to be present
wait = WebDriverWait(driver, 10)
button = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='__next']/div[6]/div[2]/div/div[1]/div/button")))

# Click the button
button.click()

# Wait for the parent div to be present
parent_div = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#__next > div.container-xl.content-container > div.styles__layout__2aTIJ.layout-container > div > div.md-hide.m-0 > div > article > div.styles__box__1sXJN.styles__resortsList__3pFyu")))

# Loop through the two child divs
for i in range(1, 3):
    # Find the child div
    child_div = parent_div.find_element(By.CSS_SELECTOR, f"div:nth-child({i})")

    # Find the link inside the child div
    link_element = child_div.find_element(By.CSS_SELECTOR, "div:nth-child(1) > a")

    # Print the text of the link
    print(link_element.text)

# Close the browser
driver.quit()