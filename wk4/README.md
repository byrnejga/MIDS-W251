### Name all the layers in the network, describe what they do.
:`layer_defs.push({type:'input', out_sx:24, out_sy:24, out_depth:1})`  This is the input neuron layer that takes in each 28x28 image, cropped randomly down to 24x24 - one of 16 possible crops, hence the out_sx and out_sy of 24.  The images are one-bit black and white, so the depth is only 1.

`layer_defs.push({type:'conv', sx:5, filters:8, stride:1, pad:2, activation:'relu'});`
This is the first hidden layer. It is convolutional, so neurons are not fully connected, but only to a limited nubmer of neurons the following layers. It pads the input with zeros to a depth of 2, making the full image 28/28 again and traverses the input with a stride of 1 using a 5x5 kernel. There are 8 filters that make independent activation maps based on the image.  the output of this layer should be 23x23x8 - the 8 being due to the 8 different filters being used to create the activation maps.  Activation function used is ReLu.

`layer_defs.push({type:'pool', sx:2, stride:2});`
This pooling layer combines pixels to reduce the overall size, in this case using a 2x2 filter and a stride of 2, so there is no overlap between the summarised pixels

`layer_defs.push({type:'conv', sx:5, filters:16, stride:1, pad:2, activation:'relu'});`
Similar to the second layer, except with 16 filters being used, though now we are on a much smaller set of pixels due to the pooling layer before

`layer_defs.push({type:'pool', sx:3, stride:3});`
Again, pooling the output - this time each group of 9 pixels (3x3) gets pooled into 1

`layer_defs.push({type:'softmax', num_classes:10});`
This is the output layer.  We have 10 possible classes, the digits from 0-9.  softmax activation function means we get probabilities for each class instead of 1/0 answers.

### Experiment with the number and size of filters in each layer. Does it improve the accuracy?

The following are all done with running ~10,000 examples through the network.

Filter Count:
* Default: 8, 16: 0.94
* Doubled: 16, 32: 0.96, only marginal benefit for much longer training time
* Halved: 4, 8:  0.85, but noticably faster to train

Size of Filters:
* Default: 5, 5: 0.94
* Reduced: 3, 3: 0.91
* Increased: 9,9: 0.88
* Increased: 15,15: 0.12
    
Without going to much more granular experiments - tough to do with the website, the default number and size of filters seems to be reasonably well optimised at 5x5 and 8 then 16 filters.

### Remove the pooling layers. Does it impact the accuracy?
Accuracy was 0.97, higher than the default case of 0.94, but probably within the margin of randomness in the algorithm. It did however make for appreciably longer time to train with 10,000 examples.

### Add one more conv layer. Does it help with accuracy

With an additional convolutional layer (32 Filters) plus another pooling layer, and 32 filters:  0.92 
With an additional convolutional layer (32 Filters) only:  0.93

Extra pooling layer does not seem to help, so experimenting with the filter count: 

With an additional convolutional layer (32 Filters) only:0.92
With an additional convolutional layer (16 Filters) only: 0.92
With an additional convolutional layer ( 8 Filters) only: 0.92

The extra layer did degrade the model slightly, but the filters and pooling layer changes had no noticable effect.



### Increase the batch size. What impact does it have?

Batch Size = 10: 0.91
Batch Size = 20: 0.94 (Defaults)
Batch Size = 40: 0.87
Batch Size = 80: 0.91
Batch Size = 120: 0.88

### What is the best accuracy you can achieve? Are you over 99%? 99.5%?

From these experiments, I was not able to exceed the default by much - 96% at best.  Extended testing would be needed to find the best combination of all the parameters.