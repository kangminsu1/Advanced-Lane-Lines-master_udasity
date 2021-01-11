# Advanced-Lane-Lines-master_minsu
#### The code for project is in advance_lane_dectection.ipynb. The other notebook is for parameter fine-tune.

## Camera Calibration
#### 1. Have the camera matrix and distortion coefficients been computed correctly and checked on one of the calibration images as a test?

The code for this step is contained in the third code cell of the IPython notebook (advance_lane_dectection.ipynb).

I read in all the chessboard image for undistortion. Assuming all the chessboard are fixing at the plane where z=0, objpoints are filled with (x,y,0), or simply (x,y) where x,y is the coordinate index from (0,0) to (8,5) since there are 9x6 corners should be found on the chessboard. Then, imgpoints are filled by findChessboardCorners function on the chessboard image. For each image with ret=True returned by findChessboardCorners (17 out of 20), the objpoints and imgpoints are constructed and serve as input to calibrateCamera to get the parameters to undistort images.

There is the comparison between the original and undistort image I get from calibration1.jpg (saved as undistorted_calibration1.jpg in output_images/)  

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/comparison_undistort.png)

## Pipeline (single images)

#### 1. Has the distortion correction been correctly applied to each image?

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this
one: (saved as undistorted_test1.jpg in output_images/)

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/undistort_test1_comparison.png)

#### 2. Has a binary image been created using color transforms, gradients or other methods?

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this
one: (saved as sobeled_test2.jpg in output_images/)
One thing need to mention is that I apply grayscale to image first, then use single that single channel to do sobel gradient. While, when I play that method on the road that have a gray road surface (other than black surface) the yellow becomes unclear since after grayscale it looks similar to road surface. Thus, I use RGB channels with sobel, then, I defined a function named shrink_image_over_thresh() to shrink them to one channel (e.g, (1,0.9,0) -> 1)  

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/sobel_comparison.png)

* The following is modified after first submission:  
To achieve better result, I use use color selection combined with sobel magnitude, the code lies in `Yellow & White Lane Detection` section. I tried to detect yellow lane line and white lane line separately (before I always trying to detect them both in one shot, which generates worse result), and then OR the two binary images.
![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/color_hsv_selection.png)


#### 3. Has a perspective transform been applied to rectify the image?

To demonstrate this step, I will describe how I apply the distortion correction to one of the test images like this
one: (saved as perspective_straight_lines1.jpg in output_images/)
The code for my perspective transform is includes a function called perspective_transform() , which appears in the first two cell under "Perspective Transform" section. This function takes an image and a transform matrix M as input. M is defined by src and dst points through cv2.getPerspectiveTransform(). For src and dst points, dst is what I suppose it should be after transform, so that a rectangle with coordinate [[400,625],[1035,625],[400,200],[1035,200]] ; on the other end, src points is generated from "test_images/straight_lines1.jpg", I use my image software manualy measured as [[255,678],[1053,678],[556,475],[729,475]] (I suppose those lane line as indicated is straight and pick two pairs each from same horizontal value.)

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/perspective_comparison.png)

#### 4. Have lane line pixels been identified in the rectified image and fit with a polynomial?
Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/polyfit_demonstration.png)

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I use the code provided in course 35 to calculate the curvation in both pixel space and real world.  
The code responsed is settled in "Calculate Curvation" section (first 2 code pieces respectively). I have changed this part, please see section 7 below.

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/drawback_on_road_demonstration.png)

#### 7. Curvation and Center Off Calculation.
I calculate the curvation and center off position using the functions under `Calculate Curvation and Center Off` section in notebook. The curvation is calculated according to the course. And the center off position is calculated by compare the position of middle of the end of left and right curve to the middle of screen (where I suppose to be the center of the real car position).  

### 8. Finally the pipeline for processing image with curvation and center off info output looks like:

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/final_processing_image.png)


## Pipeline (video)
#### 1. Provide a link to your final video output. Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).  
Here's a [link to my video result](https://raw.githubusercontent.com/qitong/SDC-P4/master/project_out.mp4) in repo.
And here's the same one on youtube:
[![alt Project_output](https://img.youtube.com/vi/286CATfcGU8/0.jpg)](https://youtu.be/286CATfcGU8)

## Discussion
#### 1. Briefly discuss any problems / issues you faced in your implementation of this project. Where will your pipeline likely fail? What could you do to make it more robust?  

I implement the project mainly follow what I learned in P4 courses. 
At first time, I use sobel gradient to detect the lane line solely. Even I tuned the parameters several times, it will fail where there is tree shadow on shallow color road surface (e.g, 39~40s) which is the most crucial problem in my case. After I delving into that problem, I get the binary image as follow:  

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/pure_sobel_binary.png)

The shadow is falsed categorized as spot on the road. I tried to remove the shadow on the road simply by using HSV Value Channel as threshold (rather than using HLS, I also have a HLS code piece in it) in "HSV threshold to remove shadow" section.

![alt tag](https://raw.githubusercontent.com/qitong/SDC-P4/master/output_images/with_HSV_binary.png)

After doing that tuning, I got better result.

It is generally not robust though. I tried with challenge video, I think it cannot distinguish the line-shaped stuff on the road and curb shadow if it is to close to the lane line. Maybe the first one can be elminated by a more sophisticated design of region of interest and second one can be done by a good design of shadow removal algorithm instead of simply using a threshold on Value channel.
Also, when it passes the turn there is shake on the driveable area, I think I need to use smooth method to optimize that when I have time.
