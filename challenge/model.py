import pandas as pd
from datetime import datetime
import numpy as np

from sklearn.linear_model import LogisticRegression

from typing import Tuple, Union, List
import joblib

top_10_features = [
    "OPERA_Latin American Wings", 
    "MES_7",
    "MES_10",
    "OPERA_Grupo LATAM",
    "MES_12",
    "TIPOVUELO_I",
    "MES_4",
    "MES_11",
    "OPERA_Sky Airline",
    "OPERA_Copa Air"
]

class DelayModel:

    def __init__(
        self
    ):
        self._model = None # Model should be saved in this attribute.
        
    def get_min_diff(self, data):
        fecha_o = datetime.strptime(data['Fecha-O'], '%Y-%m-%d %H:%M:%S')
        fecha_i = datetime.strptime(data['Fecha-I'], '%Y-%m-%d %H:%M:%S')
        min_diff = ((fecha_o - fecha_i).total_seconds())/60
        return min_diff
    

    def preprocess(
        self,
        data: pd.DataFrame,
        target_column: str = None
    ) -> Union[Tuple[pd.DataFrame, pd.DataFrame], pd.DataFrame]:
        """
        Prepare raw data for training or predict.

        Args:
            data (pd.DataFrame): raw data.
            target_column (str, optional): if set, the target is returned.

        Returns:
            Tuple[pd.DataFrame, pd.DataFrame]: features and target.
            or
            pd.DataFrame: features.
        """
        threshold_in_minutes = 15
        data['min_diff'] = data.apply(self.get_min_diff, axis = 1)
        data['delay'] = np.where(data['min_diff'] > threshold_in_minutes, 1, 0)


        features = pd.concat([
            pd.get_dummies(data['OPERA'], prefix = 'OPERA'),
            pd.get_dummies(data['TIPOVUELO'], prefix = 'TIPOVUELO'), 
            pd.get_dummies(data['MES'], prefix = 'MES')], 
            axis = 1
        )
        features = features[top_10_features]

        if target_column:
            target = pd.DataFrame(data[target_column])
            return (features, target)
        else:
            return features

    def fit(
        self,
        features: pd.DataFrame,
        target: pd.DataFrame
    ) -> None:
        """
        Fit model with preprocessed data.

        Args:
            features (pd.DataFrame): preprocessed data.
            target (pd.DataFrame): target.
        """
        
        # Data balance
        n_y0 = len(target[target['delay'] == 0])
        n_y1 = len(target[target['delay'] == 1])

        self._model = LogisticRegression(class_weight={1: n_y0/len(target), 0: n_y1/len(target)})
        # pd.DataFrame -> 1d array to avoid the warning
        self._model.fit(features, target.values.ravel())
        joblib.dump(self._model, 'model.sav')

        return None

    def predict(
        self,
        features: pd.DataFrame
    ) -> List[int]:
        """
        Predict delays for new flights.

        Args:
            features (pd.DataFrame): preprocessed data.
        
        Returns:
            (List[int]): predicted targets.
        """
        self._model = joblib.load('model.sav')
        y_hat = self._model.predict(features) # numpy array

        return y_hat.tolist() # list of ints