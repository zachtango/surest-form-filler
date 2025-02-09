from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import json

# First, you'll need to install selenium:
# pip install selenium
# You'll also need to install a webdriver for your browser
# For Chrome: pip install webdriver-manager

# Load form data from JSON file
def load_form_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Load the form data
FORM_DATA = load_form_data('form_data.json')

def fill_form_1(driver, data):
    """
    Fill the form with provided data
    
    Args:
        driver: Selenium WebDriver instance
        data: Dictionary containing form field values
    """
    # Wait for forms to be present and fill them
    # Member ID
    member_id = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "QR~QID17"))
    )
    member_id.send_keys(data.get('member_id', ''))
    
    # First Name
    first_name = driver.find_element(By.ID, "QR~QID22~4")
    first_name.send_keys(data.get('first_name', ''))
    
    # Middle Initial
    middle_initial = driver.find_element(By.ID, "QR~QID22~5")
    middle_initial.send_keys(data.get('middle_initial', ''))
    
    # Last Name
    last_name = driver.find_element(By.ID, "QR~QID22~6")
    last_name.send_keys(data.get('last_name', ''))
    
    # Date of Birth
    dob = driver.find_element(By.ID, "QR~QID16")
    dob.send_keys(data.get('dob', ''))
    
    # Group Number
    group_number = driver.find_element(By.ID, "QR~QID51")
    group_number.send_keys(data.get('group_number', ''))
    
    # Employer Name
    employer = driver.find_element(By.ID, "QR~QID54")
    employer.send_keys(data.get('employer', ''))

    def click_dependent_button(driver):
        """
        Clicks the 'Dependent' radio button
        
        Args:
            driver: Selenium WebDriver instance
        """
        # Wait for the element to be present and clickable
        dependent_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "QR~QID2~3"))
        )
        
        # Try using JavaScript to click the element
        driver.execute_script("arguments[0].click();", dependent_button)
        time.sleep(1)  # Give it a moment to register the click

    click_dependent_button(driver)

def fill_form_2(driver, form_data):
    """
    Fills out the Surest claim form using the correct element IDs
    """
    # Wait for form to be loaded
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "QuestionBody"))
    )

    try:
        # Define field mappings with correct IDs
        fields = {
            # Name fields
            "first_name": "QR~QID1~4",
            "middle_initial": "QR~QID1~5",
            "last_name": "QR~QID1~6",
            
            # Member Info
            "member_id": "QR~QID8",
            "date_of_birth": "QR~QID9",
            
            # Address fields
            "street_address": "QR~QID53~4",
            "city": "QR~QID53~5",
            "state": "QR~QID53~6",
            "zip_code": "QR~QID53~7"
        }

        # Fill out each field
        for field_name, element_id in fields.items():
            if field_name in form_data:
                try:
                    field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, element_id))
                    )
                    field.clear()
                    field.send_keys(form_data[field_name])
                    print(f"Successfully filled {field_name}")
                except Exception as e:
                    print(f"Error filling {field_name}: {str(e)}")

    except Exception as e:
        print(f"General error in form filling: {str(e)}")

def click_next_button(driver):
    """
    Clicks the 'Next' button on the form
    
    Args:
        driver: Selenium WebDriver instance
    """
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "NextButton"))
    )
    next_button.click()

def fill_form_3(driver, data):
    """
    Fills out the foreign services form (3rd page)
    
    Args:
        driver: Selenium WebDriver instance
        data: Dictionary containing:
            - is_foreign: boolean, whether service was in foreign country
    """
    try:
        # Wait for radio buttons to be present
        if data.get('is_foreign', False):
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "QR~QID55~1"))
            )
        else:
            button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "QR~QID55~2"))
            )
        
        # Use JavaScript to click the button
        driver.execute_script("arguments[0].click();", button)
        time.sleep(1)  # Give it a moment to register the click
            
        print("Successfully filled form 3")
    except Exception as e:
        print(f"Error filling form 3: {str(e)}")

