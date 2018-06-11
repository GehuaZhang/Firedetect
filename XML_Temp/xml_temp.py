import xml.dom.minidom
import pandas as pd
import numpy as np

def read_xml(directory):

    # Read XML
    xml_doc = xml.dom.minidom.parse(directory)
    list_object = xml_doc.getElementsByTagName('object')
    list_store = [] # store values in a list then convert to Dataframe
    list_tagName = [] # store value tag used in Dataframe columns
    list_objName = [] # store obj tag used in Dataframe rows

    for object in list_object:
        list_bndBox = object.getElementsByTagName("bndbox")
        list_objValue = list_bndBox.item(0).childNodes
        list_objName.append(object.getElementsByTagName("name").item(0).firstChild.data)

        # Drop "\n"
        list_objValue = list(filter(lambda x: x.nodeValue != "\n", list_objValue))
        list_temp_value = []
        for objValue in list_objValue:
            # Find all tag names under tag <bndbox>
            tagName = objValue.nodeName
            if not tagName in list_tagName:
                list_tagName.append(tagName)
            for coord in list_bndBox:
                # Looking for corresponding tag values
                tagValue = coord.getElementsByTagName(tagName).item(0).firstChild.data
                list_temp_value.append(tagValue)
        list_store.append(list_temp_value)

    df_bndBox = pd.DataFrame(data=list_store, columns=list_tagName, index=list_objName)
    return df_bndBox

def write_txt(fileName,dataFrame):
    np.savetxt(fileName+str(".txt"), X=dataFrame.values, fmt="%5s")
    return

test = read_xml("P0003.xml")
write_txt("test", test)
print(test)