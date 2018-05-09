import tensorflow as tf

# Get image input first
inImage = []

# Begin
inChnlDims = [3]  # Input channel dimension: Colored image, dimension = 3.
outChnlDims = [32]  # Output channel dimension: Expected output dimension after first conv layer.
imageDims = [50, 50]  # Image dimension: For later convert image to tensor.
patchShp = [5, 5]  # Patch Shape: Shape of sliding window.
initWtShp = patchShp+inChnlDims+outChnlDims  # Shape size: 1X4 Matrix: [patch size: 2x1, input channels, output channels].
initBsShp = outChnlDims  # Shape size = initWtShp output channels.
convStrd = [1, 1, 1, 1]  # CNN Stride: step length for sliding window in Conv layers.
poolSz = [1, 2, 2, 1]  # Pooling Size. Default is 2x2: Each Pooling layer reduces 4 dimensions.
poolStrd = [1, 2, 2, 1]  # Pooling Stride: step length for sliding window in Pooling layers.
inFulConnNum = 1024  # Input Fully Connected Number: Number of nerves in FIRST fully connected layer.
outFulConnNum = 10  # Output Fully Connected Number: Number of nerves in SECOND fully connected layer.



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
        imageX = tf.reshape(image, [-1, imageDims[0], imageDims[1], inChnlDims])
        return imageX

    def weight_initial(self, shape=initWtShp):
        # Shape size: 1X4 Matrix: [patch size: 2x1, input channels, output channels]
        initial = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(initial)

    def bias_initial(self, shape=initBsShp):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)


    
    ## CNN Model
    def conv2d(self, inputX, weight, strides=convStrd):
        return tf.nn.conv2d(inputX, weight, strides=strides, padding='SAME')

    def max_pool_2x2(sefl, x, ksize=poolSz, strides=poolStrd):
        return tf.nn.max_pool(x, ksize=ksize, strides=strides, padding='SAME')




    ## Process Model
    def verify_dimension(self):
        # Left blank now.
        # For verify dimension of image after pooling is still capable of processing another conv.
        return



    def CNN_recursion(self, conv_times, xTemp, weightShp, biasShp, outDim):
        if conv_times == 0:
            return xTemp, outDim

        weightConv = self.weight_initial(shape=weightShp)
        biasConv = self.bias_initial(shape=biasShp)

        conv = tf.nn.relu(self.conv2d(xTemp, weightConv) + biasConv)
        pool = self.max_pool_2x2(conv)

        weightShp = patchShp + [outDim] + [outDim*2]
        biasShp = [outDim*2]
        outDim = outDim*2

        return self.CNN_recursion(conv_times-1, pool, weightShp, biasShp, outDim)



    def fully_connected(self, xTemp, outDim):
        flatSize = len(xTemp.reshape(-1)) * outDim

        weightFulConn_1 = self.weight_initial([flatSize, inFulConnNum])
        biasFulConn_1 = self.bias_initial([inFulConnNum])

        poolFlat_1 = tf.reshape(xTemp, [-1, flatSize])
        convFulConn_1 = tf.nn.relu(tf.matmul(poolFlat_1, weightFulConn_1) + biasFulConn_1)

        convDrop = self.drop_out(convFulConn_1)

        weightFulConn_2 = self.weight_initial([inFulConnNum, outFulConnNum])
        biasFulConn_2 = self.bias_initial([outFulConnNum])

        convFinal = tf.nn.softmax(tf.matmul(convDrop, weightFulConn_2) + biasFulConn_2)

        return convFinal



    # Avoid over-fitting
    def drop_out(self, xTemp):
        keep_prob = tf.placeholder(tf.float32)
        return tf.nn.dropout(xTemp, keep_prob)



    # For test of whole class
    def test_class(self):
        imageX = self.image_initial(inImage)
        xTmep, outDim = self.CNN_retursion(2, imageX, initWtShp, initBsShp, outChnlDims)
        self.fully_connected(xTmep, outDim)
        return


    # For test of recursion ONLY
    def test_recursion(self):
        imageX = self.image_initial(inImage)
        self.CNN_retursion(2, imageX, initWtShp, initBsShp, outChnlDims)



temp = FireDetect()
temp.test_class()