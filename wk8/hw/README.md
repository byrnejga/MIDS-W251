## Homework 8 - James Byrne

### PART 1, Questions:

#### 1. In the time allowed, how many images did you annotate?
I 3 hours I managed almost 340 of the images.  It went much faster once I worked out the keyboard shortcuts.  I continued after the 3 hours to complete all the images.
#### 2. Home many instances of the Millennium Falcon did you annotate? How many TIE Fighters?
```
$ cat *.xml | grep -c "<name>Millennium Falcon</name>"
307

 cat *.xml | grep -c "<name>Tie Fighter</name>"
270
```
#### 3. Based on this experience, how would you handle the annotation of large image data set?
Typically this would be a manual exercise, so I would look to crowdsource labeling of large image sets like this.

I would also consider using available object detection and framing models, use the 300 or so I just tagged by hand to at least find and frame possible instances of fighters or the Falcon and have it output in a form labelimg could use. It could then be much faster to run through many more pictures when we could just accept the simple network's answer, adjust it or pick up errors and instances where it may have missed a ship in the more complex scenes.


#### 4. Think about image augmentation? How would augmentations such as flip, rotation, scale, cropping, and translation effect the annotations?o

Provided the frame coordinates were similarly transformed, we could significantly increase the dataset size.  We could also check whether the crops we select still include at least one predefined frame and automatically reject crops that do not have one.  Cropping partial frames would be OK as we already include partial images in the manual exercise, the frames would just need to be altered to meet the image boundary.

Before doing that, however, I would consider stripping off the black letterbox bars from the images. They contain no information, and increase the likelihood that cropping scaling or other distortion augmentation techniques result in an output with no labeled objects.



### PART 2, Questions:

#### 1. Describe the following augmentations in your own words

To generate more images for the data set, the augmentations create similar images, but due to the transformations used, will train different parts of the image detection netwkork.

It may be necessary to rescale or pad both original and augmenting images to a standard resolution expected by the input layer of a CNN.


#### Flip
mirror the image either vertically or horizontally - doing both is the equvalent of a 180^o.
##### Rotation
The image can be rotated - usually by 90^o, 180^o or 270^o. Rotation can be used in conjunction with flips, but be sure to avoid using multiple combinations that add up to the same transformation.

##### Scale
The image can be scaled up or down, changing the size of the objects (also known as zooming). Scaling can also be anamorpic, resulting in distorted pictures of the objects, but preserving the core features (also referred to as stretching).

##### Crop
We can randomly crop sections out of each picture, effectively changing the position of the objects. Checks should be included to ensure we do not end up cropping out the objects of interest. Partially cropping the objects is generally OK, as we would typically tag partial or occluded images of objecs by hand.

##### Translation
Translation moves the object of interest within the frame and avoids image recognition models only being able to identify objects that are in a particular part of the image. 

##### Noise
Noise augmentation introduces either random image variations - like analog TV smow - or uses a blurring algorithm (usually a gaussian) to reduce detail. Noisy pictures will help generalization of the trained network. 

### PART 3, Questions:

#### 1. Image annotations require the coordinates of the objects and their classes; in your option, what is needed for an audio annotation?
For audio annotation, in addition to the label, we would need the start and end timings of the labelled sound, possibly down to the specific sound sample level - the equivalent of image tagging tightly to the nearest pixel. 
