from FlowSpec import run
from ModelSpecs.MedmalCplParams import MedmalCplParams

if __name__ == "__main__":
    """Top-level entry point to construct and execute a specific Loss Reserve model, as defined in MedmalCplParams."""
    
    run(params=MedmalCplParams())

