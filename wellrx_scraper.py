from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import re
from operator import itemgetter 
import csv

drug_list = ["LEVOTHYROXINE SODIUM", "LISINOPRIL", "ATORVASTATIN CALCIUM", "METFORMIN HCL", "AMLODIPINE BESYLATE", "METOPROLOL TARTRATE", "OMEPRAZOLE", "SIMVASTATIN", "LOSARTAN POTASSIUM", "ALBUTEROL SULFATE", "GABAPENTIN", "HYDROCHLOROTHIAZIDE", "HYDROCODONE-ACETAMINOPHEN", "SERTRALINE HCL", "FUROSEMIDE", "AMOXICILLIN", "ALPRAZOLAM", "ATENOLOL", "CITALOPRAM HBR", "LANTUS", "MONTELUKAST SODIUM", "TRAZODONE HCL", "ESCITALOPRAM OXALATE", "PANTOPRAZOLE SODIUM", "PRAVASTATIN SODIUM", "BUPROPION XL", "FLUOXETINE HCL", "CARVEDILOL", "PREDNISONE", "FLUTICASONE PROPIONATE"]
city_list = ['New York', 'Los Angeles', 'Chicago', 'Dallas', 'Houston', 'Washington, DC', 'Miami', 'Philadelphia', 'Atlanta', 'Boston', 'Phoenix', 'San Francisco', 'Riverside, CA', 'Detroit', 'Seattle', 'Minneapolis','San Diego','Tampa', 'Denver', 'St Louis', 'Baltimore', 'Orlando', 'Charlotte', 'San Antonio', 'Portland', 'Sacramento', 'Pittsburgh', 'Las Vegas', 'Cincinnati', 'Austin']
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')  # Last I checked this was necessary.
driver = webdriver.Chrome(options=options)

delay = 10 # seconds

csv_columns = ['drug','city','name','address','price']
with open('scrapedprices.csv', 'a') as f:
	writer = csv.DictWriter(f, fieldnames = csv_columns)
	writer.writeheader()
	for i in drug_list:
		for c in city_list:
			driver.get(f'https://www.wellrx.com/prescriptions/{i}/{c}')
			try:
			    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "price-list-item")]')))
			    print (f"Page loaded: {i} {c}")
			except TimeoutException:
			    print ("Timeout!")
			results = driver.find_elements_by_xpath('//div[contains(@class, "price-list-item")]')
			pharmacy_list = []
			pharmacy_dict = {}	
			for x in results:
				name = x.find_element_by_xpath('.//p[starts-with(@id, "y")]').text
				address = x.find_element_by_xpath('.//address[contains(@id, "adr")]').text
				price_string = x.find_element_by_xpath('.//p[starts-with(@id, "pr")]').text
				price = float(re.sub(r'(.*\s*.*)\$', '', price_string))
				pharmacy_dict = {'drug': i, 'city': c, 'name': name, 'address': address, 'price': price}
				pharmacy_list.append(pharmacy_dict)
			writer.writerows(pharmacy_list)