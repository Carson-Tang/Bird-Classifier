from numpy import expand_dims
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import ImageDataGenerator
from matplotlib import pyplot


img = load_img('bird.jpg')

data = img_to_array(img)

samples = expand_dims(data, 0)

data_gen_args = dict(featurewise_center=True,
                     featurewise_std_normalization=True,
                     rotation_range=90,
                     width_shift_range=0.1,
                     height_shift_range=0.1,
                     brightness_range=[0.5, 1],
                     zoom_range=0.2,)

datagen = ImageDataGenerator(**data_gen_args)

it = datagen.flow(samples, batch_size=1)

for i in range(9):

    pyplot.subplot(330 + 1 + i)

    batch = it.next()

    image = batch[0].astype('uint8')

    pyplot.imshow(image)

pyplot.show()
