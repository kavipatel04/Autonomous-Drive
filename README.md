# AutonomousDrive
Using OpenCV Pre-Image Processing Techniques to find lanes, and coral ai for car and lane detection. 
<br>
<h2>Instructions</h2>
The file named magical file contains all the heavy processing techniques needed to filter out the lane lines from the video stream.
Currently, OpenCV is reading frames from a file called "TrimmedVid.mp4". Unfortunately this file couldn't upload due to issues with file sizes. 
If you want to use this file for actual production, you will have to change the OpenCV video source to read frames from your camera

<h2>Poor FPS from RPi</h2>
If you're experiencing laggy frames processing from a RPi. Fear Not! <br>
In this git repo, there is a server and client file which can be set up in a way such that users can connect the pi to another computer where 
the frames will be processed and displayed. In this set up the pi will only be used as a camera server. <br>

If you have any questions about this poor documentation (sorry, I was so excited about the project itself I didn't have much time to document)
please feel free to contact me at kavipatel@kavipatel.xyz! 
