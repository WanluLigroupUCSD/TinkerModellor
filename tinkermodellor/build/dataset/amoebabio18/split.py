import json
with open('./amoebabio18.prm') as file:
    file_content = [list(filter(None,line.strip().split('  ')))[2:] for line in file.readlines() if line.startswith('biotype')]
    #print(file_content[:5])
    #[['N', '"Glycine"', '1'],
    #  ['CA', '"Glycine"', '2'],
    #  ['C', '"Glycine"', '3'],
    #  ['HN', '"Glycine"', '4'],
    #  ['O', '"Glycine"', '5']]
    TYPE_DICT = {}
    old_AA = eval(file_content[0][1])
    temp_container = []
    for line in file_content:
        new_AA = eval(line[1])
        if new_AA !=old_AA : 
            TYPE_DICT[old_AA] = {line[0]:int(line[2]) for line in temp_container}
            temp_container = []
        else:pass
        temp_container.append(line)
        old_AA = new_AA
with open('amoebabio18.json','wt') as f:
    json.dump(TYPE_DICT,f)
    
        
        





