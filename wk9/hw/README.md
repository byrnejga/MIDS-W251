# Homework 9 - James Byrne


Please submit the nohup.out file along with screenshots of your Tensorboard indicating training progress (Blue score, eval loss) over time. Also, answer the following (simple) questions:


## How long does it take to complete the training run? (hint: this session is on distributed training, so it will take a while)
Started 16:17 UTC on Monday June 29

Ended: 20:38 UTC on Tuesday June 30

Total time: 28:21.  


## Do you think your model is fully trained? How can you tell?

I am not convinced that the model is fully trained - at least not as well as it might be possible - the eval loss function was still trending downward (1.6 to 1.58 over the last 10,000 records.), thought the rate was small, and more training may be too costly for only a marginal improvement.

## Were you overfitting?
It does not seem so. The train_loss was continuing to trend downward at the end (see detail chart), but I would have expected the eval_loss to start trending up in the case of overfitting. This would be due to the model being less generalizable and therefore less able to correctly translate the evaluation data set. 

## Were your GPUs fully utilized?
For the most part, yes. Utilization of all four GPUs remained at 100% except for brief occasions when the utilization dips for a second or so at the start of a new batch. 

## Did you monitor network traffic (hint: apt install nmon ) ? Was network the bottleneck?
I did monitor the network during training, and saw that eth0, the virtual network between the VMs was consistently running around 200MB/s in both directions. The stated speed of the virtual network is 1Gbit/s, which with protocol overhead is equal to around 100MBytes/s.  I am getting double that speed duplexed, so perhaps there is excess capacity on the virtual network I get to use, or there may be compression involved.

The 16 CPUs on nether box ever peaked over an average usage of 25-30%, so we could have done this with an 8 CPU image with the same GPUs (if that image is available) and still not seen major performance hits, the CPUs therefore are not the limiting factor

Monitoring the load on the GPUs, they were consistently at 100% except for small dips as a new batch is loaded, and larger ones during the evaluations. Had the network bandwidth been the bottleneck, I would have expected to see nvidia-smi to show less than 100% during batch processing while it waited on data, this was not the case, and monitoring the network did show significant data transfer ongoing during training.

On this evidence, it appears that the GPU capacity is the limiting factor to the speed of training.


## Take a look at the plot of the learning rate and then check the config file. Can you explan this setting?
The following portion of the `base_params` configuration stucture sets up the learning rate approach:
```
  "lr_policy": transformer_policy,
  "lr_policy_params": {
    "learning_rate": 2.0,
    "warmup_steps": 8000,
    "d_model": d_model,
  },
```
The `transformer_policy` sets up a Noam style warmup and lr decay pattern. 2.0 is the initial learning rate.  The model will increase learning rate linearly for the first 8000 steps and then revert to the Noam formula described in the _Attention is All You Need_ paper we studied a few weeks ago.

## How big was your training set (mb)? How many training lines did it contain?
The training set comprises of two tokenized files, one for English and the corresponding German records.  A total of 1.88GB:

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
There is a master `checkpoint` file that lists all the checkpoints then a set of 3 or more files for each chekpoint. For the checkpoint taken at the end of the run, the following files were created:
```
model.ckpt-50000.data000000-of-000001  # May be multiple of these files depending on size and configuration
model.ckpt-50000.index
model.ckpt-50000.meta
```

## How big is your resulting model checkpoint (mb)?
Each set of three files is a total of 865MB.

## Remember the definition of a "step". How long did an average step take?
Training took a total of 28h, 21m, or 102,060 seconds.  Dividing in the 50,000 steps gives us an average time of 2.04 seconds per step. Note that this includes the time taken to initialize the model, and 6 evaluation runs, but they are negligible in duration compared with the total time taken. 

## How does that correlate with the observed network utilization between nodes?
I am not 100% sure of the intent of this question, but I am going to guess that it involves how and what data passes between the nodes in a Hovorod cluster.  When using Hovorod, each GPU gets its own worker thread on the GPU's host machine.  Each worker randomly selects its own minibatch of (256/4)=64 records from the training data set. The data itself can be obtained locally - why we have to put the files on both nodes - so never goes across the connection between them. When upgrading the gradients however, all four workers and the gradients and parameters loaded in their respective GPUs are kept in step, so at a minimum a set of 60,880,896 trainable parameters need to pass between the nodes at least four times, once per worker from remote to master to calculate the common gradients and once per remote worker (in this case 2 remote workers) to push back the full, matched set of new parameters.  Mixed precision mode uses a mix of 16- and 32-bit floats for calculations, so each set of parameters will be between 122 and 244MB of total data, or between 244MB and 488MB of data flowing in each direction per step.  

With a step time of 2s, this works out to between 122MB/s and 244MB/s duplex not accounting for protocol overheads and other communication done by Hovorod. This lines up with the ~200MB/s duplex rates I observed during training. 


