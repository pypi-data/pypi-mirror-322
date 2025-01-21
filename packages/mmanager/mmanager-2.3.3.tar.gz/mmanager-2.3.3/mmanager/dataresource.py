import json
import requests
import datetime


def get_model_data(model_data):

    data = model_data
    registryOption = model_data.get('registryOption', None) 
    if registryOption:
        registryOption = json.dumps(registryOption)
        data.update({"registryOption": registryOption})

    fetchOption = model_data.get('fetchOption', None)
    if fetchOption:
        fetchOption = json.dumps(fetchOption)
        data.update({"fetchOption": fetchOption})
    
    return data

def file_mod(insertionType, field_name, mlflow_file_key, file_path):
    if insertionType == "MLFlow":
        file_mod_dict = {mlflow_file_key:file_path}
    else:
        file = open(file_path, 'rb')
        file_mod_dict = {field_name: file}
    print(file_mod_dict)
    return file_mod_dict

    
def get_files(model_data):
        training_dataset = model_data.get('training_dataset', None)
        pred_dataset = model_data.get('pred_dataset', None)
        actual_dataset = model_data.get('actual_dataset', None)
        test_dataset = model_data.get('test_dataset', None)
        model_image_path = model_data.get('model_image_path', None)
        model_summary_path = model_data.get('model_summary_path', None)
        model_file_path = model_data.get('model_file_path', None)

        files = {}

        # print(model_data.get("is_mlflow_local", True))
        insertionType = model_data.get("datasetinsertionType", None)
        if training_dataset:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="training_dataset", mlflow_file_key="train_file", file_path=training_dataset)
            files.update(file_mod_dict)

        if test_dataset:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="test_dataset", mlflow_file_key="test_file", file_path=test_dataset)
            files.update(file_mod_dict)

        if pred_dataset:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="pred_dataset", mlflow_file_key="pred_file", file_path=pred_dataset)
            files.update(file_mod_dict)

        if actual_dataset:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="actual_dataset", mlflow_file_key="truth_file", file_path=actual_dataset)
            files.update(file_mod_dict)

        if model_image_path:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="model_image_path", mlflow_file_key="model_image_file", file_path=model_image_path)
            files.update(file_mod_dict)

        if model_summary_path:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="model_summary_path", mlflow_file_key="model_summary_file", file_path=model_summary_path)
            files.update(file_mod_dict)

        if model_file_path:
            file_mod_dict = file_mod(insertionType=insertionType, field_name="model_file_path", mlflow_file_key="model_file", file_path=model_file_path)
            files.update(file_mod_dict)

        return files
