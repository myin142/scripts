import re
import json

values = {}
FILE = 'output/read-excel/result.json'

# with open("phrases.txt", "r") as f:
#     for line in f.readlines():
#         split = line.split(':')
#         code = int(split[0].strip())
#         name = ':'.join(split[1:]).strip()
#         values[code] = name

with open(FILE, "r") as f:
    codeKey = 'phraseid'
    nameKey = 'phrasetext'
    data = json.loads(f.read())
    for item in data:
        code = item[codeKey]
        name = item[nameKey]
        values[code] = name

    
parsed_code = []

replace_map = {
    '\u00b5': 'my',
    '\u00b3': '3',
    '\u00b2': '2',
    '%': 'percentage',
}

with open('output.txt', 'w') as f:
    for code, name in values.items():
        if code in parsed_code: continue

        # without_bracket_content = re.sub('\(.*?\)', '', name).strip(' ')

        replaced = name
        for v in replace_map:
            replaced = re.sub(v, replace_map[v], replaced)

        no_special = re.sub('[^a-zA-Z0-9_ \n]', ' ', replaced)
        normalized = re.sub('[ ]+', '_', no_special.strip(' ').upper())

        #f.write('|' + name + '|' + str(code) + '|\n') # For creating table in Confluence

        # f.write(normalized + '(\"'+normalized+'\", ' + str(code) + ', null),\n') # For creating enum
        f.write(f'{normalized}({str(code)}, null),\n')

        # f.write(prefix + normalized + '=' + name + '\n') # For creating translations with prefix

        parsed_code.append(code)
