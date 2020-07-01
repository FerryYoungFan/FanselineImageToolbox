<a href="./GUI/Help/main_en.md"><font color=#437BB5><u>Back to Homepage</u></font></a>

---
# Magic Wand
Select surrounding pixels based on tone and color.  
<font color=#9C9642>Press SPACE to move and zoom in/out canvas in this mode.</font>

---
### Step 1
Well, this is not a very good method for selecting, but I still put it here.  
Click on the image, it will select the surroundings according to the tolerance you set.  
There are two tolerance sliders in RGB Channel:
* Upper Difference: Determine how "bright" a color can be considered as selection.
* Lower Differnece: Determine how "dark" a color can be considered as selection.

---
### Step 2
If you want to adjust the edge of the current selection, you can use the following sliders:
* Grow: Expand the edge of current mask (selection).
* Contract: Shrink the edge of current mask.
* Feather Edge: Smooth and feather the edge of current mask.

<font color=#40874A>You can fill small holes by applying grow and contract at the same time (morphological closing).</font>  
<br />
![Image](selection_edit_en.png)

---
### Step 3
You can now apply your current selection to the global selection by clicking the buttons on the right column:  
<br />
![Image](selection_apply_en.png)

---
<a href="./GUI/Help/main_en.md"><font color=#437BB5><u>Back to Homepage</u></font></a>
