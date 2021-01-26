import os
import sys
import json

from urllib import request
from urllib import parse

def main():
    if len(sys.argv) < 2:
        print("usage: ./notion2md.py <filename>")
        sys.exit(0)

    if not os.path.exists('./assets'):
        os.makedirs('./assets')

    with open(sys.argv[1]) as page_file:
        page_data = json.load(page_file)
    
    result = []
    block = page_data['recordMap']['block']

    for i, v in enumerate(block):
        value = block[v]['value']

        if i == 0:
            result.append('# ' + value['properties']['title'][0][0])
        elif 'properties' in value:
            properties = value['properties']

            if value['type'] == 'text':
                for text in properties['title']:
                    result.append(text[0])

            elif value['type'] == 'bulleted_list':
                result.append('- ' + properties['title'][0][0])

            elif value['type'] == 'divider':
                result.append('---')

            elif value['type'] == 'header':
                result.append('## ' + properties['title'][0][0])

            elif value['type'] == 'image':
                file_url = properties['source'][0][0]
                file_name = os.path.basename(parse.urlparse(file_url).path)

                request.urlretrieve('https://www.notion.so/image/{}?table=block&id={}'.format(parse.quote(file_url, safe=''), value['id']), './assets/{}'.format(file_name))
                result.append('![Image](./assets/{})'.format(file_name))

            elif value['type'] == 'code':
                result.append('```{}\n{}\n```'.format(properties['language'][0][0], properties['title'][0][0]))

            elif value['type'] == 'quote':
                result.append('> {}'.format(properties['title'][0][0]))

            else:
                print('{} UNKNOWN TYPE ({})'.format(v, value['type']), file=sys.stderr)
        else:
            print('{} PROPERTIES NOT FOUND'.format(v), file=sys.stderr)

    print('\n\n'.join(result))

if __name__ == '__main__':
    main()