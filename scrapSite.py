import time
import os
from urllib.request import urlopen
from selenium import webdriver

my_url = 'https://images.nasa.gov/'
chromedriver = './chromedriver'
urls = []

driver = webdriver.Chrome(chromedriver)


## Selenium helpers
def get_elements_by_css_locator(locator):
    result = None
    try:
        result = driver.find_elements_by_css_selector(locator)
    except Exception as exception:
        print('Cannot find {}. Exception: {}'.format(locator, exception))
    return result


def get_element_by_css_locator(locator):
    result = None
    try:
        result = driver.find_element_by_css_selector(locator)
    except Exception as exception:
        print('Cannot find {}. Exception: {}'.format(locator, exception))
    return result


def get_element_by_id(locator):
    result = None
    try:
        result = driver.find_element_by_id(locator)
    except Exception as exception:
        print('Cannot find {}. Exception: {}'.format(locator, exception))
    return result


def get_page(page_url):
    print(page_url)
    driver.get(page_url)
    time.sleep(2)


get_page(my_url)

p_element = get_element_by_id('landing-assets')


def get_data():
    nato_id = get_element_by_css_locator('#detail-metadata span')
    keywords = get_elements_by_css_locator('#detail-keywords a')
    location = get_element_by_css_locator("span[editable-text='media.Location']")
    photographer = get_element_by_css_locator('span[e-form="editPhotographer"]')
    size = get_element_by_css_locator("li[ng-If='mediaFileSize'] span")
    data_format = get_element_by_css_locator('[ng-if="mediaFileExt"] span')
    center = get_element_by_css_locator('[data-ng-if="media.Center || editAsset === true"] span')
    created = get_element_by_css_locator("#edit-dateCreated span[e-form='editDateCreated']")
    description = get_element_by_css_locator('#editDescription')
    data_href = get_element_by_css_locator('[data-ng-if="media.Center.website"] a')

    return {
        'id': nato_id.text if nato_id else '-',
        'keywords': [x.text for x in keywords] if keywords else '-',
        'location': location.text if location else '-',
        'photographer': photographer.text if photographer else '-',
        'size': size.text if size else '-',
        'data_format': data_format.text if data_format else '-',
        'center': center.text if center else '-',
        'created': created.text if created else '-',
        'description': description.text if description else '-',
        'href': data_href.get_attribute('href') if data_href else '-',
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
    nato_img = get_element_by_id('details_img')
    nato_img_src = nato_img.get_attribute('src')
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
    img_elements = get_elements_by_css_locator('#landing-assets a.recent')

    for element in img_elements:
        href = element.get_attribute('href')
        urls.append(href)

    for url in urls:
        get_page(url)
        data = get_data()

        if data:
            if data['id']:
                save_meta_data(data, data['id'])
                save_img(data['id'])

driver.close()
