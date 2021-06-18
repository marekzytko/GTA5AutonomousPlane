# GTA5AutonomousPlane

GTA5AutonomousPlane is small project that allows autonomous aircraft control in Grand Theft Auto 5

![](https://i.imgur.com/U3QcEoV.jpg)

### Recording data
In order to start training your neural net model, you need to record frames and keys used to steer aircraft. To do this, just open "getData.py" script and follow instructions

### Training and testing neural net
To train model based on recorded data, simply run "createModel.py". Training time depends on computing power of your machine and whether you want to use CPU or GPU Cuda cores.

If you want to try autonomous steering, open "testModel.py" and follow instructions!
Have fun!


### Neural net architecture:

![](https://i.imgur.com/EwcnpzR.png)



Inspired by Sentdex project - GTA5 autonomus car driving series
https://github.com/Sentdex/pygta5
