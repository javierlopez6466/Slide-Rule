# Slide-Rule
Requirements: PIL, Computer Modern Fonts (ttf)

"Sticker Cut" file generates sticker image ready to be scaled to 677.33ppi in Gimp and then print and cut in Silhouette.

"Laser Cut" file generates png images of the frame alone (Scale Cutting Pattern) and the frame with the scales fully printed inside (Scale Etching Pattern). Additionally, it generates a Diagnostic Print of all the scales alone. Internally, the program can be modified to print pink lines indicating where the metal pieces would go (just un-comment the metalcutoffs() in the rendering section) and you may select whether to render, run diagnostic, or both.

The excel files helps convert between pixels and inches / millimeters
