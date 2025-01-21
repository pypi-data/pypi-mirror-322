"""
Class to handle data operations
"""

import warnings
import pickle
import json
from pathlib import Path
from google.cloud import bigquery, bigquery_storage, storage
import pandas as pd

class DataOperations:
    """
    A class for handling data operations with Google Cloud services (BigQuery and Cloud Storage).

    Parameters
    ----------
    project : str
        Google Cloud project ID for initializing clients.
    """

    def __init__(self, project: str):
        self.bq_client = bigquery.Client(project=project)
        self.bq_storage_client = bigquery_storage.BigQueryReadClient()
        self.gcs_client = storage.Client(project=project)

    def get_data_from_bq(
        self,
        table: str,
        where_clause: str = None,
        save_location: str = None
    ) -> pd.DataFrame:
        """
        Returns data from BigQuery as DataFrame.

        Parameters
        ----------
        table: str
            Name of table/view to get data from.
        where_clause: str
            Where clause to filter data (starting with WHERE).
        save_location: str
            Directory path where to save the data. The filename will be automatically generated
            from the table name.

        Returns
        ----------
        pd.DataFrame
            Data from the view/table.
        """
        sql = f"""
         SELECT * FROM `{table}` {where_clause}
        """
        
        results = self.bq_client.query(sql).to_dataframe(
            bqstorage_client=self.bq_storage_client
        )
        
        if save_location:
            table_simple_name = table.split('.')[-1].strip('`')
            save_path = Path(save_location) / f"{table_simple_name}.csv"
            save_path.parent.mkdir(parents=True, exist_ok=True)
            results.to_csv(save_path, index=False)
            
        return results

    def call_procedure_and_get_data_from_bq(
        self,
        procedure_name: str,
        parameters: list = None,
        save_location: str = None
    ) -> pd.DataFrame:
        """
        Calls a stored procedure in BigQuery. If the procedure returns data, it is returned as a DataFrame.

        Parameters
        ----------
        procedure_name: str
            Name of the stored procedure to call.
        parameters: list
            List of parameters to pass to the procedure.
        save_location: str
            Directory path where to save the data. The filename will be automatically generated
            from the procedure name.

        Returns
        ----------
        pd.DataFrame
            Result of the procedure call. Returns None if procedure doesn't output any data.

        Raises
        ----------
        Warning
            If the procedure execution was successful but didn't return any data.
        """
        param_str = ', '.join(parameters) if parameters else ''
        sql = f"""
        CALL `{procedure_name}`({param_str})
        """
        
        query_job = self.bq_client.query(sql)
            
        if query_job.result().total_rows > 0:
            results = query_job.to_dataframe()
            if save_location:
                procedure_simple_name = procedure_name.split('.')[-1]
                save_path = Path(save_location) / f"{procedure_simple_name}.csv"
                save_path.parent.mkdir(parents=True, exist_ok=True)
                results.to_csv(save_path, index=False)
            return results
        warnings.warn(f"Procedure {procedure_name} executed successfully but didn't return any data.")
        return None

    def delete_data_from_bq(
        self,
        table: str,
        where_clause: str
    ) -> None:
        """
        Delete old data from BigQuery table.

        Parameters
        ----------
        table: str
            Name of table/view to delete data from.
        where_clause: str
            Where clause to filter data (starting with WHERE).
        """
        
        sql = f"""
        DELETE FROM `{table}` {where_clause}
        """
        self.bq_client.query(sql).result()

    def write_dataframe_to_bq(
        self,
        df: pd.DataFrame,
        table: str,
        job_config: bigquery.LoadJobConfig
    ) -> None:
        """
        Function to write dataframe to BigQuery table

        Parameters
        ----------
        df: pd.DataFrame
            Dataframe to write
        table: string
            Table in BigQuery to write dataframe
        job_config : bigquery.LoadJobConfig
            Job configuration.
        """
        job = self.bq_client.load_table_from_dataframe(
            df,
            table,
            job_config=job_config
        )
        job.result()

    def read_gcs_file(
        self,
        bucket_name: str,
        destination_blob_name: str,
        file_type: str
    ) -> object:
        """
        Function to read a file from a specific path on Google Cloud Storage.
            
        Parameters
        ----------
        bucket_name: str
            Name of bucket on GCS, where file is written.
        destination_blob_name: str
            Path in bucket to read file.
        file_type: str
            Type of file to read (either 'pickle', 'json' or 'csv').

        Returns
        ----------
        object
            The object read from the file.
        """
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        with blob.open(mode='rb') as file:
            match file_type:
                case 'pickle': return pickle.load(file)
                case 'json': return json.load(file)
                case 'csv': return pd.read_csv(file)
                case _: raise ValueError(f'Unknown file type: {file_type}')

    def save_gcs_file(
        self,
        bucket_name: str,
        destination_blob_name: str,
        content: str,
        content_type: str
    ) -> None:
        """
        Function to save content to a specific path on Google Cloud Storage.
        
        Parameters
        ----------
        bucket_name: str
            Name of the bucket on GCS where the file will be saved.
        destination_blob_name: str
            Path in the bucket to save the file.
        content: str
            The content to be saved.
        content_type: str
            The MIME type of the content (eg. 'text/html' or 'application/json').
        """
        bucket = self.gcs_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_string(content, content_type=content_type)