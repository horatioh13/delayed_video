# Long Duration Delayed Video Application

This python script is designed to display video feeds with an adjustable delay of up to 24 hours. The program acomplishes this through sequentially recording images and dynamically displaying them based on the time stamp that they were recorded, so the delay is completely accurate regardless of the read/write speed of the SSD and the FPS of the webcam being used to record images.  
The recorded images are stored on the ssd of the computer, not in RAM to allow for a very long delay, even on lightweight computers.  
