from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import concurrent.futures
import re
from selenium.common.exceptions import TimeoutException, NoSuchElementException
app = Flask(__name__)
import requests

def clean_data(data):
    if data is None:
        return ''  # Return an empty string or a default value
    cleaned_data = re.sub(r'\\"|"', '', data)
    return cleaned_data


@app.route('/ski-resort-data', methods=['POST'])
def get_ski_resort_data():
    # Get the URL from the request data
    url = request.json['url']

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Navigate to the specified URL
    driver.get(url)

    def extract_box_info(title_selector, metric_selector=None, by=By.XPATH):
        title_text = None
        metric_text = None

        try:
            # Wait for the title element to be present (up to 5 seconds)
            title_element = WebDriverWait(driver, 0.3).until(
                EC.presence_of_element_located((by, title_selector))
            )
            title_text = title_element.text
        except TimeoutException:
            print(f"Title element not found: {title_selector}")

        if metric_selector:
            try:
                # Wait for the metric element to be present (up to 5 seconds)
                metric_element = WebDriverWait(driver, 0.3).until(
                    EC.presence_of_element_located((by, metric_selector))
                )
                metric_text = metric_element.text
            except TimeoutException:
                print(f"Metric element not found: {metric_selector}")

        return title_text, metric_text

    # Extract information for beginner runs
    beginner_title_css = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div.styles_box__1BTY2.slopesColors_fillGreen__25hpD > div.styles_title__23khW"
    beginner_metric_css = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div.styles_box__1BTY2.slopesColors_fillGreen__25hpD > div.styles_metric__14Z7T"
    beginner_title, beginner_metric = extract_box_info(beginner_title_css, beginner_metric_css, by=By.CSS_SELECTOR)
    # Print the extracted values for beginner runs
    print("Beginner Runs:")
    print("Title:", beginner_title)
    print("Metric:", beginner_metric)

    # Extract information for intermediate runs
    intermediate_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div.styles_box__1BTY2.slopesColors_fillPrimary__3XIND > div.styles_title__23khW"
    intermediate_metric_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div.styles_box__1BTY2.slopesColors_fillPrimary__3XIND > div.styles_metric__14Z7T"
    intermediate_title, intermediate_metric = extract_box_info(intermediate_title_xpath, intermediate_metric_xpath, by=By.CSS_SELECTOR)
    print("Title:", intermediate_title)
    print("Metric:", intermediate_metric)

    # Extract information for advanced runs
    advanced_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div.styles_title__23khW"
    advanced_metric_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(3) > div.styles_metric__14Z7T"
    advanced_title, advanced_metric = extract_box_info(advanced_title_xpath, advanced_metric_xpath, by=By.CSS_SELECTOR)
    print("Title:", advanced_title)
    print("Metric:", advanced_metric)
    # Extract information for resort info
    resort_info_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_descriptionTabs__3eDit > div.styles_description__16DzX > div.styles_readMoreDescription__2OTyA.styles_wrap__u6bah.styles_active__1wotC.styles_collapsed__3HOrO"
    resort_info, _ = extract_box_info(resort_info_xpath, by=By.CSS_SELECTOR)
    print("Title:", resort_info)
    # Extract information for expert runs
    expert_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(4) > div.styles_title__23khW"
    expert_metric_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(4) > div.styles_metric__14Z7T"
    expert_title, expert_metric = extract_box_info(
        expert_title_xpath, expert_metric_xpath, by=By.CSS_SELECTOR)
    print("Title:", expert_title)
    print("Metric:", expert_metric)
    # Extract information for resort info
    total_lifts_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(7) > article > div.styles_box__m1CLQ > h3"
    total_lifts_value, _ = extract_box_info(total_lifts_xpath, by=By.CSS_SELECTOR)
    total_lifts_cleaned = re.sub(r'[^0-9]', '', total_lifts_value)
    print('total lifts')
    print("Metric:", total_lifts_value)
    # Extract information for runs total
    runs_in_total_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(5) > div.styles_title__23khW"
    runs_in_total_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(5) > div.styles_metric__14Z7T"
    runs_in_total_title, runs_in_total_metric = extract_box_info(
        runs_in_total_xpath, runs_in_total_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", runs_in_total_title)
    print("Metric:", runs_in_total_metric)
    # Extract information for resort info
    phone_number_css = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_wrapBox__2j8bk > article > div.styles_box__1sXJN.styles_box__16JJ5 > div.styles_innerLeft__DOWs_ > div > div.styles_phone__3mzWV > p > a"
    phone_number, _ = extract_box_info(phone_number_css, by=By.CSS_SELECTOR)
    print("phone:", phone_number)
    # Extract information for longest run total
    longest_run_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(6) > div.styles_title__23khW"
    longest_run_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(6) > div.styles_metric__14Z7T"
    longest_run_title, longest_run_metric = extract_box_info(
        longest_run_title_xpath, longest_run_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", longest_run_title)
    print("Metric:", longest_run_metric)
    # Extract information for skiable terrain total
    skiable_terrain_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(7) > div.styles_title__23khW"
    skiable_terrain_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(7) > div.styles_metric__14Z7T"
    skiable_terrain_title, skiable_terrain_metric = extract_box_info(
        skiable_terrain_title_xpath, skiable_terrain_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", skiable_terrain_title)
    print("Metric:", skiable_terrain_metric)
    # Extract information for snow making total
    snow_making_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(8) > div.styles_title__23khW"
    snow_making_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > article:nth-child(6) > div:nth-child(2) > div:nth-child(8) > div.styles_metric__14Z7T"
    snow_making_title, snow_making_metric = extract_box_info(
        snow_making_title_xpath, snow_making_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", snow_making_title)
    print("Metric:", snow_making_metric)
    # Extract information for snow making total
    #night_skiing_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[8]/div[3]"
    #night_skiing_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[8]/div[3]"
    #night_skiing_title_xpath, night_skiing_value_xpath = extract_box_info(
     #   night_skiing_title_xpath, night_skiing_value_xpath, by=By.CSS_SELECTOR)
    #print("Title:", night_skiing_title_xpath)
    #print("Metric:", night_skiing_value_xpath)
    # Extract information for base elevation
    base_elevation_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(8) > article > div:nth-child(2) > div.styles_title__23khW"
    base_elevation_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(8) > article > div:nth-child(2) > div.styles_metric__14Z7T"
    base_elevation_title, base_elevation_metric = extract_box_info(
        base_elevation_title_xpath, base_elevation_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", base_elevation_title)
    print("Metric:", base_elevation_metric)
    # Extract information for summit elevation
    summit_elevation_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(8) > article > div:nth-child(3) > div.styles_title__23khW"
    summit_elevation_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(8) > article > div:nth-child(3) > div.styles_metric__14Z7T"
    summit_elevation_title, summit_elevation_metric = extract_box_info(
        summit_elevation_title_xpath, summit_elevation_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", summit_elevation_title)
    print("Metric:", summit_elevation_metric)
    # Extract information for vertical drop
    vertical_elevation_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(8) > article > div:nth-child(4) > div.styles_title__23khW"
    vertical_elevation_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div:nth-child(8) > article > div:nth-child(4) > div.styles_metric__14Z7T"
    vertical_elevation_title, vertical_elevation_metric = extract_box_info(
        vertical_elevation_title_xpath, vertical_elevation_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", vertical_elevation_title)
    print("Metric:", vertical_elevation_metric)
    # Extract information for average snowfall
    average_snowfall_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(2) > div:nth-child(3) > div"
    average_snowfall_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(2) > div:nth-child(3) > span"
    average_snowfall_title, average_snowfall_metric = extract_box_info(
        average_snowfall_title_xpath, average_snowfall_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", average_snowfall_title)
    print("Metric:", average_snowfall_metric)
    # Extract information for years open
    years_open_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(2) > div:nth-child(2) > div"
    years_open_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(2) > div:nth-child(2) > span"
    years_open_title, years_open_metric = extract_box_info(
        years_open_title_xpath, years_open_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", years_open_title)
    print("Metric:", years_open_metric)
    # Extract information for days open last year
    days_open_last_year_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(2) > div:nth-child(1) > div"
    days_open_last_year_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(2) > div:nth-child(1) > span"
    days_open_last_year_title, days_open_last_year_metric = extract_box_info(
        days_open_last_year_title_xpath, days_open_last_year_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", days_open_last_year_title)
    print("Metric:", days_open_last_year_metric)
    # Extract information for days open last year
    projected_opening_title_xpath = " #__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(1) > div:nth-child(1) > div"
    projected_opening_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(1) > div:nth-child(1) > span > span.styles_desktopDate__1Djk-"
    projected_opening_title_xpath, projected_opening_value_xpath = extract_box_info(
        projected_opening_title_xpath, projected_opening_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", projected_opening_title_xpath)
    print("Metric:", projected_opening_value_xpath)
    # Extract information for days open last year
    projected_closing_title_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(1) > div:nth-child(2) > div"
    projected_closing_value_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_importantDates__LELVC > article > div.styles_box__1sXJN.styles_box__1iaJy > div:nth-child(1) > div:nth-child(2) > span > span.styles_desktopDate__1Djk-"
    projected_closing_title_xpath, projected_closing_value_xpath = extract_box_info(
        projected_closing_title_xpath, projected_closing_value_xpath, by=By.CSS_SELECTOR)
    print("Title:", projected_closing_title_xpath)
    print("Metric:", projected_closing_value_xpath)
    print('navigating to table')
    try:
        print('navigating to table')
        # Navigate to the page with the table
        table_link_xpath = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_bestTimeSnow__2KOHq > article > div.styles_box__m1CLQ > div > a"
        table_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, table_link_xpath))
        )
        table_link.click()

        # Wait for the page to fully load
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, 'body')))

        # Check if the table is inside an iframe and switch to it if needed
        # Replace with the actual iframe XPath if applicable
        iframe_css = "iframe#table-iframe"
        if len(driver.find_elements(By.CSS_SELECTOR, iframe_css)) > 0:
            iframe = driver.find_element(By.CSS_SELECTOR, iframe_css)
            driver.switch_to.frame(iframe)

        # Wait for the table to be present and visible
        table_css = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_wrap__1Y1Mv > div:nth-child(2) > div.styles_inner__3LR9h.ps > section > table"
        table_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, table_css))
        )

        # Locate the header row
        header_row_css = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_wrap__1Y1Mv > div:nth-child(2) > div.styles_inner__3LR9h.ps > section > table > thead > tr"
        header_row = table_element.find_element(By.CSS_SELECTOR, header_row_css)

        # Extract the headers
        headers = [cell.text for cell in header_row.find_elements(By.CSS_SELECTOR, "th")]

        # Get all the rows in the table body
        rows_css = "#__next > div.container-xl.content-container > div.styles_layout__2aTIJ.layout-container > div > div.styles_wrap__1Y1Mv > div:nth-child(2) > div.styles_inner__3LR9h.ps > section > table > tbody > tr"
        rows = table_element.find_elements(By.CSS_SELECTOR, rows_css)

        data = []
        for row in rows:
            row_data = {}
            
            # Extract the month value
            month_cell_css = "th"
            month_cell = row.find_element(By.CSS_SELECTOR, month_cell_css)
            row_data["Month"] = month_cell.text
            
            # Extract the values for each column
            columns_css = "td"
            columns = row.find_elements(By.CSS_SELECTOR, columns_css)
            for i in range(len(headers) - 1):
                if i < len(columns):
                    row_data[headers[i + 1]] = columns[i].text
                else:
                    row_data[headers[i + 1]] = None
            
            data.append(row_data)
    except (TimeoutException, NoSuchElementException):
        print("Table extraction failed. Moving on without table data.")
        data = []
    # Prepare the response data
    response_data = {
        'beginner_runs': {'metric': clean_data(beginner_metric)},
        'intermediate_runs': {'metric': clean_data(intermediate_metric)},
        'advanced_runs': {'metric': clean_data(advanced_metric)},
        'expert_runs': {'metric': clean_data(expert_metric)},
        'runs_in_total': {'metric': clean_data(runs_in_total_metric)},
        'longest_run': {'metric': clean_data(longest_run_metric)},
        'skiable_terrain': {'metric': clean_data(skiable_terrain_metric)},
        'snowMaking': {'metric': clean_data(snow_making_metric)},
        'baseElevation': {'metric': clean_data(base_elevation_metric)},
        'topElevation': {'metric': clean_data(summit_elevation_metric)},
        'verticalDrop': {'metric': clean_data(vertical_elevation_metric)},
        'averageSnowfall': {'metric': clean_data(average_snowfall_metric)},
        'yearsOpen': {'metric': clean_data(years_open_metric)},
        'daysOpenLastYear': {'metric': clean_data(days_open_last_year_metric)},
        'phoneNumber': {'title': clean_data(resort_info)},
        'total_lifts': {'metric': clean_data(total_lifts_cleaned)},
        'projectedOpening': {'metric': clean_data(projected_opening_value_xpath)},
        'projectedClosing': {'metric': clean_data(projected_closing_value_xpath)},
        ##'phone_number': {'title': clean_data(phone_number_xpath)},
        'table_data': [
            {
                'Month': clean_data(row['Month']),
                'Snowfall Days': clean_data(row['Snowfall Days']) if 'Snowfall Days' in row else None,
                'Average Base Depth': clean_data(row['Average Base Depth']) if 'Average Base Depth' in row else None,
                'Average Summit Depth': clean_data(row['Average Summit Depth']) if 'Average Summit Depth' in row else None,
                'Max Base Depth': clean_data(row['Max Base Depth']) if 'Max Base Depth' in row else None,
                'Biggest Snowfall': clean_data(row['Biggest Snowfall']) if 'Biggest Snowfall' in row else None
            }
            for row in data
        ]
    }

    # Format the JSON response with indentation and sorting
    formatted_response = json.dumps(response_data, indent=2, sort_keys=True)

    # Return the formatted JSON response
    return formatted_response, 200, {'Content-Type': 'application/json'}



@app.route('/ski-resort-lodging', methods=['POST'])
def get_ski_resort_lodging():
    # Get the URL from the request data
    url = request.json['url']

    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Navigate to the specified URL
    driver.get(url)

    # Wait for the page to fully load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Get the parent div containing the lodge articles
    parent_div_xpath = "//*[@id='__next']/div[6]/div[3]/div/div"
    parent_div_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, parent_div_xpath))
    )

    # Get all the article elements within the parent div
    article_xpath = "./div/article"
    article_elements = parent_div_element.find_elements(By.XPATH, article_xpath)

    lodges = []
    for article in article_elements:
        # Extract the lodge title
        title_xpath = "./div[2]/h3/span"
        title_element = WebDriverWait(article, 10).until(
            EC.presence_of_element_located((By.XPATH, title_xpath))
        )
        title = title_element.text
        title = clean_data(title)

        lodges.append({'title': title})

    # Prepare the response data
    response_data = {
        'lodges': lodges
    }

    # Format the JSON response with indentation and sorting
    formatted_response = json.dumps(response_data, indent=2, sort_keys=True)

    # Return the formatted JSON response
    return formatted_response, 200, {'Content-Type': 'application/json'}



