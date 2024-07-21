from ._water_ions_trans import WaterAndIonsForceField

class AMOEBAPRO13ForceFieldDict:

    _commonpara={
        'H':10,'H1':232,'H2':232,'H3':232,'HA':12,'HD1':24,'HD2':24,'HD3':24,
        'CA':8,'CG1':17,'CG2':17,'C':9,'CTe':233,
        'N':7,'NTe':231,
        'O':11,'OXT':234,'OC1':234,'OC2':234,'OTe':234,
    }

    #new[# CYS and CYX has the same SG , the only difference is that CYX has no H atom
         # two paths to deal with the problem
         # 1: divide residue into CYS and CYX via HG 2: divide atomtype into SG and SGH via HG 
         # we choose the second one , however CYX is also avaliable]
    _amberpara={
        'GLY': {**_commonpara, **{"N": 1,"CA": 2,"C": 3,"H": 4,"O": 5,"HA1": 6,"HA2": 6}},
        'ALA': {**_commonpara, **{"CB": 13,"HB1": 14,"HB2": 14,"HB3": 14}},
        'VAL': {**_commonpara, **{"CB":15,"HB":16,'HB1':16,'HB2':16,"CG":17,"HG":18,'HG11':18,'HG12':18,'HG13':18,'HG21':18,'HG22':18,'HG23':18,},},
        'LEU': {**_commonpara, **{"CB":19,"HB":20,'HB1':20,'HB2':20,"CG":21,"HG":22,"CD":23,"CD1":23,"CD2":23,"HD":24,"HD11":24,"HD12":24,"HD13":24,"HD21":24,"HD22":24,"HD23":24,}},
        'ILE': {**_commonpara, **{"CB":25,"HB":26,"HB2":26,"CG1":27,"HG1":28,"HG11":28,"HG12":28,"HG12":28,"HG13":28,"HG21":30,"HG22":30,"HG23":30,"CG2":29,"HG2":30,"CD":31,"HD":32,"HD1":32,"HD2":32,"HD3":32}},
        'SER': {**_commonpara, **{"CB":33,"HB":34,"HB1":34,"HB2":34,"OG":35,"HG":36}},
        'THR': {**_commonpara, **{"CB":37,"HB":38,"HB2":38,"OG1":39,"HG1":40,'HG21':42,'HG22':42,'HG23':42,"CG2":41,"HG2":42}},
        'PRO': {**_commonpara, **{"N":50,"CA":51,"C":52,"O":53,"HA":54,"CB":55,"HB":56,"HB1":56,"HB2":56,"CG":57,"HG":58,"HG1":58,"HG2":58,"HG3":58,"CD":59,"HD":60,"HD1":60,"HD2":60,"HD3":60,}},
        'PHE': {**_commonpara, **{"CB":61,"HB":62,"HB1":62,"HB2":62,"CG":63,"CD":64,"CD1":64,"CD2":64,"HD1":5,"HD1":65,"HD2":65,"HD3":65,"CE":66,"CE1":66,"CE2":66,"HE":67,"HE1":67,"HE2":67,"CZ":68,"HZ":69,}},
        'TYR': {**_commonpara, **{"CB":70,"HB":71,"HB1":71,"HB2":71,"CG":72,"CD":73,"CD1":73,"CD2":73,"HD":74,"HD1":74,"HD2":74,"HD3":74,"CE":75,"CE1":75,"CE2":75,"HE":76,"HE1":76,"HE2":76,"CZ":77,"OH":78,"HH":79,}},
        'TYRA': {**_commonpara, **{"CB":80,"HB":81,"HB2":81,"CG":82,"CD":83,"HD":84,"CE":85,"HE":86,"CZ":87,"O-":88,}},
        'TRP': {**_commonpara, **{"CB":89,"HB":90,"HB1":90,"HB2":90,"CG":91,"CD1":92,"HD1":93,"CD2":94,"NE1":95,"HE1":96,"CE2":97,"CE3":98,"HE3":99,"CZ2":100,"HZ2":101,"CZ3":102,"HZ3":103,"CH2":104,"HH2":105,}},
        'ASN': {**_commonpara, **{"CB":147,"HB":148,"HB1":148,"HB2":148,"CG":149,"OD1":150,"ND2":151,"HD2":152,"HD21":152,"HD22":152,}},
        'GLN': {**_commonpara,**{"CB":167,"HB":168,"HB1":168,"HB2":168,"CG":169,"HG":170,"HG1":170,"HG2":170,"CD":171,"OE1":172,"NE2":173,"HE2":174,"HE21":174,"HE22":174,},},
        'MET': {**_commonpara,**{"CB":175,"HB":176,"HB1":176,"HB2":176,"CG":177,"HG":178,"HG1":178,"HG2":178,"HG3":178,"SD":179,"CE":180,"HE":181,"HE1":181,"HE2":181,"HE3":181,},},
        'LYS': {**_commonpara,**{"CB":182,"HB":183,"HB1":183,'HB2':183,"CG":184,"HG":185,"HG1":185,'HG2':185,'HG3':185,"CD":186,"HD":187,"HD1":187,"HD2":187,"HD3":187,"CE":188,"HE":189,"HE1":189,"HE2":189,"HE3":189,"NZ":190,"HZ1":191,"HZ2":191,"HZ3":191,"HN":191,},},
        'ARG': {**_commonpara,**{"CB": 202,"HB1": 203,"HB2": 203,"CG": 204,"HG1": 205,"HG2": 205,"CD": 206,"HD1": 207,"HD2": 207,"NE": 208,"HE": 209,"CZ": 210,"NH1": 211,"NH2": 211,"HH11": 212,"HH12":212,"HH21": 212,"HH22": 212},},

        'CYS': {**_commonpara, **{"CB":43,"HB1":44,"HB2":44,"SGH":45,"HG":46,'SG':47}},
        'CYX': {**_commonpara, **{"SG":47}},
        'ASP': {**_commonpara, **{"CB":137,"HB1":138,"HB2":138,"CG":139,"OD1":140,"OD2":140}},
        'ASPH': {**_commonpara, **{"CB":141,"HB1":142,"HB2":142,"CG":143,"OD1":144,"OD2":145,"HD2":146}},
        'GLU': {**_commonpara, **{"CB":153,"HB1":154,"HB2":154,"CG":155,"HG1":156,"HG2":156,"CD":157,"OE1":158,"OE2":158}},
        'GLUH': {**_commonpara, **{"CB":159,"HB1":160,"HB2":160,"CG":161,"HG1":162,"HG2":162,"CD":163,"OE1":164,"OE2":165,'HE2':166}},  
            
            
        'HISH': {**_commonpara, **{"CB":106,"HB1":107,"HB2":107,"CG":108,"ND1":109,"HD1":110,"CD2":111,"HD2":112,"CE1":113,"HE1":114,"NE2":115,"HE2":116}},
        'HISD': {**_commonpara, **{"CB":117,"HB1":118,"HB2":118,"CG":119,"ND1":120,"HD1":121,"CD2":122,"HD2":123,"CE1":124,"HE1":125,"NE2":126}},
        'HISE': {**_commonpara, **{"CB":127,"HB1":128,"HB2":128,"CG":129,"ND1":130,"CD2":131,"HD2":132,"CE1":133,"HE1":134,"NE2":135,"HE2":136}},
        'LYS': {**_commonpara,**{"CB":182,"HB":183,"HB1":183,'HB2':183,"CG":184,"HG":185,"HG1":185,'HG2':185,'HG3':185,"CD":186,"HD":187,"HD1":187,"HD2":187,"HD3":187,"CE":188,"HE":189,"HE1":189,"HE2":189,"HE3":189,"NZ":190,"HZ1":191,"HZ2":191,"HZ3":191,"HN":191,},},
        'LYSN': {**_commonpara,**{"CB":192,"HB1":193,'HB2':193,"CG":194,"HG1":195,'HG2':195,"CD":196,"HD1":197,"HD2":197,"CE":198,"HE1":199,"HE2":199,"NZ":200,"HZ1":201,"HZ2":201}},
    }
    
    _amberpara.update(WaterAndIonsForceField.ion_para)
    _amberpara.update(WaterAndIonsForceField.water_para)
    _Amberpara = _amberpara

