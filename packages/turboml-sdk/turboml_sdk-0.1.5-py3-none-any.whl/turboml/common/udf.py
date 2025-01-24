from typing import Any


class ModelMetricAggregateFunction:
    """
    Base class for defining a Model Metric Aggregate Function.
    """

    def __init__(self):
        pass

    def create_state(self) -> Any:
        """
        Create the initial state for the UDAF.

        Returns:
            Any: The initial state.
        """
        raise NotImplementedError(
            "The 'create_state' method must be implemented by subclasses."
        )

    def accumulate(self, state: Any, prediction: float, label: float) -> Any:
        """
        Accumulate input data (prediction and label) into the state.

        Args:
            state (Any): The current state.
            prediction (float): The predicted value.
            label (float): The ground truth label.

        Returns:
            Any: The updated state.
        """
        raise NotImplementedError(
            "The 'accumulate' method must be implemented by subclasses."
        )

    def retract(self, state: Any, prediction: float, label: float) -> Any:
        """
        Retract input data from the state (optional).

        Args:
            state (Any): The current state.
            prediction (float): The predicted value.
            label (float): The ground truth label.

        Returns:
            Any: The updated state.
        """
        raise NotImplementedError(
            "The 'retract' method must be implemented by subclasses."
        )

    def merge_states(self, state1: Any, state2: Any) -> Any:
        """
        Merge two states into one.

        Args:
            state1 (Any): The first state.
            state2 (Any): The second state.

        Returns:
            Any: The merged state.
        """
        raise NotImplementedError(
            "The 'merge_states' method must be implemented by subclasses."
        )

    def finish(self, state: Any) -> float:
        """
        Finalize the aggregation and compute the result.

        Args:
            state (Any): The final state.

        Returns:
            float: The result of the aggregation.
        """
        raise NotImplementedError(
            "The 'finish' method must be implemented by subclasses."
        )
