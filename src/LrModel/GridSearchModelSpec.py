from typing import Generic, Optional, TypeVar

import chainladder as cl
import pandas as pd

from .GridSearchParams import GridSearchParams

T = TypeVar("T", bound=GridSearchParams)

from pydantic import BaseModel, Field


class GridSearchModelSpec(BaseModel, Generic[T]):
    """Defines proxy methods to the GridSearchParams object for operations at the GridSearch model level."""
    pars: T = Field(description="The GridSearchParams object to proxy through to.")
    
    def __init__(self, pars: T):
        super().__init__(pars=pars)
        self.pars = pars
    
    def load_data(self):
        """Proxy through to the derived GridSearchParams to load the data."""
        return self.pars.load_data()

    def preprocess_data(self, data):
        """Proxy through to the derived GridSearchParams to preprocess the data."""
        return self.pars.preprocess_data(data)

    def sample_weight(self, data):
        """Proxy through to the derived GridSearchParams to select the sample weight."""
        return self.pars.sample_weight(data)

    def specify_model(self):
        """Proxy through to the derived GridSearchParams to construct the model specification."""
        estimator = cl.Pipeline(steps=self.pars.estimator())
        return cl.GridSearch(
            estimator=estimator,
            param_grid=self.pars.param_grid(),
            scoring=self.pars.scoring(),
            n_jobs=self.pars.n_jobs
        )

    def fit(self, model, preprocessed_data, weight):
        """Proxy through to the derived GridSearchParams to fit the model to the data."""
        return self.pars.fit(model, preprocessed_data, weight)

    def analyze(self, fitted_model):
        """Proxy through to the derived GridSearchParams to analyze the fitted model, usually a DataFrame pivot."""
        return self.pars.analyze(fitted_model)
    
