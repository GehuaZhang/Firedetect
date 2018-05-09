import tensorflow as tf

# Get image input first
inImage = []


imageDims = [50, 50]
channelDims = 3
initWtShp = [0, 0, channelDims, 0]  # Shape size: 1X4 Matrix: [patch size: 2x1, input channels, output channels].
initBsShp = [initWtShp[-1]]  # Shape size = initWtShp output channels.
convStrd = [1, 1, 1, 1]  # CNN Stride: step length for sliding window in Conv layers.
poolSz = [1, 2, 2, 1]  # Pooling Size. Default is 2x2: Each Pooling layer reduces 4 dimensions.
poolStrd = [1, 2, 2, 1] # Pooling Stride: step length for sliding window in Pooling layers


class FireDetect:

    def __init__(self):
        # Open Session for TensorFlow Connect to C++
        sess = tf.InteractiveSession()
        # Test Running of Session
        test_sess = tf.constant('Session Established')
        try:
            print(sess.run(test_sess))
        except:
            print("Session Starting Fails")
            exit()



    # Initialize Model

    def image_initial(self, image):
        imageX = tf.reshape(image, [-1, imageDims[0], imageDims[1], channelDims])
        return imageX

    def weight_initial(self, shape=initWtShp):
        # Shape size: 1X4 Matrix: [patch size: 2x1, input channels, output channels]
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_initial(self, shape=initBsShp):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)



    # CNN Model

    def conv2d(self, inputX, weight, strides=convStrd):
        return tf.nn.conv2d(inputX, weight, strides=strides, padding='SAME')

    def max_pool_2x2(sefl, x, ksize=poolSz, strides=poolStrd):
        return tf.nn.max_pool(x, ksize=ksize, strides=strides, padding='SAME')


    #Process Model

    def CNN_train(self):

        # Could update with loops

        W_conv1 = self.weight_initial()
        b_conv1 = self.bias_variable()
        imageX = self.image_initial(inImage)

        h_conv1 = tf.nn.relu(self.conv2d(imageX, W_conv1) + b_conv1)
        h_pool1 = self.max_pool_2x2(h_conv1)




        W_conv2 = weight_variable([5, 5, 32, 64])
        b_conv2 = bias_variable([64])

        h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
        h_pool2 = max_pool_2x2(h_conv2)
