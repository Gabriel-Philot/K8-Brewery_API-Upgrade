import requests
import json
import logging
import boto3
from pathlib import Path
from datetime import datetime
from resources.utils.utils import log_header

config_path = Path("src/resources/utils/configs.json")

with config_path.open('r') as config_file:
    config = json.load(config_file)

# Main class to interact with the OpenBreweryDB API
class BreweryRequestsApi:
    _Url_Brewery_API = config['api']['url']
    _bronze_path_file = Path(config['paths']['bronze'])

    def __init__(self, per_page: int = 100):
        self.per_page = per_page
    
    def _request_get(self, endpoint: str) -> dict:
        
        response = requests.get(self._Url_Brewery_API + endpoint)

        if response.status_code != 200:
            raise Exception(f"Unexpected response code: {response.status_code}. Details: {response.text}")

        if not isinstance(response.json(), (dict, list)):
            raise Exception(f"Response did not return a valid JSON object. Returned type: {type(response.json())}")

        return response.json()

    def _save_file(self, data_to_save: list, file_name: str = 'extracted_at_', bucket_name: str = 'my-bucket') -> None:
        # Define o nome do arquivo com base na data atual
        file_name += datetime.today().strftime('%Y_%m_%d') + '.json'

        # Converte os dados para o formato JSON
        data_to_save_json = '[' + ',\n'.join(json.dumps(record) for record in data_to_save) + ']\n'

        try:
            s3_client = boto3.client(
                's3',
                endpoint_url = 'http://minio.deepstorage.svc.cluster.local:9000',  # Alterar para o seu endpoint MinIO
                aws_access_key_id='miniouser',    # Coloque sua chave de acesso
                aws_secret_access_key='miniosecret' # Coloque sua chave secreta
            )

            # lakehouse/bronze_layer
            bucket_name = 'lakehouse'
            key = f"bronze_layer/{file_name}"

            # Carrega o arquivo JSON para o MinIO
            s3_client.put_object(Bucket=bucket_name, Key=key, Body=data_to_save_json)
            logging.info(f"[SUCCESS] | File {file_name} saved successfully to MinIO.")

        except Exception as e:
            logging.critical(f"[ERROR] | FAILED TO SAVE DATA TO MINIO. ERROR: {str(e)}")

    def _total_pages(self) -> dict:
        total_pages = self._request_get(endpoint='/meta')

        total_registres = total_pages.get('total')
        if total_registres is None:
            raise KeyError('The key "total" was not found in the response metadata.')

        total_registres = int(total_pages.get('total'))
        num_pages = (total_registres // self.per_page) + (1 if total_registres % self.per_page > 0 else 0)

        page_data = {
            'page_list': [page + 1 for page in range(num_pages)],
            'total_records': total_registres
        }

        return page_data

    def extract_data(self) -> None:
        msg = "STARTING DATA EXTRACTION"
        log_header(msg)

        data_request = []
        page_data = self._total_pages()
        pages = page_data['page_list']
        total_registres = page_data['total_records']
        report_num = 1

        for num, page in enumerate(pages):
            data_request += self._request_get(endpoint=f'?page={page}&per_page={self.per_page}')

            # visual extraction monitor (only funny)
            if num % 2 == 0:
                logging.info(f"[EXTRACT] | {num / max(pages) * 100:.2f}% [{('=' * int(num / max(pages) * 10 - 1)) + '>' + ' ' * int(10 - num / max(pages) * 10)}]")

            # last one
            if num == max(pages) - 1:
                logging.info('[EXTRACT] --> 100% [==========]')
                logging.info(f'[LOAD] --> SAVING PAGE {num + 1} OF {max(pages)}')
                self._save_file(data_to_save=data_request, file_name=f'PART_{report_num}_AT_')
                logging.info('[LOAD] --> SAVING BreweryApiData COMPLETED INTO BRONZE LAYER')
                break
            # multiple of 1000 registers
            if len(data_request) % 1000 == 0:
                logging.info(f'[LOAD] --> SAVING PAGE {num + 1} OF {max(pages)}')
                self._save_file(data_to_save=data_request, file_name=f'PART_{report_num}_AT_')
                data_request = []
                report_num += 1

        logging.info(f'[EXTRACT] --> EXTRACTION COMPLETE. {total_registres} BREWERIES IN {max(pages)} PAGES')
