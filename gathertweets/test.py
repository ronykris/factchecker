from utility import cleanup, getEmbeddings, performSRL

#txt = "Today, @POTUS, @AlboMP, and @RishiSunak announced steps to carry forward the Australia \u2013 U.K. \u2013 U.S. Partnership.\n\nDeveloping Australia\u2019s conventionally-armed, nuclear-powered submarine capacity and our own will enhance stability in the Indo-Pacific. https://t.co/nZzWt5SbQq"
#cleanup(txt)
#srl = performSRL(txt)
srl = {'entities': [{'name': '@POTUS', 'type': 'person'}, {'name': '@AlboMP', 'type': 'person'}, {'name': '@RishiSunak', 'type': 'person'}], 'relation': ['announced steps to carry forward the Australia – U.K. – U.S. Partnership', 'Developing Australia’s conventionally-armed, nuclear-powered submarine capacity and our own will enhance stability in the Indo-Pacific.'], 'subject': '@POTUS'}

names = list(map(lambda entity: entity['name'], filter(lambda entity: entity['type'] == 'person' or entity['type'] == 'location' or entity['type'] == 'organisation', srl['entities'])))

subject = srl['subject']

relation = srl['relation']

names_vec = []
for name in names:
    names_vec.append(getEmbeddings(name))
#print (len(list(names_vec)))
print (len(names_vec))
print(names_vec)
#print(names)
#print(subject)
#print(relation)



"""
srl = performSRL(data['text'])
        names = list(map(lambda entity: entity['name'], filter(lambda entity: entity['type'] == 'person' or entity['type'] == 'location' or entity['type'] == 'organization', srl['entities'])))
        names_vec = []
        for name in names:
            names_vec.append(getEmbeddings(name))
        data['names_vec'] = names_vec
        data['subject_vec'] = getEmbeddings(srl['subject'])
        relation_vec = [] 
        for relation in srl['relation']:
            relation_vec.append(getEmbeddings(relation))
        data['relation_vec'] = relation_vec
"""
