import json
import logging
from collections import Counter
import boto3
from resources.brew_api.brewapi_bronze import BreweryRequestsApi
from resources.utils.utils import log_header, load_config


class IngestionValidation:
    config = load_config()
    _bronze_path_file = config["storages"]["brew_paths"]["bronze"]
    _minio_endpoint_url = config["minio_dev"]["endpoint_url"]
    _minio_access_key = config["minio_dev"]["access_key"]
    _minio_secret_key = config["minio_dev"]["secret_key"]
    _storage_brew_bucket = config["storages"]["brew_bucket"]
    _minio_key_landing = config["storages"]["brew_paths"]["bronze"]

    # Definição do esquema esperado para o processo de validação
    _expected_schema = {
        "id": str,
        "name": str,
        "brewery_type": str,
        "address_1": (str, type(None)),
        "address_2": (str, type(None)),
        "address_3": (str, type(None)),
        "city": str,
        "state_province": str,
        "postal_code": str,
        "country": str,
        "longitude": (str, type(None)),
        "latitude": (str, type(None)),
        "phone": (str, type(None)),
        "website_url": (str, type(None)),
        "state": str,
        "street": (str, type(None))
    }

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=self._minio_endpoint_url,
            aws_access_key_id=self._minio_access_key,
            aws_secret_access_key=self._minio_secret_key
        )

    def _list_files_in_bronze(self):
        """Lista todos os arquivos no bucket S3 na pasta bronze."""
        response = self.s3_client.list_objects_v2(
            Bucket=self._storage_brew_bucket,
            Prefix=self._minio_key_landing
        )
        return [content['Key'] for content in response.get('Contents', [])]

    def _read_s3_file(self, key):
        """Lê o conteúdo de um arquivo JSON do S3."""
        response = self.s3_client.get_object(Bucket=self._storage_brew_bucket, Key=key)
        content = response['Body'].read().decode('utf-8')
        return json.loads(content)

    def _validate_files_numbers(self, expected_total_responses: int) -> int:
        total_responses = 0
        responses_per_file = []

        # Variável auxiliar para a branch de qualidade de dados no Airflow
        var_validation_ingestion_1 = 0

        msg = "INICIANDO VALIDAÇÃO DE INGESTÃO DE DADOS [QUANTIDADE & TIPO]"
        log_header(msg)

        logging.info('[VALIDAÇÃO] -> INICIANDO VALIDAÇÃO DE QUANTIDADE')

        files = self._list_files_in_bronze()
        for key in files:
            data = self._read_s3_file(key)
            responses_per_file.append(len(data))
            total_responses += len(data)
        try:
            if total_responses != expected_total_responses:
                var_validation_ingestion_1 = 1
                raise ValueError(f'Esperado {expected_total_responses} respostas, mas obteve {total_responses}')
        except ValueError as e:
            logging.error(f'[VALIDAÇÃO] -> ERRO DE QUANTIDADE: {e}')

        responses_per_file = Counter(responses_per_file)
        responses_per_file = [
            f'{responses_per_file.get(n)} {"ARQUIVO" if responses_per_file.get(n) == 1 else "ARQUIVOS"} COM {n} CERVEJARIAS'
            for n in responses_per_file.keys()
        ]

        logging.info(
            f'[VALIDAÇÃO] -> NÚMERO TOTAL DE ARQUIVOS SALVOS: {len(files)}\n' +
            f"\n".join(responses_per_file) +
            f'\nNÚMERO TOTAL DE CERVEJARIAS: {total_responses}'
        )
        logging.info('[VALIDAÇÃO] -> VALIDAÇÃO DE QUANTIDADE FINALIZADA')
        return var_validation_ingestion_1

    def _validate_files_types(self) -> int:
        logging.info('[VALIDAÇÃO] -> INICIANDO VALIDAÇÃO DE TIPOS')

        # Variável auxiliar para a branch de qualidade de dados no Airflow
        var_validation_ingestion_2 = 0

        files = self._list_files_in_bronze()

        for key in files:
            data = self._read_s3_file(key)

            # Valida a tipagem de cada registro no arquivo
            for idx, record in enumerate(data):
                for field, expected_type in self._expected_schema.items():
                    try:
                        if field not in record:
                            var_validation_ingestion_2 = 1
                            raise ValueError(f'Campo "{field}" ausente no arquivo "{key}", índice de registro {idx}')

                        if not isinstance(record[field], expected_type):
                            var_validation_ingestion_2 = 1
                            raise TypeError(f'Campo "{field}" no arquivo "{key}", índice de registro {idx} esperado tipo {expected_type}, mas obteve {type(record[field])}')
                    except (ValueError, TypeError) as e:
                        logging.error(f'[VALIDAÇÃO] -> ERRO DE TIPO: {e}')

        logging.info('[VALIDAÇÃO] -> VALIDAÇÃO DE TIPOS FINALIZADA')
        msg = '[VALIDAÇÃO] -> VALIDAÇÃO DE ARQUIVOS FINALIZADA'
        log_header(msg)

        return var_validation_ingestion_2

    def validation_execute(self) -> int:
        page_data = BreweryRequestsApi()._total_pages()
        total_records_api = page_data['total_records']
        var_validation_ingestion_1 = self._validate_files_numbers(expected_total_responses=total_records_api)
        var_validation_ingestion_2 = self._validate_files_types()
        
        print(var_validation_ingestion_1 + var_validation_ingestion_2)
        return var_validation_ingestion_1 + var_validation_ingestion_2
