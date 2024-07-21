from._water_ions_trans import WaterAndIonsForceField

class AMOEBABIO09ForceFieldDict:

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
        'ILE': {**_commonpara, **{"CB":25,"HB":26,"HB2":26,"CG1":27,"HG1":28,"HG11":28,"HG12":28,"HG12":28,"HG13":28,"HG21":28,"HG22":28,"HG23":28,"CG2":29,"HG2":30,"CD":31,'CD1':31,"HD":32,"HD1":32,"HD2":32,"HD3":32,"HD11":32,"HD12":32,"HD13":32,}},
        'SER': {**_commonpara, **{"CB":34,"HB":35,"HB1":35,"HB2":35,"OG":36,"HG":37,'HB2':35,'HB3':35}},
        'THR': {**_commonpara, **{"CB":38,"HB":39,"HB2":39,"OG1":42,"HG1":41,'HG21':41,'HG22':41,'HG23':41,"CG2":40,"HG2":41,}},
        'PRO': {**_commonpara, **{"N":53,"CA":54,"C":55,"O":56,"HA":57,"CB":58,"HB":59,"HB1":59,"HB2":59,"CG":60,"HG":61,"HG1":61,"HG2":61,"HG3":61,"CD":62,"HD":63,"HD1":63,"HD2":63,"HD3":63,}},
        'PHE': {**_commonpara, **{"CB":64,"HB":65,"HB1":65,"HB2":65,"CG":66,"CD":67,"CD1":67,"CD2":67,"HD":68,"HD1":68,"HD2":68,"HD3":68,"CE":69,"CE1":69,"CE2":69,"HE":70,"HE1":70,"HE2":70,"CZ":71,"HZ":72,}},
        'TYR': {**_commonpara, **{"CB":73,"HB":74,"HB1":74,"HB2":74,"CG":75,"CD":76,"CD1":76,"CD2":76,"HD":77,"HD1":77,"HD2":77,"HD3":77,"CE":78,"CE1":78,"CE2":78,"HE":79,"HE1":79,"HE2":79,"CZ":80,"OH":81,"HH":82,}},
        'TYRA': {**_commonpara, **{"CB":83,"HB":84,"HB2":84,"CG":85,"CD":86,"HD":87,"CE":88,"HE":89,"CZ":90,"O-":91,}},
        'TRP': {**_commonpara, **{"CB":92,"HB":93,"HB1":93,"HB2":93,"CG":94,"CD1":95,"HD1":96,"CD2":97,"NE1":98,"HE1":99,"CE2":100,"CE3":101,"HE3":102,"CZ2":103,"HZ2":104,"CZ3":105,"HZ3":106,"CH2":107,"HH2":108,}},
        'ASN': {**_commonpara, **{"CB":150,"HB":151,"HB1":151,"HB2":151,"CG":152,"OD1":153,"ND2":154,"HD2":155,"HD21":155,"HD22":155,}},
        'GLN': {**_commonpara,**{"CB":170,"HB":171,"HB1":171,"HB2":171,"CG":172,"HG":173,"HG1":173,"HG2":173,"HG3":173,"CD":174,"OE1":175,"NE2":176,"HE2":177,"HE21":177,"HE22":177,},},
        'MET': {**_commonpara,**{"CB":178,"HB":179,"HB1":179,"HB2":179,"CG":180,"HG":181,"HG1":181,"HG2":181,"HG3":181,"SD":182,"CE":183,"HE":184,"HE1":184,"HE2":184,"HE3":184,},},
        'LYS': {**_commonpara,**{"CB":185,"HB":186,"HB1":186,'HB2':186,"CG":187,"HG":188,"HG1":188,'HG2':188,'HG3':188,"CD":189,"HD":190,"HD1":190,"HD2":190,"HD3":190,"CE":191,"HE":192,"HE1":192,"HE2":192,"HE3":192,"NZ":193,"HZ1":194,"HZ2":194,"HZ3":194,"HN":194,},},
        'ARG': {**_commonpara,**{"CB": 205,"HB1": 206,"HB2": 206,"CG": 207,"HG1": 208,"HG2": 208,"CD": 209,"HD1": 210,"HD2": 210,"NE": 211,"HE": 212,"CZ": 213,"NH1": 214,"NH2": 214,"HH11": 215,"HH12":215,"HH21": 215,"HH22": 215},},
        }

    #CYS->CYS(HS)-SGH,CYX-> CYS(SS)-SG
    _special = {
        'CYS': {**_commonpara, **{"CB":45,"HB1":46,"HB2":46,"SGH":47,"HG":48,'SG':49}},
        'CYX': {**_commonpara, **{"CB":43,"HB1":44,"HB2":44,"SG":47}},
        'CYSA':{**_commonpara, **{"CA":48,"CB":50,"HB1":51,"HB2":51,"SG":52}},
        'ASP': {**_commonpara, **{"CB":140,"HB1":141,"HB2":141,"CG":142,"OD1":143,"OD2":144}},#OD -> OD1=OD2,HB -> HB1=HB2
        'ASPH': {**_commonpara, **{"CB":144,"HB1":145,"HB2":145,"CG":146,"OD1":147,"OD2":147,"HD2":148}},
        'GLU': {**_commonpara, **{"CB":156,"HB1":157,"HB2":157,"CG":158,"HG1":159,"HG2":159,"CD":160,"OE1":161,"OE2":161}},
        'GLUH': {**_commonpara, **{"CB":162,"HB1":163,"HB2":163,"CG":164,"HG1":162,"HG2":162,"CD":166,"OE1":167,"OE2":168,'HE2':169}},
        'HISH': {**_commonpara, **{"CB":109,"HB1":110,"HB2":110,"CG":111,"ND1":112,"HD1":113,"CD2":114,"HD2":115,"CE1":116,"HE1":117,"NE2":118,"HE2":119}},
        'HISD': {**_commonpara, **{"CB":120,"HB1":121,"HB2":121,"CG":122,"ND1":123,"HD1":124,"CD2":125,"HD2":126,"CE1":127,"HE1":128,"NE2":129}},
        'HISE': {**_commonpara, **{"CB":130,"HB1":131,"HB2":131,"CG":132,"ND1":133,"CD2":134,"HD2":135,"CE1":136,"HE1":137,"NE2":138,"HE2":139}},

        'LYS': {**_commonpara,**{"CB":185,"HB1":186,'HB2':186,"CG":187,"HG1":188,'HG2':188,"CD":189,"HD1":190,"HD2":190,"CE":191,"HE1":192,"HE2":192,"NZ":193,"HZ1":194,"HZ2":194,"HZ3":194},},
        'LYSN': {**_commonpara,**{"CB":195,"HB1":196,'HB2':196,"CG":197,"HG1":198,'HG2':198,"CD":199,"HD1":200,"HD2":200,"CE":201,"HE1":202,"HE2":202,"NZ":203,"HZ1":204,"HZ2":204}},
    }

    _amberpara.update(_special)
    _amberpara.update(WaterAndIonsForceField.ion_para)
    _amberpara.update(WaterAndIonsForceField.water_para)
