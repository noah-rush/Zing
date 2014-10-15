"""
Adapted from 
/** 
 * Synthesis 1: Form and Code
 * Riley Waves by Casey Reas (www.processing.org)
 * p. 151
 * 
 * Step 3, values are modified to create a new pattern. 
*/
"""
import numpy as np
from pyprocessing import *
from random import randint



def star(x, y, radius1, radius2, npoints):
    angle = TWO_PI / npoints;
    halfAngle = angle/2.0;
    beginShape();
    points = np.arange(0,TWO_PI,angle)
    for a in points:
      sx = x + cos(a) * radius2;
      sy = y + sin(a) * radius2;
      vertex(sx, sy);
      sx = x + cos(a+halfAngle) * radius1;
      sy = y + sin(a+halfAngle) * radius1;
      vertex(sx, sy);
    
    endShape(CLOSE);


    
size(1600, 1000)
background(240,240,240);
yellow = color(255,223,136);
gray = color(221,221,221);


for i in range(0,250):
    for j in range(0,250):

      onoff = randint(0,1);
      if onoff == 0:
       
        fill(yellow)
        stroke(yellow)
        pushMatrix()
        rad1 = randint(3,10)
        rad2 = rad1 * 70/30
        translate(i*width/250, j*height/250);
        rotate(0.95)
        star(0, 0, rad1, rad2, 5)
        popMatrix();
   
      else:
       
        pushMatrix()
        rad1 = randint(3,10)
        rad2 = rad1 * 70/30
        fill(gray)
        stroke(gray)
        translate(i*width/250, j*height/250);
        rotate(0.95)
        star(0, 0, rad1, rad2, 5)
        popMatrix();

save("static/images/stars.jpg")
  

   

 
