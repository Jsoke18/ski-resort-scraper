from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Create a new instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the Whistler Blackcomb page
driver.get("https://www.onthesnow.com/british-columbia/whistler-blackcomb/ski-resort")

def extract_box_info(title_xpath, metric_xpath=None):
    # Wait for the title element to be present
    title_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, title_xpath))
    )
    title_text = title_element.text
    print("Title:", title_text)

    # Check if the metric_xpath is provided
    if metric_xpath:
        # Wait for the metric element to be present
        metric_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, metric_xpath))
        )
        metric_text = metric_element.text
        print("Metric Value:", metric_text)
    else:
        print("No metric value available.")

# Extract information for beginner runs
beginner_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[1]/div[2]"
beginner_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[1]/div[3]"
extract_box_info(beginner_title_xpath, beginner_metric_xpath)

# Extract information for intermediate runs
intermediate_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[3]/div[2]"
intermediate_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[2]/div[3]"
extract_box_info(intermediate_title_xpath, intermediate_metric_xpath)

# Extract information for advanced runs
advanced_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[3]/div[2]"
advanced_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[3]/div[3]"
extract_box_info(advanced_title_xpath, advanced_metric_xpath)

# Extract information for expert runs
expert_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[4]/div[2]"
expert_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[4]/div[3]"
extract_box_info(expert_title_xpath, expert_metric_xpath)

# Extract information for runs total
runs_in_total_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[5]/div[2]"
runs_in_total_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[5]/div[3]"
extract_box_info(runs_in_total_xpath, runs_in_total_value_xpath)


# Extract information for longest run total
runs_in_total_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[5]/div[2]"
runs_in_total_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[5]/div[3]"
extract_box_info(runs_in_total_xpath, runs_in_total_value_xpath)

# Extract information for skiable terrain total
skiable_terrain_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[7]/div[2]"
skiable_terrain_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[7]/div[3]"
extract_box_info(skiable_terrain_title_xpath, skiable_terrain_value_xpath)

# Extract information for snow making total
snow_making_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[8]/div[2]"
snow_making_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[7]/div[3]"
extract_box_info(snow_making_title_xpath, snow_making_value_xpath)


# Extract information for snow making total
base_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[2]/div[2]"
base_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[2]/div[3]"
extract_box_info(base_elevation_title_xpath, base_elevation_value_xpath)

# Extract information for snow making total
summit_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[3]/div[2]"
summit_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[3]/div[3]"
extract_box_info(summit_elevation_title_xpath, summit_elevation_value_xpath)

# Extract information for snow making total
vertical_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[4]/div[2]"
vertical_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[4]/div[3]"
extract_box_info(vertical_elevation_title_xpath, vertical_elevation_value_xpath)


# Extract information for snow making total
vertical_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[4]/div[2]"
vertical_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[4]/div[3]"
extract_box_info(vertical_elevation_title_xpath, vertical_elevation_value_xpath)

# Extract information for snow making total
important_dates_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[1]/h3"
extract_box_info(important_dates_xpath)

driver.quit()