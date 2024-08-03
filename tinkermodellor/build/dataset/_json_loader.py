import json

class JsonLoader:
    def __init__(self):
        return None

    def load_json(self,ForceField):
        
        self.ForceField = ForceField
        if self.ForceField == 1:    self.path = 'tinkermodellor/build/dataset/amoebabio18/amoebabio18.json'
        elif self.ForceField == 2:  self.path = 'tinkermodellor/build/dataset/amoebabio09/amoebabio09.json'
        elif self.ForceField == 3:  self.path = 'tinkermodellor/build/dataset/amoebabio13/amoebabio13.json'
        else: 
            print("Orinated ForceField File :"+ForceField)
            self.path = ForceField
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
        
        container = dict()
        for groups in [RNA_groups,DNA_groups,DNA_terminal_groups,RNA_terminal_groups]:
            for group in groups:
                result = ForceField.get(group,False)
                if result:
                    container[groups[group]] = result
                else:    
                    print("Group {} not found".format(group))

        return container

    def _format_ForceFiled(self,ForceField:dict[str:dict[str:int]]):
        temp_ForceField = dict.fromkeys(ForceField)
        #print(temp_ForceField)
        for group in ForceField:
            temp_ForceField[group] = {}
            for atom in ForceField[group]:
                temp_ForceField[group][atom.replace("*","'")] = ForceField[group][atom]
                if atom == "H5":
                    temp_ForceField[group]["H5'1"] = ForceField[group]["H5"]
                    temp_ForceField[group]["H5'2"] = ForceField[group]["H5"]

                elif atom == "OP":
                    temp_ForceField[group]["O1P"] = ForceField[group]["OP"]
                    temp_ForceField[group]["O2P"] = ForceField[group]["OP"]
  
        
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
        
if __name__ == "__main__":
    Force = JsonLoader()
    print(Force.load_json(1))