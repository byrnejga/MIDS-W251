## Homework 8 - James Byrne

### Questions:

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




