## Homework 5 TF2 and TF1

### Introduction to Tensorflow v2

The structure of the network used is:

```
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
flatten (Flatten)            (None, 784)               0         
_________________________________________________________________
dense (Dense)                (None, 128)               100480    
_________________________________________________________________
dropout (Dropout)            (None, 128)               0         
_________________________________________________________________
dense_1 (Dense)              (None, 10)                1290      
=================================================================
Total params: 101,770
Trainable params: 101,770
Non-trainable params: 0
_________________________________________________________________
```
, so three layers - input layer of 784 inputs, a hidden layer of 128 neurons, with a dropout added to reduce over fitting, and a 10-neuron output layer.


### Accuracy Experiements

See submitted version of beginner.ipynb, 

Variations of L2 shows l2=0.0001 as optimal at 99.74% accuracy.

Variations of the dropout factor shows best at the lowest tested value of 0.05, but this may be the result of overfitting and may not be generalizable.

Experimentation with different numbers and sizes of layers did not improve on the single hidden layer with the optimized L2.


### TF2 Quickstart Lab

Contrary to the asusmption in the homework, I only received out of memory errors until I closed the beginner.ipynb and released the memory that was using.  I have run the entire model multiple times with no issues.

With the frozen feature identification layer, we achieved around 81% accuracy. When we unfroze the layer, we got over 87% in spite of training in half-sized batches to get around the memory issues.


### Alternative Hardware

As Ryan suggested, I ran the transfer learning model on both the TX2 and my newly built home computer with the following specs:

CPU:  AMD Threadripper 3970X, 32 cores @ 3.7GHz and max boost of 4.5GHz
GPU:  NVidia RTX 2080 Super, Turing architecture, 8GB GDDR6, 2944 CUDA cores, 368 Tensor cores

Step 27:
```
steps_per_epoch = np.ceil(image_data.samples/image_data.batch_size)

batch_stats_callback = CollectBatchStats()

history = model.fit_generator(image_data, epochs=2,
                              steps_per_epoch=steps_per_epoch,
                              callbacks = [batch_stats_callback])
```

on the TX2, using provided docker image: 
```
Epoch 1/2
115/115 [==============================] - 281s 2s/step - loss: 0.6960 - acc: 0.8125
Epoch 2/2
115/115 [==============================] - 206s 2s/step - loss: 0.3478 - acc: 0.9062
```

on the RTX2080, I ran the notebook model natively. The docker image is for arm64 not X86_64.
```
Epoch 1/2
115/115 [==============================] - 14s 124ms/step - loss: 0.6457 - acc: 0.8438
Epoch 2/2
115/115 [==============================] - 13s 116ms/step - loss: 0.3304 - acc: 0.9688

```

Overall, the model trained 18 times faster on the RTX with greater accuracy results. Price vs. performance and the impracticality of using a double width full-length graphics card at the edge are important factors as well. the RTX solution in a full-size PC would be better suited as a local hub where high-volume or complex models are run.  In the face recognition pipeline from HW3, using the TX2 to recognize and extract face images could be paired with face identity recognition running on a hub with an RTX card.



### Questions:

### 1. What is TensorFlow? Which company is the leading contributor to TensorFlow?
Tensorflow is a machine learning framework for training neural networks and inferring results from generalized data. The newer release 2 integrates the Keras libraries which make creating complex networks simple, especially for the early stages of development. Google's brain team were the core developers of TensorFlow, and continue to be a major contributor to the project.

### 2. What is TensorRT? How is it different from TensorFlow?
TensorRT is NVidia's Inferrence accelerator library built on CUDA and optimized for NVidia's GPU general and tensor cores. It can take pre-trained models from many different frameworks and run hardware optimized inferrence.  TensorFlow is a full ML framework, and once trained TensorFlow models can be loaded into TensorRT for run-time inferrence using NVidia's GPU hardware.


### 3. What is ImageNet? How many images does it contain? How many classes?
ImageNet is a freely available, continually expanding database of classified, labelled images for use in training vision-based ML models. It uses a hierarchical set of classes that allow multiple levels of detail in the classifications.  There are some 100,000 classes currently - called "synsets" short for synonym sets, that provide mostly noun labels for each image. ImageNet aim to have some 1000+ images per synset, or over 100,000,000 images in total. 

### 4. Please research and explain the differences between MobileNet and GoogleNet (Inception) architectures.
The key difference is the way that each model steps through the images - the convolution step. Inception uses conventional convolution - the filter takes an NxN square of pixels times the colour depth - usually 3 for RGB or 4 where there is a transparency channel -and operates using a single kernel of NxNx3.  The MobileNet convolution breaks up the convolution into multiple, vector kernels and operates them in sequence: Nx1 followed by 1XN followed by a 3x1 for the colour channels.  This results in fewer elements (2N+3) vs Inception (3N^2), and consequently fewer multiplication events.  This results in a faster and smaller model at the expense of some accuracy.

### 5. In your own words, what is a bottleneck?
A bottleneck is a single layer of a CNN with fewer neurons than the layers surrounding it.  It reduces the the number of channels in the network, limiting the number of features. In our example, the bottleneck layer takes its input from the pre-trained layers we are transfering from the ImageNet model to produce the final outputs using the new classes we are looking for.  As the previous layers are frozen, the bottleneck layer can be calculated during pre-processing to reduce time in subsequent training runs.

### 6. How is a bottleneck different from the concept of layer freezing?
The Bottleneck files produced by TF in preprocessing create a structure based on the input files as we may look at the same picture multiple times during the training.  They are NOT frozen layers, their parameters and biases can change, it just avoids having to re-extract the structure needed each time the image is used.

### 7. In the TF1 lab, you trained the last layer (all the previous layers retain their already-trained state). Explain how the lab used the previous layers (where did they come from? how were they used in the process?)
The previous layers were pre-trained as part of the ImageNet project - with the output layer removed. We take advantage of the pre-trained layers' object identification abilities, then put in our own final layer to map to the flower-specific categories we are interested in.

### 8. How does a low --learning_rate (step 7 of TF1) value (like 0.005) affect the precision? How much longer does training take?
There was no appreciable difference in training time based on learning rate for either the TX2 and RTX2080.  There were some differences in accuracy, which generally reduced for larger learning rates, but there was significant "noise" between different runs which could simply be due to the random selection of samples.

#### Details:




### 9. How about a --learning_rate (step 7 of TF1) of 1.0? Is the precision still good enough to produce a usable graph?

### 10. For step 8, you can use any images you like. Pictures of food, people, or animals work well. You can even use ImageNet images. How accurate was your model? Were you able to train it using a few images, or did you need a lot?

### 11. Run the TF1 script on the CPU (see instructions above) How does the training time compare to the default network training (section 4)? Why?
Training Time (TX2):  Default using GPU:    16m38.014s
Training Time (TX2):  Rerun using CPU Only:  


### 12. Try the training again, but this time do export ARCHITECTURE="inception_v3" Are CPU and GPU training times different?

### 13. Given the hints under the notes section, if we trained Inception_v3, what do we need to pass to replace ??? below to the label_image script? Can we also glean the answer from examining TensorBoard?