import glob
import imageio
import numpy as np
import matplotlib.pyplot as plt
plt.ion()

images = glob.glob('DSC*')
print ("Hay %i imagenes disponibles para combinar." % len(images))

test = imageio.imread(images[0])
pictures = np.zeros([test.shape[0],test.shape[1],test.shape[2],len(images)])
print ("Las dimensiones de cada imagen son %i pix x %i pix" % (test.shape[0],test.shape[1]))

for i,j in enumerate(images):
	pictures[:,:,:,i] = imageio.imread(j)
	plt.figure(); plt.imshow(imageio.imread(j))

img_mean = np.zeros_like(test)
img_median = np.zeros_like(test)
img_std = np.zeros_like(test)

for i in range(3):
    img_mean[:,:,i] = np.mean(pictures[:,:,i,:], axis=2)
    img_median[:,:,i] = np.median(pictures[:,:,i,:], axis=2)
    img_std[:,:,i] = np.std(pictures[:,:,i,:], axis=2)

plt.figure(); plt.imshow(img_mean)
plt.figure(); plt.imshow(img_median)
plt.figure(); plt.imshow(img_std)