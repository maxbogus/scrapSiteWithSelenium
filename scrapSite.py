import os
from urllib.request import urlopen
from seleniumWrapper.client import SeleniumClient

client = SeleniumClient


def get_data():
    nato_id = client.get_element_by_css_locator(client, '#detail-metadata span')
    keywords = client.get_elements_by_css_locator(client, '#detail-keywords a')
    location = client.get_element_by_css_locator(client, "span[editable-text='media.Location']")
    photographer = client.get_element_by_css_locator(client, 'span[e-form="editPhotographer"]')
    size = client.get_element_by_css_locator(client, "li[ng-If='mediaFileSize'] span")
    data_format = client.get_element_by_css_locator(client, '[ng-if="mediaFileExt"] span')
    center = client.get_element_by_css_locator(client, '[data-ng-if="media.Center || editAsset === true"] span')
    created = client.get_element_by_css_locator(client, "#edit-dateCreated span[e-form='editDateCreated']")
    description = client.get_element_by_css_locator(client, '#editDescription')
    data_href = client.get_element_by_css_locator(client, '[data-ng-if="media.Center.website"] a')

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
    if nato_img_src:
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
    nato_img = client.get_element_by_id(client, 'details_img')
    return nato_img.get_attribute('src') if nato_img else None


def set_file_name(nasa_id, file_type=None):
    # set file name
    dir_name = 'parsedData'
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    filename = '%s' % nasa_id
    suffix = '.png' if file_type == 'image' else '.txt'
    file = os.path.join(dir_name, filename + suffix)
    return file


def parse_nasa_main_page():
    urls = []
    print('Parsing started.')
    client.open_nasa_site(client)
    if client.get_element_by_id(client, 'landing-assets'):
        img_elements = client.get_elements_by_css_locator(client, '#landing-assets a.recent')

        for element in img_elements:
            href = element.get_attribute('href')
            urls.append(href)

        for url in urls:
            client.get_page(client, page_url=url)
            data = get_data()

            if data:
                if data['id']:
                    save_meta_data(data, data['id'])
                    save_img(data['id'])
    print('Parsing complete.')
    client.terminate(client)


parse_nasa_main_page()
