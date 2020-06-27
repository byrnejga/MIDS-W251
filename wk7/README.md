## Homework 7 - Neural face detection pipeline

#### Describe your solution in detail. What neural network did you use? What dataset was it trained on? What accuracy does it achieve?

The network I used is provided by JK Jung at https://jkjung-avt.github.io/tensorrt-mtcnn/.

Jung built the tensor demo based on the MTCNN  created by K Zhang et al (https://github.com/kpzhang93/MTCNN_face_detection_alignment.git). 

The approach addresses both face detection (which is what we are looking for) and fafe feature detection - eyes, nose, ends of mouth etc. that we don't need, but will see displayed when the script runs.  

The approach uses three convolutional neural networks cascaded to ensure best performance.  The first is a shallow network that can rapidly produces candidate face frames which are assessed by the second, more complex network that rejecs a large number of the non-face frames, limiting the work needed by the third, still more complex CNN that refines the result and generates the facial landmark locations.

I replaced the week-3 face detector script with a modified version of Jung's script, adding primarily the encoding and transmission of detected faces over MQTT to the rest of the network.

Jung's script included code to show the video capture with the recognized face and facial landmarks which I extended to show the cropped frame being sent to the cloud.

I chose to not collapse the image to grey scal, which may have improved performance.

The only other change I needed to make to the wk3 solution was to update the IP address of the Jetson MQTT forwarder that communicates with the cloud service. 

Updated items are  at https://github.com/byrnejga/MIDS-W251/tree/master/wk7, and the unchanged ones at https://github.com/byrnejga/MIDS-W251/tree/master/wk3.


The network was trained using datasets from :
_S. Yang, P. Luo, C. C. Loy, and X. Tang, WIDER FACE: A Face Detection
Benchmark. arXiv preprint arXiv:1511.06523.
V. Jain, and E. G. Learned-Miller, FDDB: A benchmark for face detection
in unconstrained settings, Technical Report UMCS-2010-009, University
of Massachusetts, Amherst, 2010.
B. Yang, J. Yan, Z. Lei, and S. Z. Li, Convolutional channel features, in
IEEE International Conference on Computer Vision, 2015, pp. 82-90._


#### Does it achieve reasonable accuracy in your empirical tests? Would you use this solution to develop a robust, production-grade system?

During my testing I did not see any incorrect detections, though it did recognize non-human faces just as well, including a magazine cover drawing and a bobble head shown to the camera. 

The source paper puts the accuracy fo detection over 95%, and I have no reason to question this. 

#### What framerate does this method achieve on the Jetson? Where is the bottleneck?

I was able to get a consisitant framerate of around 6.5 fps.  The bottleneck appears to be the JSON encoding and communciation with mqtt. Using the unmodified script on the Jetson bare-metal I was able to consistently get 7.7 fps or more.  

#### Which is a better quality detector: the OpenCV or yours?

I hesitate to call this detector mine, but it appears to be much better at detecting faces at multiple angles, and much more reliably, even when not against a block colour background.

_Citation_

@article{7553523,
    author={K. Zhang and Z. Zhang and Z. Li and Y. Qiao}, 
    journal={IEEE Signal Processing Letters}, 
    title={Joint Face Detection and Alignment Using Multitask Cascaded Convolutional Networks}, 
    year={2016}, 
    volume={23}, 
    number={10}, 
    pages={1499-1503}, 
    keywords={Benchmark testing;Computer architecture;Convolution;Detectors;Face;Face detection;Training;Cascaded convolutional neural network (CNN);face alignment;face detection}, 
    doi={10.1109/LSP.2016.2603342}, 
    ISSN={1070-9908}, 
    month={Oct}
}
