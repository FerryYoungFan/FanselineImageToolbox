# Basic for Beginners

---
* <a href="./GUI/Help/about_en.md"><font color=#437BB5><u>About this software</u></font></a>
* Mouse wheel: zoom in/out.
* Space key: move canvas (when in editing mode).
* Try to select skin (make a mask) before editing it.

<br />

# Main Window

---
## Left Column

---
### 1. Settings & Help
You can change language, set max undo steps here.  
Reminder:
* Language changing takes effect after restarting this software.
* Larger undo steps <font color=#B54643>requires more memory</font>.

---
### 2. Compare
Compare the original image with the current image.  
You can also hide the mask view by this button.

---
### 3. Show Mask
Switch between mask view and masked image.  
You can check up your global mask (selection) by this button.  
Global mask will be marked in purple.

---
### 4. Grabcut
An interactive select method for selecting objects automatically.  
<a href="./GUI/Help/grabcut_en.md"><font color=#437BB5><u>See details here</u></font></a>

---
### 5. Color Range
Select all pixels within the HSV color range.  
Auto skin select methods are also provided.  
<a href="./GUI/Help/color_range_en.md"><font color=#437BB5><u>See details here</u></font></a>

---
### 6. Magic Wand
Select surrounding pixels based on tone and color.  
<a href="./GUI/Help/magic_wand_en.md"><font color=#437BB5><u>See details here</u></font></a>

---
### 7. Select Tools
Some basic select tools for selecting pixels based on shapes.  
<a href="./GUI/Help/select_tools_en.md"><font color=#437BB5><u>See details here</u></font></a>

---

### 8. Adjust Selection
Adjust the edge and opacity of global mask (selection).  
<a href="./GUI/Help/adjust_selection_en.md"><font color=#437BB5><u>See details here</u></font></a>

---
### 9. Select Inverse
Invert global selection, change the unselected areas into selected areas.

---
### 10. Deselect All
Clear all selection, then all of the filters will take effect on the whole image.

---
### 11. Undo Mask (Ctrl+Shift+Z)
Reverses the last global mask selection.

---
### 12. Redo Mask (Ctrl+Shift+Y)
Recover the undone global mask.

---
## Right Column

---
### 1. Image Histogram
Shows brightness and tonal distribution in the current image.

---
### 2. Beeswax (Filter)
A special filter designed by Fanseline for leg/arm hair removal.  
<a href="./GUI/Help/beeswax_en.md"><font color=#437BB5><u>See details here</u></font></a>

---
### 3. Smooth Skin (Filter)
A bilateral filter designed for skin smoothing and whitening.  
<font color=#B54643>Keep blur diameter low to increase processing speed.</font>

---
### 4. Glow Blur (Filter)
A Gaussian filter designed for adding glow effect.

---
### 5. Classic Filters
Classic image filter sets. Can be used for blur and sharpen images.

---
### 6. Adjust Color
Adjust image brightness, tone and saturation.

---
### 7. Inpaint
Remove the stains and spots from the image.

---
### 8. Load Image
Open a new image to process.

---
### 9. Save Image
Save your current work as an image.

---
### 10. Undo (Ctrl+Z)
Reverse the last changing on image.

---
### 11. Redo (Ctrl+Y)
Recover the undone on image.