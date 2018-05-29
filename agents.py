import xml.etree.cElementTree as ET
import pandas as pd

tree = ET.parse('./files/allagents.xml')

root = tree.getroot()
headers = ['ID','Title','Description','Type','Comments','Link 1','Link 2']

df = pd.DataFrame(columns=headers)

for node in root:
    ID = node.find('ID').text
    title = node.find('String').text
    desc = node.find('Description').text
    type = node.find('Type').text
    comment = node.find('Comment').text
    link1 = node.find('Link1').text
    link2 = node.find('Link2').text

    df = df.append(
        pd.Series([ID,title,desc,type,comment,link1,link2],index=headers),ignore_index=True
    )

df.to_csv('agents_data.csv',index=False)
