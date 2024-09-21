# LIBRARIES

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import schedule
import sqlite3

connection = sqlite3.connect("appliedurls.db")     #Connect to database and create it if does not exist
cursor = connection.cursor()     

cursor.execute("CREATE TABLE IF NOT EXISTS Links(Link TEXT)")     #Execute the SQL querie to Create the Table

# CONSTANTS

home_page_url = "https://www.daft.ie/sharing/dublin-city?radius=10000&rentalPrice_to=800&roomType=single&sort=publishDateDesc"
#applied_urls = set()
announcement_number = 1

# FUNCTIONS

def click_element(driver, by, locator):
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, locator)))
        element.click()
    except TimeoutException:
        print(f"Element with {by}='{locator}' not found within the specified time.")
    except NoSuchElementException:
        print(f"Element with {by}='{locator}' not found. Check the selectors.")

def scroll_down(driver, pixels=400):
    try:
        driver.execute_script(f"window.scrollTo(0, {pixels});")
    except:
        print("Scroll down was not possible.")

def return_to_main_page(driver):
    # RETURN TO MAIN PAGE
    time.sleep(1)
    driver.back()
    time.sleep(1)

def open_chrome():
    # OPEN CHROME
    driver = webdriver.Chrome()
    driver.get(home_page_url)
    driver.maximize_window()
    time.sleep(0.5)
    return driver

def sign_in(driver):

    # ACCEPT ALL COOKIES BUTTON
    click_element(driver, By.XPATH, "//span[contains(text(), 'Accept All')]")
    time.sleep(0.5)

    # CLICK SIGN IN BUTTON
    click_element(driver, By.XPATH, '//*[@id="__next"]/header/div/div[2]/div[3]/ul/li/a')
    time.sleep(0.5)

    # ENTER CREDENTIALS
    username_locator = (By.CSS_SELECTOR, "input[name='username']")
    password_locator = (By.CSS_SELECTOR, "input[name='password']")

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(username_locator))
    username.clear()
    username.send_keys("guillermoteniasmoron@hotmail.com")

    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(password_locator))
    password.clear()
    password.send_keys("yourpassword")

    sign_in_button_locator = (By.XPATH, '//*[@id="login"]')
    click_element(driver, *sign_in_button_locator)
    time.sleep(0.5)

def search_and_click(driver, announcement_number):

    # SEARCH AND CLICK
    #announcement_locator = (By.XPATH, f'//*[@id="__next"]/main/div[3]/div[1]/ul/li[{announcement_number}]/a/div[2]/div[1]/div[2]/div')    #FORMER ANNOUNCEMENT LOCATOR
    announcement_locator = (By.XPATH, f'//*[@id="__next"]/main/div[3]/div[1]/ul/li[{announcement_number}]/a')
    #//*[@id="__next"]/main/div[3]/div[1]/ul/li[1]/a
    #//*[@id="__next"]/main/div[3]/div[1]/ul/li[2]/a
    #//*[@id="__next"]/main/div[3]/div[1]/ul/li[8]/a
    click_element(driver, *announcement_locator)

    #CHECK THE URL 
    current_url = driver.current_url
    return current_url

