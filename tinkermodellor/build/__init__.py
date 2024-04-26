from .system.gmx._gmxsystem import GMXSystem
from .system.tinker._tinkersystem import TinkerSystem
from .system.gmx._gmxmolecule import GMXMolecule
from .system.transformer import Transformer

from .function.merge._merge import MergeTinkerSystem
from .function.delete._delete import DeleteTinkerSystem
from .function.replace._replace import ReplaceTinkerSystem

from .system.tinker._tkmtrajectory import TKMTrajectory


from .function.index_seprator._ndx_seprator import parse_ndx