def fill_form_4(driver, data):
    """
    Fills out the service type and location form (4th page)
    
    Args:
        driver: Selenium WebDriver instance
        data: Dictionary containing:
            - service_type: string matching one of the dropdown options
            - place_of_service: string matching one of the dropdown options
    """
    try:
        # Wait for dropdowns to be present
        service_type_select = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "QR~QID66"))
        )
        place_of_service_select = driver.find_element(By.ID, "QR~QID67")
        
        # Create Select objects for the dropdowns
        from selenium.webdriver.support.ui import Select
        service_select = Select(service_type_select)
        place_select = Select(place_of_service_select)
        
        # Select the options
        if data.get('service_type'):
            service_select.select_by_visible_text(data['service_type'])
        if data.get('place_of_service'):
            place_select.select_by_visible_text(data['place_of_service'])
            
        print("Successfully filled form 4")
    except Exception as e:
        print(f"Error filling form 4: {str(e)}")

def fill_form_5(driver, data):
    """
    Fills out the provider information form (5th page)
    
    Args:
        driver: Selenium WebDriver instance
        data: Dictionary containing:
            - provider_name: string
            - provider_npi: string
            - provider_facility: string
            - provider_tin: string (9 digits, default 777777777)
            - provider_address: string
            - provider_city: string
            - provider_state: string (2-letter state code)
            - provider_zip: string
    """
    try:
        # Wait for form to be loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "QuestionBody"))
        )

        # Define field mappings with correct IDs
        fields = {
            "provider_name": "QR~QID71~1",
            "provider_npi": "QR~QID71~2",
            "provider_facility": "QR~QID71~3",
            "provider_tin": "QR~QID71~4",
            "provider_address": "QR~QID71~5",
            "provider_city": "QR~QID71~6",
            "provider_state": "QR~QID71~7",
            "provider_zip": "QR~QID71~8"
        }

        # Fill out each field
        for field_name, element_id in fields.items():
            if field_name in data:
                try:
                    field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, element_id))
                    )
                    field.clear()
                    field.send_keys(data[field_name])
                    print(f"Successfully filled {field_name}")
                except Exception as e:
                    print(f"Error filling {field_name}: {str(e)}")

    except Exception as e:
        print(f"General error in form filling: {str(e)}")

def fill_form_6(driver, data, index=0):
    """
    Fills out the services and charges form, handling multiple instances
    
    Args:
        driver: Selenium WebDriver instance
        data: Dictionary containing service info
        index: Integer (0 for first form, 1 for second, etc.)
    """
    # List of form QIDs and their corresponding "add another" QIDs
    FORM_IDS = [
        {"form": "QID25", "add_another": "QID69"},  # First form
        {"form": "QID68", "add_another": "QID74"},  # Second form
        {"form": "QID75", "add_another": "QID76"},  # Third form
        {"form": "QID77", "add_another": "QID78"},  # Fourth form
        {"form": "QID79", "add_another": "QID80"},  # Fifth form
        {"form": "QID81", "add_another": "QID82"},  # Sixth form
        {"form": "QID83", "add_another": "QID84"},  # Seventh form
        {"form": "QID85", "add_another": "QID86"},  # Eighth form
    ]

    try:
        # Get the correct IDs for this form index
        if index >= len(FORM_IDS):
            raise ValueError(f"No form IDs defined for index {index}")
        
        form_qid = FORM_IDS[index]["form"]
        add_another_qid = FORM_IDS[index]["add_another"]

        # Define field mappings using the correct QID
        fields = {
            "date_of_service": f"QR~{form_qid}#4~1~1~TEXT",
            "procedure_code": f"QR~{form_qid}#1~1~1~TEXT",
            "diagnosis_code": f"QR~{form_qid}#3~1~1~TEXT",
            "charges": f"QR~{form_qid}#2~1~1~TEXT"
        }

        # Fill out each field
        for field_name, element_id in fields.items():
            if field_name in data:
                try:
                    field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, element_id))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", field)
                    field.clear()
                    field.send_keys(data[field_name])
                    print(f"Successfully filled {field_name}")
                    time.sleep(0.5)
                except Exception as e:
                    print(f"Error filling {field_name}: {str(e)}")

        # Handle "Do you have another service to add?" radio buttons
        if 'add_another' in data:
            button_id = f"QR~{add_another_qid}~{1 if data['add_another'] else 2}"
            try:
                button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, button_id))
                )
                driver.execute_script("arguments[0].click();", button)
                print("Successfully selected add_another option")
            except Exception as e:
                print(f"Error selecting add_another option: {str(e)}")

    except Exception as e:
        print(f"General error in form filling: {str(e)}")

