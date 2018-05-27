import time
import os
from urllib.request import urlopen
from selenium import webdriver


my_url = 'https://images.nasa.gov/'
chromedriver = './chromedriver'
urls = []

driver = webdriver.Chrome(chromedriver)
driver.get(my_url)

time.sleep(2)
p_element = driver.find_element_by_id(id_='landing-assets')


def get_data():

    nato_id = driver.find_element_by_css_selector('#detail-metadata span')
    keywords = driver.find_elements_by_css_selector('#detail-metadata span')
    location = driver.find_element_by_css_selector('#detail-metadata span')
    photographer = driver.find_element_by_css_selector('#detail-metadata span')
    size = driver.find_element_by_css_selector('#detail-metadata span')
    data_format = driver.find_element_by_css_selector('#detail-metadata span')
    center = driver.find_element_by_css_selector('#detail-metadata span')
    created = driver.find_element_by_css_selector('#detail-metadata span')
    description = driver.find_element_by_css_selector('#detail-metadata span')
    data_href = driver.find_element_by_css_selector('#detail-metadata span')

    return {
        'id': nato_id.text if nato_id else '-',
        'keywords': [x.text for x in keywords] if keywords else '-',
        'location': location if location else '-',
        'photographer': photographer if photographer else '-',
        'size': size if size else '-',
        'data_format': data_format if data_format else '-',
        'center': center if center else '-',
        'created': created if created else '-',
        'description': description if description else '-',
        'href': data_href if data_href else '-',
    }


def save_img(nasa_id):
    nato_img_src = get_image_src()
    file = set_file_name(nasa_id, 'image')

    # download the image
    print(nato_img_src)
    if nato_img_src:
        resource = urlopen(nato_img_src)
        if resource:
            with open(file, 'wb') as f:
                f.write(resource.read())
            print('Saved file %s' % file)


def save_meta_data(data, nasa_id):
    file = set_file_name(nasa_id)
    if file:
        text = '\n'.join("{!s}={!r}".format(k, v) for (k, v) in data.items())
        if text:
            with open(file, 'w') as f:
                print("{}".format(text), file=f)
            print('Saved file %s' % file)


def get_image_src():
    # get the image source
    nato_img = driver.find_element_by_id('details_img')
    nato_img_src = nato_img.get_attribute('src')
    print(nato_img)
    return nato_img_src


def set_file_name(nasa_id, file_type=None):
    # set file name
    dir_name = 'parsedData'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    filename = '%s' % nasa_id
    suffix = '.png' if file_type == 'image' else '.txt'
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

        if data:
            if data['id']:
                save_meta_data(data, data['id'])
                save_img(data['id'])

driver.close()
