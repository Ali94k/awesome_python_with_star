import requests
import json
from requests.auth import HTTPBasicAuth

def createTable(sectionName, sectionItems):
    table = []
    table.append(sectionName)
    table.append('|Name|Description|Star count|\n')
    table.append('|---|---|---|\n')

    orderedItems = sorted(sectionItems, key=lambda k: k['stargazers_count'], reverse=True)

    for i in orderedItems:
        try:
            name = f'[{i["full_name"]}]({i["html_url"]})'
            description = i["description"] or 'No description'
            description.replace('|', '\\')
            table.append(f'|{name}|{description}|{i["stargazers_count"]}|\n')
        except Exception as ex:
            print(i)
            print(ex)


    return table

with open('awesome-python.md', encoding='utf-8') as f:
    lines = f.readlines()

repos = {}
sectionItems =[]

with open('pythonWithStart.md', 'w', encoding='utf-8') as f:
    f.writelines('# Inspired by [awesome-dotnet](https://github.com/quozd/awesome-dotnet)\n\n')
    lastLine = lines[-1]
    for i, line in enumerate(lines):
        if line.startswith('#'):
            sectionName = line
        if line.startswith('* ['):
            s = line.index('](')
            e = line.index(')', s)
            url = line[s+2:e]
            if url.startswith('https://github.com/') or url.startswith('http://github.com/'):
                try:
                    # if i == 150:
                    #     break
                    os = url.index('//github.com/')+len('//github.com/')
                    oe = url.index('/', os)
                    owner = url[os:oe]
                    proj = url[oe+1:]
                    repo ='https://api.github.com/repos/'+owner+'/'+proj
                    print(i)
                    r = requests.get(
                        'https://api.github.com/repos/'+owner+'/'+proj, auth=HTTPBasicAuth('UserName', 'Token'))
                    if(r.ok):
                        item = json.loads(r.text or r.content)
                        sectionItems.append(item)
                    else:
                        print('not ok', end=' ')
                        print(i, end=' ')
                        print(url)

                except Exception as ex:
                    print(ex)
                    print('     error ' +url)
        if line is lastLine or lines[i+1].startswith('#'):
            if len(sectionItems) > 0:
                f.writelines(createTable(sectionName, sectionItems))
                sectionItems = []
