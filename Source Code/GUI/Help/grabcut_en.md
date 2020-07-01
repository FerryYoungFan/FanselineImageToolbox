<a href="./GUI/Help/main_en.md"><font color=#437BB5><u>Back to Homepage</u></font></a>
# Grabcut
An interactive select method for selecting objects automatically.  
<font color=#9C9642>Press SPACE to move and zoom in/out canvas in this mode.</font>

---

### Step 1
Draw a rectangle around the skin (object) you want to process (ROI).  
If you want to reselect the area later, just click on "ROI Select" button and frame select again.  
You will be waiting for <font color=#9C9642>several seconds </font> before the result shows up.  
The area that has been selected currently will be marked in red.  
Grabcut Iteration: higher value will increase the select precision as well as the <font color=#B54643>computing time</font>.  
<br />
![Image](grabcut_frame.png)

---
### Step 2
The selection maybe not perfect. Then you should mark the skin and the background manually.  
Firstly, click on the <font color=#B54643>Subtract(-)</font> button and mark the background.  
Reminder: You can change the brush size before marking.  
<br />
![Image](grabcut_subtract.png)

---
### Step 3
Secondly, click on the <font color=#40874A>Add(+)</font> button and mark the skin (foreground).  
<br />
![Image](grabcut_add.png)

---
### Step 4
If you want to adjust the edge of the current selection, you can use the following sliders:
* Grow: Expand the edge of current mask (selection).
* Contract: Shrink the edge of current mask.
* Feather Edge: Smooth and feather the edge of current mask.

<font color=#40874A>You can fill small holes by applying grow and contract at the same time (morphological closing).</font>  
<br />
![Image](selection_edit_en.png)

---
### Step 5
You can now apply your current selection to the global selection by clicking the buttons on the right column:  
<br />
![Image](selection_apply_en.png)

---
<a href="./GUI/Help/main_en.md"><font color=#437BB5><u>Back to Homepage</u></font></a>
