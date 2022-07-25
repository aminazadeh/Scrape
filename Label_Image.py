import os 
import glob
import pandas as pd
import xml.etree.ElementTree as Et

current_dir = 'C:\\Users\\mehdi\\Desktop\\Scrape\\Tensor\\Image'

def xml_to_csv(path):

    xml_lst = list()

    for xml_file in glob.glob(path + '/*.xml'):
        tree = Et.parse(xml_file)
        root = tree.getroot()

        for rt in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     rt[0].text,
                     int(rt[4][0].text),
                     int(rt[4][1].text),
                     int(rt[4][2].text),
                     int(rt[4][3].text),
                    )

            xml_lst.append(value)
    columns = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    df = pd.DataFrame(xml_lst, columns= columns)
    
    return df


def main():
    list_of_cities = ['Isfahan', 'Tehran', 'Karaj', 'Qom','Qazvin', 'Shiraz', 'Tabriz', 'Mashad']
    
    for dir in ['train', 'test']:
        images_paths = os.path.join(current_dir, f'Isfahan\{dir}')
        xml_df = xml_to_csv(images_paths)
        xml_df.to_csv('{0}/{1}_labels.csv'.format(current_dir+'\\Isfahan\\Labeled',dir), index=None)
        print('SUCCESS!')
        # print(images_paths)

main()