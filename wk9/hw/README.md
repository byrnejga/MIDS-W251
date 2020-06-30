Please submit the nohup.out file along with screenshots of your Tensorboard indicating training progress (Blue score, eval loss) over time. Also, answer the following (simple) questions:


## How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)
Started 16:17 UTC on Monday June 29

Ended: 20:38 UTC on Tuesday June 30

Total time: 28:21.  


## Do you think your model is fully trained? How can you tell?

## Were you overfitting?

## Were your GPUs fully utilized?
for the most part, yes. Utilization of all four GPUs are at 100% except for brief occasions when the utilization seems to dip, likely due to the end of a batch. 

## Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
I did monitor the network during training, and saw that eth0, the virtual network between the VMs was consistently running around 200MB/s in both directions. The stated speed of the network is 1Gbit/s, which with protocol overhead is around 100MBytes/s.  I am getting double that speed duplexed, so perhaps there is excess capacity on the virtual network I get to use, or there may be compression involved.

Either way, the 16 CPUs on both boxes do not seem to ever peak over an average of 25-30%, so we could have done this with an 8 CPU image with the same GPUs (if that image is available) and still not seen major performance hits.


## Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?

## How big was your training set (mb)? How many training lines did it contain?
The training set comprises of two tokenized files, one for English and the corresponding German records.  A total opf 1.88GB:

```
root@v100a:/data/wmt16_de_en# du -h  train.clean*shuff*tok
971M	train.clean.de.shuffled.BPE.32K.tok
976M	train.clean.de.shuffled.BPE_common.32K.tok
909M	train.clean.en.shuffled.BPE.32K.tok
915M	train.clean.en.shuffled.BPE_common.32K.tok
```
There are 4524868 lines in the training sample.
```
root@v100a:/data/wmt16_de_en# wc -l train.clean*shuff*tok
   4524868 train.clean.de.shuffled.BPE.32K.tok
   4524868 train.clean.de.shuffled.BPE_common.32K.tok
   4524868 train.clean.en.shuffled.BPE.32K.tok
   4524868 train.clean.en.shuffled.BPE_common.32K.tok
```

## What are the files that a TF checkpoint is comprised of?

## How big is your resulting model checkpoint (mb)?

## Remember the definition of a "step". How long did an average step take?

## How does that correlate with the observed network utilization between nodes?
