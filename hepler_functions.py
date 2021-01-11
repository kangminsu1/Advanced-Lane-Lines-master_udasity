import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import os

OUTPUT_IMAGE_DIR = 'output_images/'


def show_two_image(image1, image2, title1="Original Image", title2="Transformed Image"):
    f, (ax1, ax2) = plt.subplots(1, 2, figsize=(24, 9))
    f.tight_layout()
    ax1.imshow(image1)
    ax1.set_title(title1, fontsize=50)
    ax2.imshow(image2)
    ax2.set_title(title2, fontsize=50)
    plt.subplots_adjust(left=0., right=1, top=0.9, bottom=0.)
    plt.show()


def get_output_image_path(original_image_path, prefix=''):
    return os.path.join(OUTPUT_IMAGE_DIR, prefix + os.path.basename(original_image_path))


def show_images(list_of_images, nb_column=1, list_of_title_names=[]):
    fig = plt.figure(figsize=(15,15))
    number_of_images = len(list_of_images)
    nb_row = number_of_images // nb_column
    for i in range(number_of_images):
        a = fig.add_subplot(nb_row , nb_column, i+1)
        if list_of_title_names:
        	a.set_title(list_of_title_names[i],fontsize=30)
        plt.imshow(list_of_images[i], cmap='Greys_r')
        #plt.axis('off')
    plt.tight_layout(pad=0.1, w_pad=0.1, h_pad=0.1)
    plt.show()