def apply(driver):

    # SCROLL DOWN
    scroll_down(driver)

    def element_exists(driver, locator):
        try:
            driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    #CLICK THE EMAIL AGENT BUTTON
    #email_agent_locator = (By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div/div[1]/div[2]/div[2]/button/div/span')  FORMER BUTTON CLICK, USED WITH A TRY-EXCEPT BLOCK

    #EMAIL(FOR PRIVATE USERS): 
    email_locator = (By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div/div[1]/div[2]/div[2]/button')

    #EMAIL AGENT OR AGENCIES: 
    email_agent_locator = (By.XPATH, '//*[@id="__next"]/main/div[3]/div[2]/div/div[1]/div[2]/div[2]/button')

    if element_exists(driver, email_locator):
        click_element(driver, *email_locator)

    elif element_exists(driver, email_agent_locator):
        click_element(driver, *email_agent_locator)

    else: 
        return_to_main_page()

    #FILL THE  EMAIL AGENT FORM
    time.sleep(1)
    first_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="keyword1"]')))
    #first_name.clear()                                                                  
    first_name.send_keys("Guillermo")

    last_name = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="keyword2"]')))
    #last_name.clear()
    last_name.send_keys("Tenias")

    email = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="keyword3"]')))
    #email.clear()
    email.send_keys("guillermoteniasmoron@hotmail.com")

    phone_number = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="keyword4"]')))
    #phone_number.clear()
    phone_number.send_keys("+34650919957")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, 2500);")  #SCROLL DOWN

    try:
        number_of_adults_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input-wrapper-adultTenants"]/div/div/div/button[2]'))).click()

    except:
        pass

    try:
     no_pets_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="hasPets"]/label[2]'))).click()
 
    except:
        pass

    try:
        moveindates_expandable_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="moveInDate"]'))).click()
        selectdate_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="input-wrapper-moveInDate"]/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[4]/div[5]'))).click()

    except:
        pass

    message = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="message"]')))
    message.clear()
    message.send_keys("""Hi there!

I'm Guillermo, a Spanish professional in my late twenties, currently working for a Hospitality Software company in Dublin City Center. I would describe myself as a laid-back individual who enjoys working on personal programming projects in my free time, as well as going to the gym and spending time with friends.

I am very interested in renting your room as it perfectly matches what I am looking for. I have been living in Ireland for over three years and can provide any references you may need, including previous landlord references and work references.

Thank you very much for considering my application.

Best regards,
Guillermo""")


    driver.execute_script("window.scrollTo(0, 500);")  #SCROLL DOWN
    try:
        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contact-form-modal"]/div[2]/form/div/div[6]/div/button'))).click()  #This is for email privates
    except:
        send_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contact-form-modal"]/div[2]/form/div/div[9]/div/button'))).click()  #This is for email agencies


    #CLICK THE X BUTTON
    time.sleep(1)
    x_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="contact-form-modal"]/div[1]/button/svg'))).click()

    #//*[@id="contact-form-modal"]/div[1]/button
    #//*[@id="contact-form-modal"]/div[1]/button/svg

    #RETURN TO MAIN PAGE
    return_to_main_page(driver)


# MAIN PROGRAM

def main_program():
    announcement_number = 1
    driver = open_chrome()
    sign_in(driver)

    while announcement_number <= 20:  # LOOP FOR THE DIFFERENT ANNOUNCEMENTS
        current_url = search_and_click(driver, announcement_number)

        #if current_url not in applied_urls: # FILTER TO APPLY OR NOT FOR THE ANNOUNCEMENT
        cursor.execute("SELECT * FROM Links WHERE Link = ?", (current_url,))
        result = cursor.fetchone()

        if result is None:
            # URL is not in the database, proceed to apply
            apply(driver)
    
            # Insert the URL into the database
            cursor.execute("INSERT INTO Links (Link) VALUES (?)", (current_url,))
    
            # Commit the changes to the database
            connection.commit()

        else:
            driver.quit()
            
        return_to_main_page(driver)
        driver.execute_script("window.scrollTo(0, 2500);")  #SCROLL DOWN IN THE MAIN PAGE TO GET TO THE NEXT ANNOUNCEMENT
        announcement_number += 1


main_program()
#FINISH THE PROGRAM

connection.commit()     #Close out the current transaction and applies the changes to the database
connection.close()   #Close the connection with the database
driver.quit()       #Close the current program

#SCHEDULE JOB
daily_schedule = schedule.every().monday.to("friday").at("07:00").to("22:00").do(main_program())
daily_schedule.every(10).minutes.do(main_program)
# schedule.every().monday.to("friday").at("07:00").to("22:00").do(main_program())
# schedule.every(10).minutes.do(main_program)
# schedule.every().minute.at(":00").do(main_program)

#RUN THE SCHEDULER

while True:
   schedule.run_pending()
   time.sleep(1)

