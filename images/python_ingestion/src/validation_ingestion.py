from resources.validation.sample_validation import IngestionValidation
import json
def raw_files_validation():
    # Executa a validação e obtém o valor de retorno
    var_branch_validation = IngestionValidation().validation_execute()
    
    # Cria o dicionário com o valor de retorno para o XCom
    result = {"return_value": var_branch_validation}
    
    # Escreve o resultado no arquivo JSON que o Airflow espera para XCom
    with open("/airflow/xcom/return.json", "w") as f:
        json.dump(result, f)

if __name__ == "__main__":
    raw_files_validation()