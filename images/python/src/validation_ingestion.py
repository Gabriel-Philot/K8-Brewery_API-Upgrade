from resources.validation.sample_validation import IngestionValidation
import json
def raw_files_validation():
    var_branch_validation=IngestionValidation().validation_execute()
    result = {"return_value": var_branch_validation}
    with open("/airflow/xcom/return.json", "w") as f:
        json.dump(result, f)

if __name__ == "__main__":
    raw_files_validation()