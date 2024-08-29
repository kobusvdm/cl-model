import chainladder as cl
import pandas as pd

# Load data
clrd = cl.load_sample("clrd").groupby("LOB").sum()
X = clrd.loc["medmal", "CumPaidLoss"]
sample_weight = clrd.loc["medmal", "EarnedPremDIR"].latest_diagonal

# Specify Model
grid = cl.GridSearch(
    estimator=cl.Pipeline(
        steps=[
            ("dev", cl.Development()),
            ("tail", cl.TailCurve()),
            ("model", cl.Benktander()),
        ]
    ),
    param_grid=dict(
        model__n_iters=list(range(1, 100, 2)), 
        model__apriori=[0.50, 0.75, 1.00]
    ),
    scoring={
        "IBNR": lambda x: x.named_steps.model.ibnr_.sum()
    },
    n_jobs=-1,
)

# Fit Model
grid.fit(X, sample_weight=sample_weight)

# Analyze results
output = grid.results_.pivot(
    index="model__n_iters", columns="model__apriori", values="IBNR"
)
print(output.head())
