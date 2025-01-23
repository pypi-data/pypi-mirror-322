import os
import pandas as pd
import numpy
import matplotlib
import sklearn

def welcome():
        '''Get a welcome message to ensure package is working properly.
        
        Returns
        -------
        str
            A welcome string.
        '''
        return 'Welcome to UConn Data Science Club!'

class Courses():
    pass

class Datasets():
    
    def __init__(self, dataset):
        self.dataset = dataset.lower() #str

        self.available_datasets = {
            'boston': 'housing.csv'
        }

        if self.dataset not in self.available_datasets:
            raise ValueError(
                f"Dataset '{self.dataset}' is not available. "
                f"Choose from {list(self.available_datasets.keys())}."
            )
        
        self.data_assignment()

    def data_assignment(self) -> pd.DataFrame:
        dataset_path = os.path.join(os.path.dirname(__file__), 'datasets', self.available_datasets[self.dataset])
        return pd.read_csv(dataset_path)
    
class Info():

    def __init__(self):
        self.uconntact = 'https://uconntact.uconn.edu/organization/datascience'
        self.instagram = '@uconndatascience'
        self.email = 'uconndatascience@gmail.com'
        self.discord = 'https://discord.gg/zTTYvVAa'

    def schedule(year: int=2025, semester: str='spring') -> dict:
        '''
        Get the schedule for the specified year and semester.

        Parameters
        ----------
        year : int, optional
            The academic year. Must be one of {2024, 2025}. Default is 2025 (current year).
        semester : str, optional
            The academic semester. Must be one of {'spring', 'fall'}. Default is 'spring'.

        Returns
        -------
        dict
            A dictionary representing the schedule for the given year and semester.
        '''
        # implementation
        print('Coming soon!')
        pass

class OnlineResources():
    pass


