



# Specifically For Decode Vatic XML Data to Yolo Format


from bs4 import BeautifulSoup
import numpy as np
import os


class VaticToSSD():

    def __init__(self, XML_directory, size_directory, annot_direcory):
        self.XML_directory = XML_directory
        self.soup = BeautifulSoup(open(XML_directory), "lxml")
        self.size_directory = size_directory
        self.annot_directory = annot_direcory


    def vaticReplace(self, frame_interval = 1, start_frame = 0):
        soup = self.soup

        soup.source.type.name = "database"
        soup.source.database.string.replace_with("Mivis_Fire")

        soup.source.sourceimage.name = "annotation"
        soup.source.annotation.string.replace_with("Mivis_Fire Annotation")

        soup.source.sourceannotation.name="image"
        soup.source.image.string.replace_with("NAL")

        a = soup.find_all(["moving","action","verified","id","createdframe","startframe","endframe"])
        for x in a:
            x.decompose()

        add_tags = soup.find_all("object")
        for add_tag in add_tags:
            add_tag.append(soup.new_tag("pose", href="Noaaane"))

        #print(soup.prettify())
        #f = open("converted.xml", 'wb')
        #f.write(soup.encode('utf-8'))

    def readSize(self):
        # read image size from txt file then store it in an int list
        size_directory = self.size_directory
        f = open(size_directory, "r")
        picSize = list(map(int, f.read().split()))  # Read file then convert it to int list
        return picSize


    # bndbox parameter should be in format: [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]
    # Return [centralPos, range] in ratio to the entire image
    def calculateBndbox(self, bndbox):
        imgSize = np.array(self.readSize())  # Obtain image width and height
        bndbox = np.array(bndbox)
        centralPos = (bndbox.sum(axis=0)/4.0)/imgSize
        centralPos = np.round(centralPos,5)
        range = (bndbox.max(axis=0)-bndbox.min(axis=0))/imgSize
        range = np.round(range,5)

        print("Bndbnx Coordinate: "+str(bndbox))
        print("Image Size: "+str(imgSize))
        print("Center Position and Range: "+str([centralPos, range]))
        return [centralPos, range]


    def bndboxExtract(self, searchType = "fire"):
        soup = self.soup
        nameNames = soup.find_all("name")
        objs = []
        polygons = []
        frameList = []
        bndboxList = []
        for name in nameNames:
            if name.string == searchType:
                objs.append(name.parent)

        for obj in objs:
            polygons += obj.find_all("polygon")

        for polygon in polygons:
            framePos = polygon.find("t").string
            frameList.append(framePos)
            points = polygon.find_all("pt")
            bndbox = []
            if len(points) != 4:
                print("point number problem")
                return
            for point in points:
                xPos = int(point.find("x").string)
                yPos = int(point.find("y").string)
                bndbox.append([xPos, yPos])
            bndboxList.append(bndbox)

        if len(frameList) != len(bndboxList):
            print("frame length not match with bndbox length")
            return

        return [frameList, bndboxList]


    def main(self):
        dictBndbox = {}
        frameList, bndboxList = self.bndboxExtract(searchType = "fire")  # Only Extract Fire's Bndbox
        for idx in range(len(frameList)):
            print("\nProcessing frame %s" % frameList[idx])
            bndbox = self.calculateBndbox(bndboxList[idx])

            if str(frameList[idx]) in dictBndbox.keys():
                dictBndbox[str(frameList[idx])] += bndbox
            else:
                dictBndbox[str(frameList[idx])] = bndbox



        annot_path = os.path.join(self.annot_directory, self.XML_directory[:-4])

        if not os.path.exists(annot_path):
            os.mkdir(annot_path)



        # Single Object Detection
        # Only for fire
        for key, value in dictBndbox.items():
            fileName = "%s.txt" % (key)
            annot_directory_name = os.path.join(annot_path, fileName)
            f = open(annot_directory_name, "w")

            content = [" ".join(x.astype(str)) for x in value]
            content = " ".join(content)
            content = "0"+" "+content
            f.write(content)
            f.close()



a = VaticToSSD(XML_directory = "fire1_annot.xml", size_directory= r'D:\AliothAtlas\Project\FireTrain\Mivis_Fire\Size\fire1.txt',
               annot_direcory = r'D:\AliothAtlas\Project\FireTrain\Mivis_Fire\yolo_annot')
#a.bndboxExtract()
#a.readSize()
#a.calculateBndbox([[1,1],[2,1],[2,4],[1,4]])
a.main()