import os
import sys
import json

from urllib import request
from urllib import parse

def main():
    if len(sys.argv) < 2:
        print("usage: ./notion2md.py <filename>")
        sys.exit(0)

    with open(sys.argv[1]) as page_file:
        page_data = json.load(page_file)

    if not os.path.exists('./assets'):
        os.makedirs('./assets')
    
    result = []
    block = page_data['recordMap']['block']

    for i, v in enumerate(block):
        value = block[v]['value']

        if i == 0:
            result.append('# ' + value['properties']['title'][0][0] + '\n')
        elif value['type'] == 'text':
            if 'properties' in value:
                for text in value['properties']['title']:
                    result.append(text[0])
                result.append('\n\n')
        elif value['type'] == 'bulleted_list':
            result.append('- ' + value['properties']['title'][0][0] + '\n')
        elif value['type'] == 'divider':
            result.append('\n---\n')
        elif value['type'] == 'header':
            result.append('\n## ' + value['properties']['title'][0][0] + '\n')
        elif value['type'] == 'image':
            file_url = value['properties']['source'][0][0]
            file_name = os.path.basename(parse.urlparse(file_url).path)
            request.urlretrieve('https://www.notion.so/image/{}?table=block&id={}'.format(parse.quote(file_url, safe=''), value['id']), './assets/{}'.format(file_name))
            result.append('![Image](./assets/{})\n\n'.format(file_name))
        elif value['type'] == 'code':
            result.append('```{}\n{}\n```\n'.format(value['properties']['language'][0][0], value['properties']['title'][0][0]))
        elif value['type'] == 'quote':
            result.append('> {}\n\n'.format(value['properties']['title'][0][0]))
        else:
            print('UNKNOWN TYPE:', value['type'])

    print(''.join(result))

if __name__ == '__main__':
    main()