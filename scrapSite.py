import time
import os
from urllib.request import urlopen
from selenium import webdriver

# Write a python code to get images and meta-data from this page:
# https://images.nasa.gov/
#
# Need "medium" image and all metadata, such as:
# NASA ID: NHQ201805170022
# Keywords: DC, Jim Bridenstine, NASA Headquarters, Town Hall, Washington
# Center: HQ
# Date Created: 2018-05-17
# Visit HQ Website
# NASA Administrator Jim Bridenstine is seen during a NASA town hall event, Thursday, May 17, 2018 at NASA Headquarters in Washington. Photo Credit: (NASA/Bill Ingalls)
#
#
# Write image as {nasa_id}.gif (or .tif or whatever)
# Write meta data as test to {nasa_id}.txt
#
# Don't use the NASA API.
#
# Please send the code here when done and tested. Harvest the first page only (no search results). Good luck.

my_url = 'https://images.nasa.gov/'
chromedriver = './chromedriver'
urls = []

driver = webdriver.Chrome(chromedriver)
driver.get(my_url)

time.sleep(2)
p_element = driver.find_element_by_id(id_='landing-assets')


def get_data():
    return {'id': 'VAFB-20180501-PH_RKB04_0038'}


def save_img(nasa_id):
    nato_img_src = get_image_src()
    file = set_file_name(nasa_id)

    # download the image
    print(nato_img_src)
    if nato_img_src:
        resource = urlopen(nato_img_src)
        # time.sleep(2)
        if resource:
            with open(file, 'wb') as f:
                f.write(resource.read())
            print('Saved file %s' % file)


def get_image_src():
    # get the image source
    nato_img = driver.find_element_by_id('details_img')
    nato_img_src = nato_img.get_attribute('src')
    print(nato_img)
    print(nato_img_src)
    return nato_img_src


def set_file_name(nasa_id):
    # set file name
    dir_name = 'parsedData'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    filename = '%s' % nasa_id
    suffix = '.png'
    file = os.path.join(dir_name, filename + suffix)
    return file


if p_element:
    img_elements = driver.find_elements_by_css_selector('#landing-assets a.recent')
    print(1)
    for element in img_elements:
        href = element.get_attribute('href')
        urls.append(href)
        print(href)

    for url in urls:
        driver.get(url)
        time.sleep(2)
        data = get_data()

        if data['id']:
            save_img(data['id'])

driver.close()
