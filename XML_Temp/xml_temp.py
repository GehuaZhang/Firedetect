import xml.dom.minidom
import pandas as pd
import numpy as np

def read_xml(directory):

    # Read XML
    xml_doc = xml.dom.minidom.parse(directory)

    # Get XML's General Information, including <folder><filename><type><sourceImage>
    value_folder = xml_doc.getElementsByTagName('annotation').item(0).getElementsByTagName("folder").item(0).firstChild.data
    value_fileName = xml_doc.getElementsByTagName('annotation').item(0).getElementsByTagName("filename").item(0).firstChild.data
    value_sourceType = xml_doc.getElementsByTagName('source').item(0).getElementsByTagName("type").item(0).firstChild.data
    value_sourceImage = xml_doc.getElementsByTagName('source').item(0).getElementsByTagName("sourceImage").item(0).firstChild.data
    str_info = "%s\n%s\n%s\n%s\n" % (value_folder, value_fileName, value_sourceType, value_sourceImage)

    list_object = xml_doc.getElementsByTagName('object')
    list_store = [] # store values in a list then convert to Dataframe
    list_tagName = ["x1","y1","x2","y2","x3","y3","x4","y4","centerx","centery","widthRot","heightRot","AngleDegree(0,360)","xmin","ymin",
                    "xmax","ymax","Remarks", "Others"]  # Dataframe columns
    str_info += ", ".join(list_tagName) # Store All Descriptive Information

    for object in list_object:
        list_polygon = object.getElementsByTagName("polygon")
        value_name = object.getElementsByTagName("name").item(0).firstChild.data
        value_moving = object.getElementsByTagName("moving").item(0).firstChild.data

        for polygon in list_polygon:
            #value_t = polygon.getElementsByTagName("t").item(0).firstChild.data #Label for each polygon
            #list_objName.append(value_t)
            list_pt = polygon.getElementsByTagName("pt")
            arr_x, arr_y, arr_l = np.empty(list_pt.length), np.empty(list_pt.length), np.empty(list_pt.length)

            for i in range(len(list_pt)):
                pt = list_pt[i]
                arr_x[i] = pt.getElementsByTagName("x").item(0).firstChild.data
                arr_y[i] = pt.getElementsByTagName("y").item(0).firstChild.data

            list_extreme = [min(arr_x), min(arr_y), max(arr_x), max(arr_y)]
            list_center = [np.mean(arr_x), np.mean(arr_y)]
            list_length = [np.ptp(arr_x), np.ptp(arr_y)]
            list_direction = [0]
            list_remark = [str(value_name)+" "+str(value_moving)]
            list_value = list(np.vstack((arr_x, arr_y)).flatten("F"))
            list_row = list_value + list_center + list_length + list_direction + list_extreme + list_remark + list_direction

            list_store.append(list_row)

    df_bndBox = pd.DataFrame(data=list_store, columns=list_tagName)
    return df_bndBox, str_info


def write_txt(fileName, dataFrame, description):
    np.savetxt(fileName+str(".txt"), X=dataFrame.values, fmt="%s", header=description)
    return

df_test, descrip = read_xml("output.xml")
print(df_test)
write_txt("test", df_test, descrip)
