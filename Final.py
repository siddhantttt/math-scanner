from cv2 import GaussianBlur, threshold, resize, imread
from numpy import zeros,array
from skimage.feature import hog
from skimage.morphology import skeletonize
from skimage.util import invert
from sklearn.externals import joblib
import urllib.request

def create_exp():
    Lreg_lb = joblib.load("digits_cls.pkl")
    url=#put  url here
    img=url_to_image(url)
    img_gb=GaussianBlur(img,(5,5),0)
    img_th = threshold(img_gb, 127, 255, cv2.THRESH_BINARY )[1]
    
    rowwiseSum=[0 for i in range(img_th.shape[0])]
    for i in range(len(rowwiseSum)):
        for j in range(img_th.shape[1]):
            rowwiseSum[i]+=(255-img_th[i][j])
    
    x=zeros(100)
    y=zeros(100)
    flag = 0
    c=0
    for i in range(0,img_th.shape[0]):
        if rowwiseSum[i] != 0 and flag == 0 :
            x[c] = i
            flag = 1
        elif rowwiseSum[i] == 0 and flag == 1 :
            y[c] = i
            flag = 0
        c = c+1 
    
    for i in range(0,c):
        if(y[i] - x[i] > 30):
            temp1=int(x[i])
            temp2=int(y[i])
            segmentedImg=img_th[temp1:temp2,:]
            break
    
    columnwiseSum=[0 for i in range(segmentedImg.shape[1])]
    for i in range(len(columnwiseSum)):
        for j in range(segmentedImg.shape[0]):
            columnwiseSum[i]+=(255-segmentedImg[j][i])
    
    x= zeros(50)
    flag = 0
    c=0
    k=0
    for i in range(0,segmentedImg.shape[1]):
        if columnwiseSum[i] >765 and flag == 0 :
            x[c] = int((i+k)/2)
            flag = 1
            c=c+1
        elif columnwiseSum[i] == 0 and flag == 1 :
            k = i
            flag = 0
    x[c]=int((segmentedImg.shape[1]+k)/2)
    
    exp=[]
    seg_count = 0
    for i in range(0,c+1):
        if(x[i+1] - x[i] > 50):
            temp1=int(x[i])
            temp2=int(x[i+1])
            segment = segmentedImg[:, temp1 : temp2]
            resized = resize(segment,(32,32),interpolation=cv2.INTER_AREA)
            img_new = threshold(resized, 127 , 255, cv2.THRESH_BINARY )[1]
            skeleton=skeletonize(invert(np.array(img_new,'bool')))
            converted=array(invert(skeleton),'float32')
            hogImg=hog(converted,orientations=9,pixels_per_cell=(4,4),cells_per_block=(1,1),visualise=False)
            pred=Lreg_lb.predict(np.array(hogImg,'float64'))
            exp.append(pred[0])
        #change starts here
            seg_count = seg_count + 1
        if exp[seg_count-1]=="\ " or exp[seg_count-1]=='-' or exp[seg_count-1]=='*' or exp[seg_count-1]=='+':
            exp.pop()
        #change ends here
    return exp