def fill_form_7(driver, data):
    """
    Fills out the charges summary form (7th page)
    
    Args:
        driver: Selenium WebDriver instance
        data: Dictionary containing:
            - total_charge: string (dollar amount)
            - amount_paid: string (dollar amount)
    """
    try:
        # Wait for form to be loaded
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "QuestionBody"))
        )

        # Define field mappings
        fields = {
            "total_charge": "QR~QID48~1",
            "amount_paid": "QR~QID48~2"
        }

        # Fill out each field
        for field_name, element_id in fields.items():
            if field_name in data:
                try:
                    field = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, element_id))
                    )
                    field.clear()
                    field.send_keys(data[field_name])
                    print(f"Successfully filled {field_name}")
                except Exception as e:
                    print(f"Error filling {field_name}: {str(e)}")

    except Exception as e:
        print(f"General error in form filling: {str(e)}")

def fill_form_11(driver, pdf_path):
    """
    Uploads a PDF file to the form
    
    Args:
        driver: Selenium WebDriver instance
        pdf_path: String path to the PDF file to upload
    """
    try:
        # Wait for the upload input element to be present
        # The file input is typically hidden, so we need to find it and send_keys to it
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        
        # Convert the path to absolute path
        absolute_path = os.path.abspath(pdf_path)
        
        # Send the file path to the input element
        file_input.send_keys(absolute_path)
        
        # Wait for upload to complete (look for the filename display or success message)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, "FileUploadName"))
        )
        
        print(f"Successfully uploaded PDF: {pdf_path}")
        
    except Exception as e:
        print(f"Error uploading PDF: {str(e)}")

def click_download_pdf(driver):
    """
    Clicks the download PDF button at the end of the form
    
    Args:
        driver: Selenium WebDriver instance
    """
    try:
        # Wait for the download button to be present and clickable
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "DownloadResponsesPDF"))
        )
        
        # Scroll the button into view
        driver.execute_script("arguments[0].scrollIntoView(true);", download_button)
        
        # Click the button
        download_button.click()
        
        print("Successfully clicked download PDF button")
        
    except Exception as e:
        print(f"Error clicking download PDF button: {str(e)}")

def click_button_on_website():
    # Set up the Chrome driver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    # Configure Chrome options
    chrome_options = Options()
    # chrome_options.add_argument('--headless')  # Run in headless mode (no GUI)
    
    # Initialize the driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    try:
        # Navigate to the website
        driver.get("https://survey.surest.com/jfe/form/SV_3VIAsFFJdsZZbDL")
        
        # Click Next button first to get to the form
        click_next_button(driver)
        
        # Fill form 1
        fill_form_1(driver, FORM_DATA["form_1"])
        click_next_button(driver)
        
        # Fill form 2
        fill_form_2(driver, FORM_DATA["form_2"])
        click_next_button(driver)
        
        # Fill form 3
        fill_form_3(driver, FORM_DATA["form_3"])
        click_next_button(driver)
        
        # Fill form 4
        fill_form_4(driver, FORM_DATA["form_4"])
        click_next_button(driver)
        
        # Fill form 5
        fill_form_5(driver, FORM_DATA["form_5"])
        click_next_button(driver)
        
        # Fill form 6 entries
        for index, entry in enumerate(FORM_DATA["form_6_entries"]):
            fill_form_6(driver, entry, index)
            click_next_button(driver)
        
        # Fill form 7
        fill_form_7(driver, FORM_DATA["form_7"])
        click_next_button(driver)
        
        # Upload PDF in form 11
        fill_form_11(driver, FORM_DATA["form_11"]["pdf_path"])
        click_next_button(driver)
        
        # # Click the download PDF button
        # click_download_pdf(driver)
        
        # Wait for user input before closing
        input("Press Enter to close the browser...")
        
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    click_button_on_website()
