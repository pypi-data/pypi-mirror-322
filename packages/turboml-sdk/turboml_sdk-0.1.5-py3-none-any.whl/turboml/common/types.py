from __future__ import annotations
from abc import abstractmethod
from typing import NewType, TYPE_CHECKING

if TYPE_CHECKING:
    import turboml.common.pytypes as pytypes

GGUFModelId = NewType("GGUFModelId", str)


class PythonModel:
    @abstractmethod
    def init_imports(self):
        """
        Must import all libraries/modules needed in learn_one and predict_one
        """
        pass

    @abstractmethod
    def learn_one(self, input: pytypes.InputData) -> None:
        pass

    @abstractmethod
    def predict_one(self, input: pytypes.InputData, output: pytypes.OutputData) -> None:
        pass
