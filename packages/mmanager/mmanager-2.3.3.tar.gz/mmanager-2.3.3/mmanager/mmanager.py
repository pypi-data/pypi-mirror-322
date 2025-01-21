import os
import json
import requests
import traceback
import sys
from .dataresource import *
from .serverequest import *
from .log_keeper import *
from colorama import Fore
from IPython.display import HTML, IFrame

class ModelManager:
    def  __init__(self, secret_key, base_url):
        self.base_url = base_url
        self.project_data = {}
        self.secret_key = secret_key
    
    def _get_headers(self, **kwargs):
        '''Returns headers for request
        '''
        headers = {'Authorization': 'secret-key {0}'.format(self.secret_key)}

        return headers
    
    def _logger(self, resp=None, task=None, exception_msg=None):
        if exception_msg:
            logger.error(f"{Fore.RED}Error message: {exception_msg}")
        else:
            if resp.status_code == 201:
                logger.info(f"{task} succeed with status code %s" % resp.status_code)
            elif resp.status_code == 200:
                logger.info(f"{task} succeed with status code %s" % resp.status_code)
            elif resp.status_code == 204:
                logger.info(f"{task} succeed with status code %s" % resp.status_code)
            else:
                logger.error(f"{task} failed with status code %s" % resp.status_code)
                if resp.json():
                    if resp.json().get("name", None):
                        logger.error(f"{Fore.RED}Error message: {resp.json().get('name')[0]}")
                    elif resp.json().get("detail", None):
                        logger.error(f"{Fore.RED}Error message: {resp.json().get('detail')}")
                    else:
                        logger.error(f"{Fore.RED}Error message: {next(iter(resp.json().values()))}")
            
    
class ReleaseTable(ModelManager):
    def post(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/releaseTable/" % (self.base_url)
    
        try:
            release_table = requests.patch(url, data=data, headers=kwargs['headers'])
            self._logger(resp=release_table, task="Post Release Table")
        except Exception as e:
            self._logger(exception_msg=str(e))
            release_table = e
        return release_table

class Usecase(ModelManager):
  
    def post_usecase(self, usecase_info, forecasting_fields={}, forecasting_feature_tabs={}):
        '''Post Usecase
        '''
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/projects/" % self.base_url
        
        image_p = usecase_info.get('image', None)
        banner_p = usecase_info.get('banner', None)

        try:
            #for images
            files = {}
            if image_p:
                files.update({"image":open(image_p, 'rb')})  
            if banner_p:
                files.update({"banner":open(banner_p, 'rb')})      
            #for usecase_info
            data= {}
            files_key_list = ['image', 'banner']
            for key in files_key_list:
                usecase_info.pop(key, None)

            # Add all the usecase data into one
            data.update(usecase_info)

            # For Forecasting
            if usecase_info.get("usecase_type", None)=="Forecasting":
                data.update(forecasting_fields)
                # data.update(forecasting_tables_fields)
                data.update(forecasting_feature_tabs)
        
            usecase = requests.post(url, data=data, files=files, headers=kwargs['headers'])
            self._logger(resp=usecase, task="Post usecase")
        except Exception as e:
            self._logger(exception_msg=str(e))
            usecase = e
            
        return usecase

    def patch_usecase(self, usecase_data, usecase_id):
        '''Update Usecase
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/projects/%s/" % (self.base_url, usecase_id)

        #for images
        image_p = usecase_data.get('image', None)
        banner_p = usecase_data.get('banner', None)

        files = {}
        try:
            if image_p:
                files.update({"image":open(image_p, 'rb')})
            if banner_p:
                files.update({"image":open(banner_p, 'rb')})
                
            
            #for usecase_data
            data = usecase_data

            usecase = requests.patch(url,
                    data=data, files=files, headers=kwargs['headers'])
            self._logger(resp=usecase, task="Update usecase")
        except Exception as e:
            self._logger(exception_msg=str(e))
            usecase = e

        return usecase

    def delete_usecase(self, usecase_id):
        '''Delete Usecase
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/projects/%s/" % (self.base_url, usecase_id)
        
        try:
            usecase = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=usecase, task="Delete usecase")
        except Exception as e:
            self._logger(exception_msg=str(e))
            usecase = e
            
        return usecase

    def get_usecases(self):

        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/get_usecases/" % self.base_url
        try:
            usecases = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=usecases, task="Get usecase")
        except Exception as e:
            self._logger(exception_msg=str(e))
            usecases = e
        return usecases
    
    def get_detail(self, usecase_id):

        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/%s/" % (self.base_url, usecase_id)
        try:
            usecases = requests.get(url, headers=kwargs['headers'])
        except Exception as e:
            self._logger(exception_msg=str(e))
            usecases = e

        return usecases

    def get_models(self, usecase_id):

        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/getmodels/?usecase_id=%s" % (self.base_url, usecase_id)

        try:
            models = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=models, task="Get Models")
        except Exception as e:
            self._logger(exception_msg=str(e))
            models = e
        return models
    
    def load_cache(self, usecase_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/projects/data_loadcache/?usecase_id=%s" % (self.base_url, usecase_id)
        try:
            usecases_loadcache = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=usecases_loadcache, task="Load Data Cache")
        except Exception as e:
            self._logger(exception_msg=str(e))
            usecases_loadcache = e

        return usecases_loadcache

