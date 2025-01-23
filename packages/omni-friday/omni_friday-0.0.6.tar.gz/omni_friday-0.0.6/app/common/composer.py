import json
import os

def read_composer_file():
    file_path = os.path.join(os.getcwd(), 'composer.lock')
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def extract_magento_info(data):
    packages = data['packages']
    magento_info = {}
    isCloud = False

    for package in packages:
        if 'magento/magento-cloud-metapackage' in package['name']:
            isCloud = True

        if 'magento/product-enterprise-edition' in package['name']:
            magento_info['commerce'] = {
                'edition': 'Adobe Commerce',
                'version': package['version']
            }
            

        if 'magento/product-community-edition' in package['name']:
            magento_info['opensource'] = {
                'edition': 'Magento Open Source',
                'version': package['version']
            }
            
    if('commerce' in magento_info):
        info = magento_info['commerce']
        if isCloud:
            info['edition'] = 'Adobe Commerce Cloud'
            
        return magento_info['commerce']
    
    return magento_info['opensource']