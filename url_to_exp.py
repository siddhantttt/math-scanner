import numpy as np
from skimage.feature import hog
from skimage.morphology import skeletonize
from skimage.util import invert
from sklearn.externals import joblib
import urllib2
import matplotlib.pyplot as plt
import cv2

def url_to_image(url):
    resp = urllib2.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def seg_rowwise(img1):
    img=img1
    rowwiseSum=[0 for i in range(img.shape[0])]
    for i in range(len(rowwiseSum)):
        for j in range(img.shape[1]):
            rowwiseSum[i]+=(255-img[i][j])
    
    x=np.zeros(100000)
    y=np.zeros(100000)
    flag = 0
    c=0
    for i in range(0,img.shape[0]):
        if rowwiseSum[i] != 0 and flag == 0 :
            x[c] = i
            flag = 1
        elif rowwiseSum[i] == 0 and flag == 1 :
            y[c] = i
            flag = 0
            c = c+1
            
    for i in range(0,c):
        if(y[i] - x[i] > 80):
            temp1=int(x[i])
            temp2=int(y[i])
            img1=img[temp1:temp2,:]
            break
    return img1

def create_exp(img):
    Lreg_lb = joblib.load("lreglb(new).pkl")
    #img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img_gb=cv2.GaussianBlur(img,(5,5),0)
    img_th = cv2.threshold(img_gb, 127, 255, cv2.THRESH_BINARY )[1]
    segmented=seg_rowwise(img_th)
    
    columnwiseSum=[0 for i in range(segmented.shape[1])]
    for i in range(len(columnwiseSum)):
        for j in range(segmented.shape[0]):
            columnwiseSum[i]+=(255-segmented[j][i])
    
    x= np.zeros(50)
    flag = 0
    c=0
    k=0
    for i in range(0,segmented.shape[1]):
        if columnwiseSum[i] >765 and flag == 0 :
            x[c] = int((i+k)/2)
            flag = 1
            c=c+1
        elif columnwiseSum[i] == 0 and flag == 1 :
            k = i
            flag = 0
    x[c]=int((segmented.shape[1]+k)/2)
    plt.imshow(segmented,'gray')
    plt.show()
    exp=[]

    seg_count = 0
    for i in range(0,c+1):
        if(x[i+1] - x[i] > 30):
            temp1=int(x[i])
            temp2=int(x[i+1])
            seg = segmented[:, temp1 : temp2]
            segment = seg_rowwise(seg)
            plt.imshow(segment)
            plt.show()
            resized = cv2.resize(segment,(32,32),interpolation=cv2.INTER_AREA)
            img_new = cv2.threshold(resized, 130 , 255, cv2.THRESH_BINARY )[1]            
            skeleton=skeletonize(invert(np.array(img_new,'bool')))
            converted=np.array(invert(skeleton),'float32')
            plt.imshow(converted)
            plt.show()
            ret,hogImg=hog(converted,orientations=9,pixels_per_cell=(2,2),cells_per_block=(1,1),visualise=True)
            plt.imshow(hogImg)
            plt.show()
            pred=Lreg_lb.predict(np.array(ret,'float64'))
            exp.append(str(pred[0]))
            #if exp[seg_count-1]=='/' or exp[seg_count-1]=='-' or exp[seg_count-1]=='*' or exp[seg_count-1]=='+' :
            #    exp.pop()
            seg_count = seg_count + 1
    return exp
