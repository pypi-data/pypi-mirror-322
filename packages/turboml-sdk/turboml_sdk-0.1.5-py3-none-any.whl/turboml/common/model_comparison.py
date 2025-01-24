import turboml as tb
from typing import List


def compare_model_metrics(models: List, metric: str, x_axis_title: str = "Samples"):
    """Generates a plotly plot for Windowed metrics comparison for a list of models

    Args:
        model_names (List): List of models to compare
        metric (str): Metric for evaluation of models, should be chosen from tb.evaluation_metrics()
        x_axis_title (str, optional): X axis title for the plot. Defaults to "Samples".

    Raises:
        Exception: If other metrics are chosen then Execption is raised
    """
    import plotly.graph_objs as go
    import plotly.io as pio

    pio.renderers.default = "iframe"

    model_traces = []
    windowed_metrics = tb.evaluation_metrics()
    if metric in windowed_metrics:
        for model in models:
            # It is assumed that the user registers the metric before comparing the models
            evals = model.get_evaluation(metric_name=metric)
            model_evaluations = [eval.metric for eval in evals]
            index = [eval.index for eval in evals]
            trace = go.Scatter(
                x=index,
                y=model_evaluations,
                mode="lines",
                name=model.model_name,
            )
            model_traces.append(trace)
        layout = go.Layout(
            title=metric,
            xaxis=dict(title=x_axis_title),  # noqa
            yaxis=dict(title="Metric"),  # noqa
        )
        fig = go.Figure(data=model_traces, layout=layout)
        fig.show()
    else:
        raise Exception(
            f"The other Windowed metrics arent supported yet, please choose from {tb.evaluation_metrics()}, if you want to use batch metrics please use tb.compare_batch_metrics"
        )
