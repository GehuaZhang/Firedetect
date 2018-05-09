### 变量名前面加入(改)是指需要重新赋值的

### 变量名前面加入(恒)是指恒定值不用管

### 变量名前面加入(默)是指任意值都可以, 但默认值也可以不改




(恒)inChnlDims: 代表图像维度，我们恒定等于3.

(恒)initWtShp: 初始权重的大小，一旦其他值确定，该值确定.

(恒)initBsShp: 初始截距(偏差bias)的大小，同上.

(改)inImage: 是导入的图片，像素必须填入imageDims

(改)mageDims: 填入inImage的像素

(默)outChnlDims: 代表卷积核个数的值，即第一次卷积后，图像厚度从3扩展到32.

(默)patchShp: 代表窗口大小

(默)convStrd: 卷积步长, 默认值可以不改

(默)poolSz: pool的大小, 默认值可以不改

(默)poolStrd: pool的步长，默认值可以不改

(默)inFulConnNum: 全连接神经网络第一层神经元个数

(默)outFulConnNum: 全连接神经网络第二层神经元个数


### init测试了tensor能否打开

### image_initial把图片的矩阵变为tensor

### 然后初始化weight和bias





