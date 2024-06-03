from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re

app = Flask(__name__)


def clean_data(data):
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

    def extract_box_info(title_xpath, metric_xpath=None):
        # Wait for the title element to be present
        title_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, title_xpath))
        )
        title_text = title_element.text

        if metric_xpath:
            # Wait for the metric element to be present
            metric_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, metric_xpath))
            )
            metric_text = metric_element.text
        else:
            metric_text = None

        return title_text, metric_text

    # Extract information for beginner runs
    beginner_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[1]/div[2]"
    beginner_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[1]/div[3]"
    beginner_title, beginner_metric = extract_box_info(
        beginner_title_xpath, beginner_metric_xpath)

    # Extract information for intermediate runs
    intermediate_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[3]/div[2]"
    intermediate_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[2]/div[3]"
    intermediate_title, intermediate_metric = extract_box_info(
        intermediate_title_xpath, intermediate_metric_xpath)

    # Extract information for advanced runs
    advanced_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[3]/div[2]"
    advanced_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[3]/div[3]"
    advanced_title, advanced_metric = extract_box_info(
        advanced_title_xpath, advanced_metric_xpath)
    # Extract information for resort info
    resort_info_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[2]/div[2]/div[1]"
    resort_info, _ = extract_box_info(resort_info_xpath)
    # Extract information for expert runs
    expert_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[4]/div[2]"
    expert_metric_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[4]/div[3]"
    expert_title, expert_metric = extract_box_info(
        expert_title_xpath, expert_metric_xpath)

    # Extract information for resort info
    total_lifts_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[5]/article/div[1]/h3"
    total_lifts_xpath, _ = extract_box_info(total_lifts_xpath)

    # Extract information for runs total
    runs_in_total_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[5]/div[2]"
    runs_in_total_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[5]/div[3]"
    runs_in_total_title, runs_in_total_metric = extract_box_info(
        runs_in_total_xpath, runs_in_total_value_xpath)

    # Extract information for resort info
    phone_number_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[9]/article/div[2]/div[1]/div/div[2]/p/a"
    phone_number_xpath, _ = extract_box_info(phone_number_xpath)

    # Extract information for longest run total
    longest_run_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[6]/div[2]"
    longest_run_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[6]/div[3]"
    longest_run_title, longest_run_metric = extract_box_info(
        longest_run_title_xpath, longest_run_value_xpath)

    # Extract information for skiable terrain total
    skiable_terrain_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[7]/div[2]"
    skiable_terrain_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[7]/div[3]"
    skiable_terrain_title, skiable_terrain_metric = extract_box_info(
        skiable_terrain_title_xpath, skiable_terrain_value_xpath)

    # Extract information for snow making total
    snow_making_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[9]/div[2]"
    snow_making_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[8]/div[3]"
    snow_making_title, snow_making_metric = extract_box_info(
        snow_making_title_xpath, snow_making_value_xpath)

    # Extract information for snow making total
    night_skiing_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[9]/div[2]"
    night_skiing_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/article[2]/div[2]/div[8]/div[3]"
    night_skiing_title_xpath, night_skiing_value_xpath = extract_box_info(
        night_skiing_title_xpath, night_skiing_value_xpath)
    # Extract information for base elevation
    base_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[2]/div[2]"
    base_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[2]/div[3]"
    base_elevation_title, base_elevation_metric = extract_box_info(
        base_elevation_title_xpath, base_elevation_value_xpath)

    # Extract information for summit elevation
    summit_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[3]/div[2]"
    summit_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[3]/div[3]"
    summit_elevation_title, summit_elevation_metric = extract_box_info(
        summit_elevation_title_xpath, summit_elevation_value_xpath)

    # Extract information for vertical drop
    vertical_elevation_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[4]/div[2]"
    vertical_elevation_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[6]/article/div[4]/div[3]"
    vertical_elevation_title, vertical_elevation_metric = extract_box_info(
        vertical_elevation_title_xpath, vertical_elevation_value_xpath)

    # Extract information for average snowfall
    average_snowfall_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[2]/div[3]/div"
    average_snowfall_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[2]/div[3]/span"
    average_snowfall_title, average_snowfall_metric = extract_box_info(
        average_snowfall_title_xpath, average_snowfall_value_xpath)

    # Extract information for years open
    years_open_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[2]/div[2]/div"
    years_open_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[2]/div[2]/span"
    years_open_title, years_open_metric = extract_box_info(
        years_open_title_xpath, years_open_value_xpath)

    # Extract information for days open last year
    days_open_last_year_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[2]/div[1]/div"
    days_open_last_year_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[2]/div[1]/span"
    days_open_last_year_title, days_open_last_year_metric = extract_box_info(
        days_open_last_year_title_xpath, days_open_last_year_value_xpath)

    # Extract information for days open last year
    projected_opening_title_xpath = " //*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[1]/div[1]/div"
    projected_opening_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[1]/div[1]/span/span[1]"
    projected_opening_title_xpath, projected_opening_value_xpath = extract_box_info(
        projected_opening_title_xpath, projected_opening_value_xpath)

    # Extract information for days open last year
    projected_closing_title_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[1]/div[2]/div"
    projected_closing_value_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[8]/article/div[2]/div[1]/div[2]/span/span[1]"
    projected_closing_title_xpath, projected_closing_value_xpath = extract_box_info(
        projected_closing_title_xpath, projected_closing_value_xpath)
    # Navigate to the page with the table
    table_link_xpath = "//*[@id='__next']/div[6]/div[2]/div/div[2]/a[8]"
    table_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, table_link_xpath))
    )
    table_link.click()

    # Wait for the page to fully load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # Check if the table is inside an iframe and switch to it if needed
    # Replace with the actual iframe XPath if applicable
    iframe_xpath = "//iframe[@id='table-iframe']"
    if len(driver.find_elements(By.XPATH, iframe_xpath)) > 0:
        iframe = driver.find_element(By.XPATH, iframe_xpath)
        driver.switch_to.frame(iframe)

    # Wait for the table to be present and visible
    table_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[1]/div[1]/div[3]/section/table"
    table_element = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, table_xpath))
    )

    # Locate the header row
    header_row_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[1]/div[1]/div[3]/section/table/thead/tr"
    header_row = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, header_row_xpath))
    )

    # Extract the headers
    headers = [cell.text for cell in header_row.find_elements(
        By.XPATH, "./th/span")]

    # Get all the rows in the table
    rows_xpath = "//*[@id='__next']/div[6]/div[3]/div/div[1]/div[1]/div[3]/section/table/tbody/tr"
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, rows_xpath))
    )

    data = []
    for row in rows:
        row_data = {"Month": row.find_element(By.XPATH, "./th/span").text}
        for i in range(1, len(headers)):
            column_element = WebDriverWait(row, 10).until(
                EC.presence_of_element_located((By.XPATH, f"./td[{i}]/span"))
            )
            row_data[headers[i]
                     ] = column_element.text if column_element.text else None
        data.append(row_data)

    # Prepare the response data
    response_data = {
        'beginner_runs': {'title': clean_data(beginner_title), 'metric': clean_data(beginner_metric)},
        'intermediate_runs': {'title': clean_data(intermediate_title), 'metric': clean_data(intermediate_metric)},
        'advanced_runs': {'title': clean_data(advanced_title), 'metric': clean_data(advanced_metric)},
        'expert_runs': {'title': clean_data(expert_title), 'metric': clean_data(expert_metric)},
        'runs_in_total': {'title': clean_data(runs_in_total_title), 'metric': clean_data(runs_in_total_metric)},
        'longest_run': {'title': clean_data(longest_run_title), 'metric': clean_data(longest_run_metric)},
        'skiable_terrain': {'title': clean_data(skiable_terrain_title), 'metric': clean_data(skiable_terrain_metric)},
        'snow_making': {'title': clean_data(snow_making_title), 'metric': clean_data(snow_making_metric)},
        'base_elevation': {'title': clean_data(base_elevation_title), 'metric': clean_data(base_elevation_metric)},
        'summit_elevation': {'title': clean_data(summit_elevation_title), 'metric': clean_data(summit_elevation_metric)},
        'vertical_drop': {'title': clean_data(vertical_elevation_title), 'metric': clean_data(vertical_elevation_metric)},
        'average_snowfall': {'title': clean_data(average_snowfall_title), 'metric': clean_data(average_snowfall_metric)},
        'years_open': {'title': clean_data(years_open_title), 'metric': clean_data(years_open_metric)},
        'days_open_last_year': {'title': clean_data(days_open_last_year_title), 'metric': clean_data(days_open_last_year_metric)},
        'resort_info': {'title': clean_data(resort_info)},
        'total_lifts': {'title': clean_data(total_lifts_xpath)},
        'projected_opening': {'title': clean_data(projected_opening_title_xpath), 'metric': clean_data(projected_opening_value_xpath)},
        'projected_closing': {'title': clean_data(projected_closing_title_xpath), 'metric': clean_data(projected_closing_value_xpath)},
        'phone_number': {'title': clean_data(phone_number_xpath)},
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

if __name__ == '__main__':
    app.run()
