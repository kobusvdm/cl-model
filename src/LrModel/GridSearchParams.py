from abc import abstractmethod
from collections.abc import Callable
from typing import Any, Dict, List

import chainladder as cl
from pydantic import BaseModel


class GridSearchParams(BaseModel):
    """Defines the abstract base parameters for a GridSearch model at the lowest configuration level."""
    n_jobs: int = -1
    
    @abstractmethod
    def load_data(self) -> cl.core.triangle.Triangle:
        """Abstract method to define data loading in a derived class."""
        pass
    
    @abstractmethod
    def preprocess_data(self, data: cl.core.triangle.Triangle) -> cl.core.triangle.Triangle:
        """Abstract method to define data preprocessing in a derived class."""
        pass
    
    @abstractmethod
    def sample_weight(self, data: cl.core.triangle.Triangle) -> cl.core.triangle.Triangle:
        """Abstract method to define sample weight selection in a derived class."""
        pass
    
    @abstractmethod
    def estimator(self) -> List[Any]:
        """Abstract method to define the estimator pipeline in a derived class."""
        pass
    
    @abstractmethod
    def param_grid(self) -> Dict[str, List]:
        """Abstract method to define the hyperparameter grid in a derived class."""
        pass
    
    @abstractmethod
    def scoring(self) -> Dict[str, Callable[[cl.GridSearch], cl.GridSearch]]:
        """Abstract method to define the scoring function in a derived class."""
        pass
    
    @abstractmethod
    def fit(self, model: cl.GridSearch, preprocessed_data: cl.core.triangle.Triangle, weight: cl.core.triangle.Triangle) -> cl.GridSearch:
        """Abstract method to define model fitting in a derived class."""
        pass
    
    @abstractmethod
    def analyze(self, fitted_model: cl.GridSearch) -> cl.GridSearch:
        """Abstract method to define model analysis in a derived class, usually a DataFrame pivot."""
        pass
    
    
