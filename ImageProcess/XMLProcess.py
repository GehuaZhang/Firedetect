
import xml.dom.minidom


def xml_process(directory='output.xml', objectType="fire", objectID = 1):

    # Read Data
    xml_doc = xml.dom.minidom.parse(directory)
    list_object = xml_doc.getElementsByTagName('object')

    # Check If Required Object Exist
    object_exist = False

    for temp_object in list_object:
        if temp_object.getElementsByTagName('name').item(0).childNodes[0].data == str(objectType) \
        and temp_object.getElementsByTagName('id').item(0).childNodes[0].data == str(objectID):
            objects = temp_object
            object_exist = True
            break
        else:
            continue

    if not object_exist:
        print("No such object type as "+str(objectType)+", or such ID as "+str(objectID))
        return

    # For Existed Object, Do Following
    # Looking for "polygon"
    list_polygon=objects.getElementsByTagName('polygon')

    dict_coord = {}
    if len(list_polygon) > 0:
        for polygon in list_polygon:

            # Looking for "t", store its value as ID of each node
            temp_id = polygon.getElementsByTagName("t").item(0).childNodes[0].data
            dict_coord[temp_id] = []

            # Looking for "pt", store its value as coordinate of x,y,l
            list_points = polygon.getElementsByTagName("pt")
            if len(list_points) > 0:
                for points in list_points:
                    temp_x = points.getElementsByTagName('x').item(0).firstChild.data
                    temp_y = points.getElementsByTagName('y').item(0).firstChild.data
                    temp_l = points.getElementsByTagName('l').item(0).firstChild.data

                    dict_coord[temp_id].append([temp_x, temp_y, temp_l])
    return dict_coord

test = xml_process()
print(test)