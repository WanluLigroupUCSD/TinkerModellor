from typing import Union
from para_trans.amoebabio18._forcefieldtrans import AmberGAFFTrans 

#temporarily not used 2023.12.06
#temporarily not used 2023.12.06
#temporarily not used 2023.12.06

class TinkerModellorAtom():

    def __init__(self, atomid: Union[str,int],
                 atomtype:str,
                 x:float, 
                 y:float, 
                 z:float, 
                 topology:list = [], 
                 forcefield:str = 'AmberGAFFtoAMOEBABIO18', 
                 Aggressive:bool = False,
                 TinkerAtomType:Union[str,int] = None):
        """TinkerModellorAtom Initialization

        Args:
            atomid (Union[str,int]):    Atom ID
            atomtype (str):             Atom Type
            x (float):                  Atom X Coordinate
            y (float):                  Atom Y Coordinate
            z (float):                  Atom Z Coordinate
            topology (list):            Atom Topology, contains the bonded atom ID
            forcefield (str):           Force Field Name
            Aggressive (bool):          If true, scripts would try to pair more atom types,
                                        and this may results mismatching
            TinkerAtomType 
            (Union[str,int]):           Tinker Atom Type

        Returns:
            None

        """
        if isinstance(atomid, (str, int)):
            self.atomid = atomid
        else :
            raise TypeError('atomid must be str or int')
        
        if isinstance(atomtype, str):
            self.atomtype = atomtype
        else :
            raise TypeError('atomtype must be str')
        
        if isinstance(x, float) & isinstance(y, float) & isinstance(z, float):
            self.x = x
            self.y = y
            self.z = z
        else :
            raise TypeError('x, y, z must be float')

        if isinstance(topology, list):
            self.topology = topology
        else :
            raise TypeError('topology must be list')

        if isinstance(forcefield, str):
            if forcefield == 'AmberGAFFtoAMOEBABIO18':
                self.TransFunc = AmberGAFFTrans(Aggressive)
            else:
                raise ValueError('For now, noly AmberGAFFtoAMOEBABIO18 is implemented')
        else :
            raise TypeError('forcefield must be str')
        
        if isinstance(TinkerAtomType, (str, int)):
            self.TinkerAtomType = TinkerAtomType
        else :
            raise TypeError('TinkerAtomType must be str or int')
        


        def __call__(self):
            self.TinkerAtomType = self.TransFunc(self.atomtype)
