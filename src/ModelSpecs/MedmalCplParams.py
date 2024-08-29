from typing import Any, Callable, Dict, List, Tuple

import chainladder as cl

from LrModel.GridSearchParams import GridSearchParams


class MedmalCplParams(GridSearchParams):
    """This module defines a specific set of parameters for a Benktander with GridSearch model on the medmal data in the clrd sample dataset."""
    
    # This class just provides parameters to be used by a construction harness defined in the MedmalCplFlow and FlowSpec classes.
    
    def load_data(self) -> cl.core.triangle.Triangle:
        """Load the clrd sample dataset and aggregate sum by LOB."""
        clrd = cl.load_sample("clrd").groupby("LOB").sum()
        return clrd

    def preprocess_data(self, data: cl.core.triangle.Triangle) -> cl.core.triangle.Triangle:
        """Preprocess the data by selecting the medmal CumPaidLoss triangle."""
        return data.loc["medmal", "CumPaidLoss"]

    def sample_weight(self, data: cl.core.triangle.Triangle) -> cl.core.triangle.Triangle:
        """Select the latest diagonal of the EarnedPremDIR triangle as the sample weight."""
        return data.loc["medmal", "EarnedPremDIR"].latest_diagonal

    def estimator(self) -> List[Any]:
        """Defines a standard dev -> tail_curve -> benktander estimator pipeline."""
        return [
            ("dev", cl.Development()),
            ("tail", cl.TailCurve()),
            ("model", cl.Benktander())
        ]

    def param_grid(self) -> Dict[str, List]:
        """Defines a grid of n_iters and apriori hyperparameter values to search over in the GridSearch."""
        return dict(
            model__n_iters=list(range(1, 100, 2)),
            model__apriori=[0.50, 0.75, 1.00]
        )

    def scoring(self) -> Dict[str, Callable[[cl.GridSearch], cl.GridSearch]]:
        """Score the cadidate models constructed by the GridSearch by summing the IBNR values."""
        return {
            "IBNR": lambda x: x.named_steps.model.ibnr_.sum()
        }

    def fit(self, model: cl.GridSearch, preprocessed_data: cl.core.triangle.Triangle, weight: cl.core.triangle.Triangle) -> cl.GridSearch:
        """Fit the model to the preprocessed data with the given sample weight."""
        return model.fit(preprocessed_data, sample_weight=weight)
    
    def analyze(self, fitted_model: cl.GridSearch) -> cl.GridSearch:
        return fitted_model.results_.pivot(
            index="model__n_iters", 
            columns="model__apriori", 
            values="IBNR"
    )

