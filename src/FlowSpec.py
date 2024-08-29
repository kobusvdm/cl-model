
from typing import Generic, Type, TypeVar

from prefect import flow, runtime, task
from prefect.artifacts import (create_link_artifact, create_progress_artifact,
                               update_progress_artifact)
from prefect.logging import get_run_logger

from LrModel.GridSearchModelSpec import GridSearchModelSpec
from LrModel.GridSearchParams import GridSearchParams
from StorageApi import LocalStorageBlob

T = TypeVar("T", bound=GridSearchParams)

    
@task
def configure(model_spec: GridSearchModelSpec[T], params: T):
    """Proxy through to the model_spec and GridSearchParams object to configure the model."""
    logger = get_run_logger()
    logger.info("Configuring model execution pipeline: [%s]", params)
    _params = params

    store = LocalStorageBlob()

    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-params.json", _params.model_dump_json().encode())
    logger.info("Model configuration complete: [%s]", _params)
    return _params

@task
def load_data(model_spec: GridSearchModelSpec[T], params: T):
    """Proxy through to the model_spec and GridSearchParams object to load the data."""
    get_run_logger().info("Loading data")
    _params = params

    data = model_spec.load_data()

    store = LocalStorageBlob()
    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-data-load.json", data.to_json().encode())
    return data

@task
def preprocess_data(model_spec: GridSearchModelSpec[T], data):
    """Proxy through to the model_spec and GridSearchParams object to preprocess the data."""
    get_run_logger().info("Preprocessing data")

    data = model_spec.preprocess_data(data)

    store = LocalStorageBlob()
    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-data-process.json", data.to_json().encode())
    return data

@task
def sample_weight(model_spec: GridSearchModelSpec[T], data):
    """Proxy through to the model_spec and GridSearchParams object to select the sample weight."""
    get_run_logger().info("Selecting sample weight")
    data = model_spec.sample_weight(data)

    store = LocalStorageBlob()

    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-sample-weight.json", data.to_json().encode())
    return data

@task
def specify_model(model_spec: GridSearchModelSpec[T], params: T):
    """Proxy through to the model_spec and GridSearchParams object to construct the model specification."""
    get_run_logger().info("Specifying model")
    _params = params

    model = model_spec.specify_model()

    store = LocalStorageBlob()
    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-model-spec.json", repr(model).encode())
    return model

@task
def fit(model_spec: GridSearchModelSpec[T], params: T, model, preprocessed_data, weight):
    """Proxy through to the model_spec and GridSearchParams object to fit the model to the data."""
    get_run_logger().info("Fitting model")
    _params = params

    f_model = model_spec.fit(model, preprocessed_data, weight)

    store = LocalStorageBlob()
    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-fit.json", repr(f_model).encode())
    return f_model
    
@task
def analyze(model_spec: GridSearchModelSpec[T], params: T, fitted_model):
    """Proxy through to the model_spec and GridSearchParams object to analyze the fitted model, usually a DataFrame pivot."""
    _params = params

    anl = model_spec.analyze(fitted_model)

    store = LocalStorageBlob()
    f_name = runtime.flow_run.name
    store.save(f".temp/{f_name}-analyze.json", anl.to_json().encode())
    return anl

@flow(cache_result_in_memory=True)
def run(params: T):
    """Defined the actual model workflow as a Prefect flow."""
    logger = get_run_logger()
    logger.info("Running model")
    model_spec = GridSearchModelSpec[T](params)
    logger.info("Constructing model: [%s]", model_spec)

    config = configure(model_spec, params)
    data = load_data(model_spec, config)
    preprocessed_data = preprocess_data(model_spec, data)
    weight = sample_weight(model_spec, data)
    model = specify_model(model_spec, params)
    fitted_model = fit(model_spec, params, model, preprocessed_data, weight)

    return analyze(model_spec, params, fitted_model)
