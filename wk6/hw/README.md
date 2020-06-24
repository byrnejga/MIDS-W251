## Comment
It took some time to work out that the prediction call to the model in the batch loop returned a tuple with one tensor member instead of a tensor type which then failed in the loss function,  so I had to replace:
```
y_pred = model(x_batch.to(device.....
```
with
```
y_pred**,** = model(x_batch.to(device....
```
so that y_pred was a tensor that could work with the loss function.

The documentation for transformers and pyTorch both still claimed the model will return a tensor of the predicted results - this is probably another version problem in the docker image.

## Comparison of V100 and P100 Performance

| Machine | Tokenizer Time | Training Time | Inferrence Time | AUC Score |
| :---: | :---: | :---: | :---: | :---: |
| V100 | 0:34:41 | 1:29:41 | 0:14:14 | 0.96819 |
| P100 | 0:40:58 | 5:49:30 | 0:59:04 | 0.96817 |

The tokenizer runs 100% on CPU, although the V100 runs faster it is only a 17% reduction in tokenizing time.  

For training and inferrence however, the differences in the GPU capabilities in the two VMs is much greater, with the time reductions on the V100 of 74% and 75% respectively.  Accuracy of the models match to 4 decimal places which is as expected given the common random seeding values.

## I selected task A, to train the model on two epochs.  
see `BERT_classifying_toxicity_2_epoch.ipynb` for the details of the run. This was run on the V100 instance only in the interests of speed, but expanding the table above to include the epochs:

| Machine | Epochs | Tokenizer Time | Training Time | Inferrence Time | AUC Score |
| :---: | :---: | :---: | :---: | :---: | :---: |
| V100 | 1 | 0:34:41 | 1:29:41 | 0:14:14 | 0.96819 |
| V100 | 2 | 0:34:29 | 2:56:22 | 0:13:52 | 0.96692 |
| P100 | 1 | 0:40:58 | 5:49:30 | 0:59:04 | 0.96817 |

As expected, the training time was almost double the 1 epoch time, with other timings close to the 1-epoch run. Accuracy dropped by ~0.12%, small, but might show a small degree of overfitting.

That said, it chose a different most and least toxic message compared to the single epoch training, and although the probabilities of the two are likely very close, to my eye, the 2-epoch top choice was clearly the more toxic, if only due to its length, and the least toxic may also have been selected due to its brevity.  So, accuracy is slightly down, but the top and bottom selections seem better than the single epoch choices given the task.