class Applications(ModelManager):
    
    def post_application(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/applications/" % (self.base_url)

        try:
            application = requests.post(url,
                    data=data, headers=kwargs['headers'])
            self._logger(resp=application, task="Post Application")
        except Exception as e:
            self._logger(exception_msg=str(e))
            application = e

        return application
    
    def delete_application(self, usecase_id):
        '''Delete application
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/applications/%s/" % (self.base_url, usecase_id)
        
        try:
            application = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=application, task="Delete Application")
        except Exception as e:
            self._logger(exception_msg=str(e))
            application = e
            
        return application
    
    def get_applications(self):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/applications/" % (self.base_url)

        try:
            applications = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=applications, task="Get Application")
        except Exception as e:
            self._logger(exception_msg=str(e))
            applications = e
        return applications

class ExternalDatabase(ModelManager):
    def post_related_db(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/related_db/" % (self.base_url)

        try:
            related_db = requests.post(url,
                    data=data, headers=kwargs['headers'])
            self._logger(resp=related_db, task="Post Related Database")
        except Exception as e:
            self._logger(exception_msg=str(e))
            related_db = e
        return related_db
    
    def get_related_db(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/related_db/" % (self.base_url)

        try:
            related_db = requests.get(url,
                    data=data, headers=kwargs['headers'])
            self._logger(resp=related_db, task="Get Related Database")
        except Exception as e:
            self._logger(exception_msg=str(e))
            related_db = e
        return related_db

    def link_externaldb(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/externaldb_link/" % (self.base_url)

        try:
            db_link = requests.post(url,
                    data=data, headers=kwargs['headers'])
            self._logger(resp=db_link, task="Post Database Link")
        except Exception as e:
            self._logger(exception_msg=str(e))
            db_link = e
        return db_link
    
    def get_externaldb_links(self):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/externaldb_link/" % (self.base_url)

        try:
            db_links = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=related_db, task="Get Database Link")
        except Exception as e:
            self._logger(exception_msg=str(e))
            db_links = e
        return db_links

class Model(ModelManager):

    def post_model(self, model_data, ml_options={}, data_distribution=True):
        '''Post Model
        '''
        url = "%s/api/models/" % self.base_url

        kwargs = {
            'headers': self._get_headers()
        }
        
        try:
            #for model_data
            model_data.update(ml_options)
            model_data.update({"data_distribution":data_distribution})
            data = get_model_data(model_data)

            #for model_files
            files = get_files(model_data)      
            model = model_request(url, kwargs, data, ml_options, files)
            self._logger(resp=model, task="Post Model")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model = e
        
        return model
    
    def delete_model(self, model_id):

        '''Delete Model
        '''

        kwargs = {
            'headers': self._get_headers()
        }
        
        url = "%s/api/models/%s/" % (self.base_url, model_id)
        
        try:
            model = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=model, task="Delete Model")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model = e
            
        return model

    def patch_model(self, model_data, model_id, create_sweetviz=True):

        '''Update Model
        '''

        url = "%s/api/models/%s/" % (self.base_url, model_id)

        kwargs = {
            'headers': self._get_headers()
        }

        try:
            #for model_data
            data = model_data
            data.update({"create_sweetviz":create_sweetviz})      

            #for model_files
            files = get_files(model_data)

            model = requests.patch(url, data=data, files=files, headers=kwargs['headers'])
            self._logger(resp=model, task="Update Model")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model = e

        return model

    def generate_report(self, model_id):
        '''Generate Model Report
        '''

        kwargs = {
            'headers': self._get_headers()
        }


        url = "%s/api/govrnreport/%s/generateReport/" % (self.base_url, model_id)

        try:
            model_report = requests.post(url, headers=kwargs['headers'])
            self._logger(resp=model_report, task="Generate Report")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model_report = e

        return model_report

    def get_details(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/models/%s/" % (self.base_url, model_id)
        try:
            model = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=model, task="Get Model Details")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model = e

        return model
    
    def get_latest_metrics(self, model_id, metric_type):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/models/get_latest_metrics/?model_id=%s&&metric_type=%s" % (self.base_url, model_id, metric_type)
        try:
            model_metrics = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=model_metrics, task="Get Latest Model Metrics")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model_metrics = e

        return model_metrics

    def get_all_reports(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/models/get_all_reports/?model_id=%s" % (self.base_url, model_id)
        try:
            model_reports = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=model_reports, task="Get Model Reports")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model_reports = e

        return model_reports
    
    def create_insight(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/insight/create_insight/?model_id=%s" % (self.base_url, model_id)
        try:
            model_insight = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=model_insight, task="Create Insight")
        except Exception as e:
            self._logger(exception_msg=str(e))
            model_insight = e

        return model_insight
    
    def create_causalgraph(self, model_id, target_col, algorithm):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/CausalGraph/%s/create_causalgraph/?target_col=%s&&algorithm=%s" % (self.base_url, model_id, target_col, algorithm)
        try:
            causal_graph = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=causal_graph, task="Create Causal Graph")
        except Exception as e:
            self._logger(exception_msg=str(e))
            causal_graph = e

        return causal_graph
    
    def get_causal_discovery_graphs(self, model_id, graph_type):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/PyCausalD3Graph/%s/get_discovery_graphs/?graph_type=%s" % (self.base_url, model_id, graph_type)
        try:
            causal_discovery = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=causal_discovery, task="Get Causal Discovery")
            causal_discovery_json = causal_discovery.json()
            html_content = causal_discovery_json.get(graph_type)
            return HTML(html_content)
        except Exception as e:
            self._logger(exception_msg=str(e))
            causal_discovery = e
            return causal_discovery
    
    def get_causal_inference_graphs(self, model_id, graph_type, treatment=None, outcome=None):
        kwargs = {
            'headers': self._get_headers()
        }
        if treatment and outcome:
            url = "%s/api/PyCausalInference/%s/create_inference_graphs/?treatment=%s&&outcome=%s" % (self.base_url, model_id, treatment, outcome)
        else:
            url = "%s/api/PyCausalInference/%s/create_inference_graphs/" % (self.base_url, model_id)
        try:
            causal_inference = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=causal_inference, task="Get Causal Inference")
            causal_inference_json = causal_inference.json()
            html_content = causal_inference_json.get(graph_type)
            return HTML(html_content)
        except Exception as e:
            self._logger(exception_msg=str(e))
            causal_inference = e
        return causal_inference
    
    def get_causal_inference_correlation(self, model_id, graph_type, treatment, outcome):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/PyCausalInference-Correlation/%s/create_correlation/?treatment=%s&&outcome=%s" % (self.base_url, model_id, treatment, outcome)
        try:
            causal_inference_corelation = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=causal_inference_corelation, task="Get Causal Inference Corelation")
            causal_inference_corelation_json = causal_inference_corelation.json()
            html_content = causal_inference_corelation_json.get(graph_type)
            if graph_type=="causal_correlation_summary":
                html_content = f"<pre>{html_content}</pre>"
            return HTML(html_content)
        except Exception as e:
            self._logger(exception_msg=str(e))
            causal_inference_corelation = e

        return causal_inference_corelation
    
    def get_wit(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/getFeature/%s/get_wit_url/" % (self.base_url, model_id)
        try:
            model_wit = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=model_wit, task="Get What If Analysis")
            model_wit_json = model_wit.json()
            url = model_wit_json.get('wit_url')
            wit_url = f"{self.base_url}{url}"
            return IFrame(wit_url, width=1500, height=800)
        except Exception as e:
            self._logger(exception_msg=str(e))
            model_wit = e
        return model_wit
    
    def get_netron(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/getFeature/%s/get_netron_url/" % (self.base_url, model_id)
        try:
            netron = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=netron, task="Get Netron")
            netron_json = netron.json()
            url = netron_json.get('netron_url')
            netron_url = f"{self.base_url}{url}"
            return IFrame(netron_url, width=1500, height=800)
        except Exception as e:
            self._logger(exception_msg=str(e))
            netron = e
        return netron

    def get_data_distribution(self, model_id):
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/getFeature/%s/get_data_distribution_url/" % (self.base_url, model_id)
        try:
            data_distribution = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=data_distribution, task="Get Data Distribution")
            data_distribution_json = data_distribution.json()
            url = data_distribution_json.get('data_distribution_url')
            data_distribution_url = f"{self.base_url}{url}"
            return IFrame(data_distribution_url, width=1500, height=800)
        except Exception as e:
            self._logger(exception_msg=str(e))
            data_distribution = e
        return data_distribution

class TableInfo(ModelManager):
    def post_table_info(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/table_info/" % (self.base_url)
    
        try:
            table_info = requests.post(url, data=data, headers=kwargs['headers'])
            self._logger(resp=table_info, task="Post Table Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            table_info = e
        return table_info
    
    def delete_table_info(self, table_id):
        '''Delete table_info
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/table_info/%s/" % (self.base_url, table_id)
        
        try:
            table_info = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=table_info, task="Table Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            table_info = e
            
        return table_info
    
    def get_table_info(self, table_id):
        '''get table_info
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/table_info/%s/" % (self.base_url, table_id)
        
        try:
            table_info = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=table_info, task="Get Table Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            table_info = e
            
        return table_info
    
class FieldInfo(ModelManager):
    def post_field_info(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/field_info/" % (self.base_url)
    
        try:
            field_info = requests.post(url, data=data, headers=kwargs['headers'])
            self._logger(resp=field_info, task="Post Field Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            field_info = e
        return field_info
    
    def delete_field_info(self, field_id):
        '''Delete field_info
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/field_info/%s/" % (self.base_url, field_id)
        
        try:
            field_info = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=field_info, task="Field Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            field_info = e
            
        return field_info
    
    def get_field_info(self, field_id):
        '''get field_info
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/field_info/%s/" % (self.base_url, field_id)
        
        try:
            field_info = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=field_info, task="Get Field Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            field_info = e
            
        return field_info
    
class LLMCreds(ModelManager):
    def post(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/llmCreds/" % (self.base_url)
    
        try:
            llm_creds = requests.post(url, data=data, headers=kwargs['headers'])
            self._logger(resp=llm_creds, task="Post LLM Creds")
        except Exception as e:
            self._logger(exception_msg=str(e))
            llm_creds = e
        return llm_creds
    
    def delete_llm_creds(self, llmCreds_id):
        '''Delete llm_creds
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/llmCreds/%s/" % (self.base_url, llmCreds_id)
        
        try:
            llm_creds = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=llm_creds, task="LLM Credentials")
        except Exception as e:
            self._logger(exception_msg=str(e))
            llm_creds = e
            
        return llm_creds
    
    def get_llm_creds(self, llmCreds_id):
        '''get llm_creds
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/llmCreds_id/%s/" % (self.base_url, llmCreds_id)
        
        try:
            llm_creds = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=llm_creds, task="Get LLM Credentials Info")
        except Exception as e:
            self._logger(exception_msg=str(e))
            llm_creds = e
            
        return llm_creds

class RelatedDatabase(ModelManager):
    def post_related_db(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/related_db/" % (self.base_url)
    
        try:
            related_db = requests.post(url, data=data, headers=kwargs['headers'])
            self._logger(resp=related_db, task="Post Related Database")
        except Exception as e:
            self._logger(exception_msg=str(e))
            related_db = e
        return related_db

    def delete_related_db(self, related_db_id):
        '''Delete related_db
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/related_db/%s/" % (self.base_url, related_db_id)
        
        try:
            related_db = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=related_db, task="Related Database")
        except Exception as e:
            self._logger(exception_msg=str(e))
            related_db = e
            
        return related_db
    
    def get_related_db(self, related_db_id):
        '''get related_db
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/related_db/%s/" % (self.base_url, related_db_id)
        
        try:
            related_db = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=related_db, task="Get Related Database")
        except Exception as e:
            self._logger(exception_msg=str(e))
            related_db = e
            
        return related_db        

class DatabaseLink(ModelManager):
    def post_db_link(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/externaldb_link/" % (self.base_url)
    
        try:
            db_link = requests.post(url, data=data, headers=kwargs['headers'])
            self._logger(resp=db_link, task="Post Database Link")
        except Exception as e:
            self._logger(exception_msg=str(e))
            db_link = e
        return db_link
    
    def delete_db_link(self, db_link_id):
        '''Delete externaldb_link
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/externaldb_link/%s/" % (self.base_url, db_link_id)
        
        try:
            db_link = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=db_link, task="Delete Database Link")
        except Exception as e:
            self._logger(exception_msg=str(e))
            db_link = e
            
        return db_link
    
    def get_externaldb_link(self, db_link_id):
        '''get externaldb_link
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/externaldb_link/%s/" % (self.base_url, db_link_id)
        
        try:
            db_link = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=db_link, task="Get Database Link")
        except Exception as e:
            self._logger(exception_msg=str(e))
            db_link = e
            
        return db_link  

class MLFlow(ModelManager):
    def post_mlflow_creds(self, data):
        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/mlflow_creds/" % (self.base_url)
    
        try:
            mlflow_creds = requests.post(url, data=data, headers=kwargs['headers'])
            self._logger(resp=mlflow_creds, task="Post MLFlow Creds")
        except Exception as e:
            self._logger(exception_msg=str(e))
            mlflow_creds = e
        return mlflow_creds
    
    def delete_mlflow_creds(self, mlflow_creds_id):
        '''Delete mlflow_creds
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/mlflow_creds/%s/" % (self.base_url, mlflow_creds_id)
        
        try:
            mlflow_creds = requests.delete(url, headers=kwargs['headers'])
            self._logger(resp=mlflow_creds, task="Deleted MLFlow Creds")
        except Exception as e:
            self._logger(exception_msg=str(e))
            mlflow_creds = e
            
        return mlflow_creds
    
    def get_mlflow_creds(self, mlflow_creds_id):
        '''get mlflow_creds
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = "%s/api/mlflow_creds/%s/" % (self.base_url, mlflow_creds_id)
        
        try:
            mlflow_creds = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=mlflow_creds, task="Get MLFlow Creds")
        except Exception as e:
            self._logger(exception_msg=str(e))
            mlflow_creds = e
            
        return mlflow_creds

    def download_dataset_model(self, mlflow_cred_id, exp_name, run_id='', artifact_path=''):

        '''Download Datasets and Model From MLFLow
        '''

        kwargs = {
            'headers': self._get_headers()
        }
       
        url = f"{self.base_url}/api/ml_flow/get_tmp_dataset_model_path/?exp_name={exp_name}&&mlflow_id={mlflow_cred_id}&&run_id={run_id}&&artifact_path={artifact_path}"

        try:
            mlflow_creds = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=mlflow_creds, task="Get MLFlow Creds")
        except Exception as e:
            self._logger(exception_msg=str(e))
            mlflow_creds = e
            
        return mlflow_creds
    
class WhatIf(ModelManager):
    def post_wit_files(self, data):
        '''Post WIT Resources
        '''
        url = "%s/api/wit_files/" % self.base_url

        kwargs = {
            'headers': self._get_headers()
        }
        
        try:
            #for resource file
            file = data.get('file', None)
            files = {}
            if file:
                files.update({"file":open(file, 'rb')})  

            wit_resources = requests.post(url, data=data, files=files, headers=kwargs['headers'])
            self._logger(resp=wit_resources, task="WIT Resources Added")
        except Exception as e:
            self._logger(exception_msg=str(e))
            wit_resources = e
        return wit_resources
    
    def post_img_cls_wit_files(self, data):
        '''Post Image Classification WIT Resources
        '''
        url = "%s/api/wit_files/img_cls/" % self.base_url

        kwargs = {
            'headers': self._get_headers()
        }
        
        try:
            #for resource file
            files = {}
            files_list = ["input_model", "input_zip", "dicom_zipfile", "dicom_labelfile"]
            for key, value in data:
                if key in files_list:
                    file_path = value
                    if file_path:
                        files.update({key:open(file_path, 'rb')})

            wit_resources = requests.post(url, data=data, files=files, headers=kwargs['headers'])
            self._logger(resp=wit_resources, task="WIT Image Classification Resources Added")
        except Exception as e:
            self._logger(exception_msg=str(e))
            wit_resources = e
        return wit_resources

    def build_wit(self, model_id):
        '''Build What If Analysis Tool.
        '''
        kwargs = {
            'headers': self._get_headers()
        }
        url = "%s/api/buildWIT/%s/build_whatif/" % (self.base_url, model_id)
        try:
            wit = requests.get(url, headers=kwargs['headers'])
            self._logger(resp=wit, task="Build What If Analysis Tool")
            return 
        except Exception as e:
            self._logger(exception_msg=str(e))
            wit = e
        return wit