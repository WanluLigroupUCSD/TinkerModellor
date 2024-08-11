import json

class JsonLoader:
    def __init__(self):
        return None

    def load_json(self,ForceField):
        
        self.ForceField = ForceField
        if self.ForceField == 1:    self.path = 'tinkermodellor/build/dataset/amoebabio18/amoebabio18.json'
        elif self.ForceField == 2:  self.path = 'tinkermodellor/build/dataset/amoebabio09/amoebabio09.json'
        elif self.ForceField == 3:  
            self.path = 'tinkermodellor/build/dataset/amoebabio13/amoebapro13.json'
            raise IndexError("3 is refer to amoebapro13 which only has parameters for protein try to use 1-[amoebabio18],2-[amoebabio09] or 4-[amoebanuc17] to slove the problem")
        elif self.ForceField == 4:  self.path = 'tinkermodellor/build/dataset/amoebanuc17/amoebanuc17.json'
        else: 
            print("Orinated ForceField File :"+str(ForceField))
            self.path = self.process_json_from_prm(ForceField)
        with open(self.path,'rt') as f:
            self.ForceFiledDict:dict[str:dict[str,int]] = self._check_ForceFiled(json.load(f))
            self.ForceFiledDict = self._format_ForceFiled(self.ForceFiledDict)
        return self.ForceFiledDict

        
        
    def _check_ForceFiled(self,ForceField:dict[str:dict[str:int]]):

        RNA_groups = {"Adenosine":"A","Guanosine":"G","Cytidine":"C","Uridine":"U","Phosphodiester RNA":"RP"}
        DNA_groups = {"Deoxyadenosine":"DA","Deoxyguanosine":"DG","Deoxycytidine":"DC","Deoxythymidine":"DT","Phosphodiester DNA":"DP"}
        DNA_terminal_groups = {"3'-Monophosphate OS DNA":"D3OS","3'-Monophosphate P DNA":"D3P","3'-Monophosphate OP DNA":"D3OP","3'-Hydroxyl DNA":"D3OH",
                               "5'-Monophosphate OS DNA":"D5OS","5'-Monophosphate P DNA":"D5P","5'-Monophosphate OP DNA":"D5OP","5'-Hydroxyl DNA":"D5OH"}
        RNA_terminal_groups = {"3'-Monophosphate OS RNA":"R3OS","3'-Monophosphate P RNA":"R3P","3'-Monophosphate OP RNA":"R3OP","3'-Hydroxyl RNA":"R3OH",
                               "5'-Monophosphate OS RNA":"R5OS","5'-Monophosphate P RNA":"R5P","5'-Monophosphate OP RNA":"R5OP","5'-Hydroxyl RNA":"R5OH"}
        Water_groups = {"Water":"SOL"}#to support gromacs water model
        
        container = dict()
        for groups in [RNA_groups,DNA_groups,DNA_terminal_groups,RNA_terminal_groups,Water_groups]:
            for group in groups:
                result = ForceField.get(group,False)
                if result:
                    container[groups[group]] = result
                    if group == "Water":
                        #support for water model
                        #specially set for amb17
                        container["WAT"] = result
                        container["HOH"] = result
                else:    
                    print("Group {} not found".format(group))

        return container

    def _format_ForceFiled(self,ForceField:dict[str:dict[str:int]]):
        temp_ForceField = dict.fromkeys(ForceField)
        #print(temp_ForceField)
        for group in ForceField:
            temp_ForceField[group] = {}
            for atom in ForceField[group]:
                #atomtype in gmx format is different from tinker format
                #gmx: O5' -> tinker: O5*
                #gmx: H2' -> tinker: H2*1
                #this function was read from the tinker prm forcefiled,so we need to change the atomtype into gmx format 
                #temp_ForceField was a semi-copy of ForceField ,they have the same keys,but there is no value in temp_ForceField
                #so that we can add the modified value in ForceField into temp_ForceField to acheive the goal of changing the atomtype
                #temp_ForceField[group][atom.replace("*","'")] = ForceField[group][atom]
                
                if atom == "H5*":
                    #it odd that the gmx forcefiled has two H5 atomtype
                    #the left atomtype is in gmx format 
                    temp_ForceField[group]["H5'1"] = ForceField[group]["H5*"]
                    temp_ForceField[group]["H5'2"] = ForceField[group]["H5*"]
                
                if atom == "OP":
                    temp_ForceField[group]["O1P"] = ForceField[group]["OP"]
                    temp_ForceField[group]["O2P"] = ForceField[group]["OP"]

                elif atom == "H2*":
                    temp_ForceField[group]["H2'1"] = ForceField[group]["H2*"]
                    temp_ForceField[group]["H2'2"] = ForceField[group]["H2*"]

                elif atom == "HO*":
                    temp_ForceField[group]["HO'2"] = ForceField[group]["HO*"]

                #DT
                elif atom == "H7":
                    temp_ForceField[group]["H71"] = ForceField[group]["H7"]
                    temp_ForceField[group]["H72"] = ForceField[group]["H7"]
                    temp_ForceField[group]["H73"] = ForceField[group]["H7"]

                #Water
                elif atom == "O" :
                    temp_ForceField[group]["OW"] = ForceField[group]["O"]
                elif atom == "H" :
                    temp_ForceField[group]["HW1"] = ForceField[group]["H"]
                    temp_ForceField[group]["HW2"] = ForceField[group]["H"]
                
                else:
                    temp_ForceField[group][atom.replace("*","'")] = ForceField[group][atom]

        
        #print(ForceField["RP"])    
        #print(temp_ForceField['RP'])        
        ForceField = temp_ForceField
        del temp_ForceField
        #print(ForceField["RP"])
        for group in ['R3OH','D3OH']:
            ForceField[group]["O3'T"] = ForceField[group]["O3'"]
            ForceField[group].pop("O3'")
        for group in ['R5OH','D5OH']:
            ForceField[group]["O5'T"] = ForceField[group]["O5'"]
            ForceField[group].pop("O5'")
        #print(ForceField["RP"])
        ForceField["R3P"] ={**ForceField.pop("R3OS"),**ForceField.pop("R3P"),**ForceField.pop("R3OP")}
        ForceField["D3P"] ={**ForceField.pop("D3OS"),**ForceField.pop("D3P"),**ForceField.pop("D3OP")}
        ForceField["R5P"] ={**ForceField.pop("R5OS"),**ForceField.pop("R5P"),**ForceField.pop("R5OP")}
        ForceField["D5P"] ={**ForceField.pop("D5OS"),**ForceField.pop("D5P"),**ForceField.pop("D5OP")}
        
        #print(ForceField["RP"])
        for group in {"A","G","C","U"} : ForceField[group].update({**ForceField['RP'],**ForceField['R3OH'],**ForceField['R5OH']})
        for group in {"DA","DG","DC","DT"} : ForceField[group].update({**ForceField['DP'],**ForceField['D3OH'],**ForceField['D5OH']})
        for i in ['RP','R3OH','R5OH','DP','D3OH','D5OH'] : ForceField.pop(i)


        return ForceField

    def process_json_from_prm(self,file_path:str,keep:bool = True) -> dict[str:dict[str:int]]:
        if file_path.endswith('.json'):
            return file_path
        elif file_path.endswith('.prm'):
            with open(file_path,'rt') as f:
                dict_sorted_by_residue = {}
                lines = f.readlines()#readlines()读取所有行，返回一个列表
                for line in lines:#遍历列表
                    if line.startswith('biotype'):
                        #判断行是否以biotype开头
                        # biotype     217    NE2     "Histidine (HD)"                  129
                        # biotype     218    N       "Histidine (HE)"                    7
                        # biotype     219    CA      "Histidine (HE)"                    8
                        title,index,atomtype,residue,numberic_type = list(filter(None,line.strip().split('  ')))
                        residue = eval(residue)
                        try:dict_sorted_by_residue[residue].update({atomtype: int(numberic_type)})
                        except:dict_sorted_by_residue[residue] = {atomtype: int(numberic_type)}
                with open(file_path.replace('.prm','.json'),'wt') as f:json.dump(dict_sorted_by_residue,f,indent=4) 
                return file_path.replace('.prm','.json')
        else:
            raise TypeError(f"file type error,support .json or .prm only,{file_path} is not supported")
        
if __name__ == "__main__":
    Force = JsonLoader()
    print(Force.load_json(1)['SOL'])