@app.route('/ski-info-route', methods=['GET'])
def get_ski_info():
    # Create a new instance of the Chrome driver
    driver = webdriver.Chrome()

    # Navigate to the initial page
    url = 'https://www.skiresort.info/ski-resorts/canada/page/2/'
    driver.get(url)
    print(f"Navigated to initial page: {url}")

    ski_resorts_data = []
    page_number = 2  # Starting from page 2
    start_scraping = False

    while page_number <= 3:
        print(f"Scraping page {page_number}...")

        # Find all ski resort links on the current page
        resort_links = driver.find_elements(By.CSS_SELECTOR, 'div[id^="resort"] > div > div:nth-child(1) > div.col-sm-11.col-xs-10 > div.h3 > a')
        print(f"Found {len(resort_links)} resort links on page {page_number}")

        for resort_link in resort_links:
            resort_url = resort_link.get_attribute('href')
            print(f"Resort URL: {resort_url}")

            if not start_scraping:
                if resort_url == 'https://www.skiresort.info/ski-resort/vista-ridge/':
                    start_scraping = True
                else:
                    continue

            # Check if the resort URL contains "cat-skiing/" or "heliskiing/"
            if "cat-skiing/" in resort_url or "heliskiing/" in resort_url:
                print(f"Skipping resort: {resort_url}")
                continue

            print(f"Opening resort URL: {resort_url}")
            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[-1])
            driver.get(resort_url)

            try:
                resort_name = clean_data(driver.find_element(By.CSS_SELECTOR, '#c50 > div.subnavi-header > div > div.col-sm-10 > h1 > span > span').text)
                resort_name = resort_name.replace("Ski resort ", "")  # Remove "Ski resort" from the name
            except NoSuchElementException:
                resort_name = ''

            try:
                description = clean_data(driver.find_element(By.CSS_SELECTOR, '#main-content > div.panel-simple.more-padding > p').text)
            except NoSuchElementException:
                description = ''

            try:
                elevation_data = clean_data(driver.find_element(By.XPATH, '//*[@id="selAlti"]').text)
            except NoSuchElementException:
                elevation_data = ''

            if elevation_data:
                elevation_parts = elevation_data.split(' - ')
                if len(elevation_parts) == 2:
                    base_elevation = elevation_parts[0].split(' ')[0]
                    top_elevation = elevation_parts[1].split(' ')[0]
                else:
                    base_elevation, top_elevation = '', ''
            else:
                base_elevation, top_elevation = '', ''

            try:
                lifts_total = clean_data(driver.find_element(By.CSS_SELECTOR, '#main-content > div.panel-simple.more-padding > a.shaded.detail-links.link-img.no-pad-bottom > div.description > div > strong#selLiftstot').text)
                lifts_total = re.sub(r'\D', '', lifts_total)
            except NoSuchElementException:
                lifts_total = ''

            try:
                skiable_km = clean_data(driver.find_element(By.XPATH, '//*[@id="selSlopetot"]').text)
            except NoSuchElementException:
                skiable_km = ''

            ski_resort_data = {
                'name': resort_name,
                'information': description,
                'baseElevation': base_elevation,
                'topElevation': top_elevation,
                'totalLifts': lifts_total,
                'skiable_terrain': skiable_km
            }

            # Send the individual ski resort data to the /ingest endpoint
            ingest_url = 'http://localhost:3000/resorts/ingest'
            response = requests.post(ingest_url, data=ski_resort_data)
            print(f"Sent data to /ingest endpoint for resort: {resort_name}. Response: {response.status_code}")

            ski_resorts_data.append(ski_resort_data)
            print(f"Scraped data for resort: {resort_name}")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

        # Navigate to the next page
        page_number += 1
        if page_number <= 3:
            next_page_url = f'https://www.skiresort.info/ski-resorts/canada/page/{page_number}/'
            print(f"Navigating to page {page_number}: {next_page_url}")
            driver.get(next_page_url)

    driver.quit()
    print(f"Scraped data for {len(ski_resorts_data)} ski resorts")

    return jsonify(ski_resorts_data)

if __name__ == '__main__':
    app.run()
