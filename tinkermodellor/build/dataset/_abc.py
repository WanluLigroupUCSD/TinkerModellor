from abc import ABCMeta, abstractmethod
from typing import Any

class FroceFieldTrans(metaclass=ABCMeta):
    
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
        
    def _transform_to_tinker(self, atom_type : str, trans_dict : dict) -> str:
        pass
