
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np


class ImageProcess(object):
    def __init__(self, pathText):
        sess_image = tf.InteractiveSession()
        file = tf.gfile.FastGFile(pathText, 'rb').read()
        deImage = tf.image.decode_png(file, channels=3)
        # Convert int to float
        floatImage = tf.image.convert_image_dtype(image=deImage, dtype=tf.float32)

        self.imageTemp = sess_image.run(floatImage)
        print(self.imageTemp.shape)

    # Read batch of images
    def batch(self):
        return

    # Write to TFRecord
    def toTFRecord(self):
        return

    def image_resize(self, imageShape):
        self.ImageResz = tf.image.resize_images(self.imageTemp, imageShape)
        return

    def image_show(self):
        plt.imshow()
        plt.show()



a = ImageProcess("1.png")
a.image_resize(imageShape = [200,1000])
a.image_show()