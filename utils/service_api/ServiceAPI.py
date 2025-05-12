import logging
import allure
import requests
import pytest

log = logging


class ServiceAPI:
    def __init__(self):
        pass

    def get_service_reponse(self, api_url):
        response = None
        with allure.step('Get the response data for given API service call'):
            log.info('Get the response data for given API service call')
            try:
                response = requests.get(api_url)
                log.info('Service request status code = {}'.format(response.status_code))
            except Exception as e:
                log.info('Service request error status code = {}'.format(response.status_code))
                pytest.fail(str(e))
        return response


if __name__ == '__main__':
    url = "https://appnot.viewglass.com/root/relaydata/55055/ncconfig.txt"
    obj = ServiceAPI()
    opt = obj.get_service_reponse(url)
    print(opt.text)
