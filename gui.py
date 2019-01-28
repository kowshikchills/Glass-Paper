import tkinter as tk
from tkinter import *
import matplotlib as ploty
ploty.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import warnings 
warnings.filterwarnings("ignore")
def imgpros(URL):
			import numpy as np
			
			from skimage.segmentation import slic
			from skimage import filters,io,morphology,color,data,exposure,img_as_float,feature
			from scipy import ndimage as ndi
			from skimage import feature
			from skimage import io
			from skimage.morphology import watershed
			from skimage.feature import peak_local_max
			from skimage.morphology import closing,dilation,opening,white_tophat,erosion,skeletonize
			from skimage.morphology import disk
			from skimage.filters.rank import median,mean
			from skimage.measure import regionprops
			from skimage.morphology import remove_small_objects

			d1  = disk(0)     #(EROSION)Thickness improvement
			d2 = disk(10)      #opening radius 
			d3 = disk(0)      #Noise reduction                    
			d4 = disk(0)      #smoothing
			d5 = disk(1)      #Dilation
			bimg = io.imread(URL)
			cimg = bimg
			image = img_as_float(cimg)
			gamma_corrected = exposure.adjust_gamma(image, 1)
			gamma_corrected = exposure.equalize_hist(gamma_corrected)
			gamma_corrected = exposure.equalize_adapthist(gamma_corrected)
			gamma_corrected = exposure.rescale_intensity(gamma_corrected)
			img  =gamma_corrected 
			imgg = color.rgb2gray(img)
			imgg1 = mean(imgg, d4)
			imgg2 = median(imgg1, d3) 
			dilated =dilation(imgg2,d5)
			eroded = erosion(dilated, d1) 
			thresh = filters.threshold_adaptive(eroded,250,'gaussian')
			BW = imgg>=thresh
			BW_smt = remove_small_objects(BW,500) 
			opened = opening(BW_smt ,d2)
			distance = ndi.distance_transform_edt(~BW_smt)
			labels = morphology.label(~opened, background=-1)
			labels = morphology.remove_small_objects(labels,500) 
			########################################################
			props = regionprops(labels)
			END = []
			for i in range(len(np.unique(labels))-1):
			    if 10 in props[i].coords:
			        END.append(i)
			for i in range(len(np.unique(labels))-1):
			    if 899 in props[i].coords:
			        END.append(i)
			#########################################################
			from scipy import ndimage
			X = []
			Y = []
			for i in np.unique(labels)[1:]:
			    X.append(ndimage.measurements.center_of_mass(labels == i)[1])
			    Y.append(ndimage.measurements.center_of_mass(labels == i)[0])

			from skimage.color import label2rgb
			import matplotlib.patches as mpatches

			label_overlay = label2rgb(labels, image=image)
			global fig
			global ax
			fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
			#ax.imshow(label_overlay)

			props = regionprops(labels)
			for  i in range(len(regionprops(labels))):

			    
			    if props[i].area < 100:
			        continue 
			    if i in END:
			        minr, minc, maxr, maxc = props[i].bbox
			        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
			                               fill=False, edgecolor='white', linewidth=1)
			    else:
			        minr, minc, maxr, maxc = props[i].bbox
			        rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
			                               fill=False, edgecolor='red', linewidth=1)
			        
			    
			ax.add_patch(rect)
			global ans
			ans = len(np.unique(labels))

			#plt.plot(X,Y,'ro')
			#plt.show()
			#print 'Number of Fragments Observed',len(np.unique(labels))
			#print 'Number of End Pieces Observed',len(END),'End Pieces'
			############################################################
			
URL = 'C:/Users/sai_praneeth7777/Desktop/crop.jpg'

root = Tk()
# label = Label(root, text="Graph Page!")
# label.pack(pady=10,padx=10)
imgpros(URL)

w2 = Label(root, 
           justify=LEFT,
           padx = 10, 
           text=ans).pack(side="left")

f = fig
a = f.add_subplot(111)
a.plot(ax)

canvas = FigureCanvasTkAgg(f,root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

toolbar = NavigationToolbar2TkAgg(canvas,root)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
root.mainloop()