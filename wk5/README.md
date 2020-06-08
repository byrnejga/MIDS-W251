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

on the RTX2080, run natively as the docker image is for arm64 not X86_64 architecture:
```
Epoch 1/2
115/115 [==============================] - 14s 124ms/step - loss: 0.6457 - acc: 0.8438
Epoch 2/2
115/115 [==============================] - 13s 116ms/step - loss: 0.3304 - acc: 0.9688

```

Overall, the model trained 18 times faster on the RTX, but of course, price vs. performance and the impracticality of using a double width full-size graphics card at the edge are important factors as well. the full-size PC would be better suited as a local hub where high-volume or complex models are run.

