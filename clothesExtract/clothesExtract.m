orig_img = imread('t4.jpg');
gray_img = rgb2gray(orig_img);
bw = im2bw(gray_img, 0.95);
edge_img = edge(bw, 'Canny');

mask = bwconvhull(edge_img);
Area = sum(mask(:)==1);

s  = regionprops(edge_img,'centroid', 'MajorAxisLength', 'MinorAxisLength');
centers = s.Centroid;
height = s.MajorAxisLength;
width = s.MinorAxisLength;
h_over_w = height / width

B = uint8(mask); 
Inew = orig_img.*repmat(B,[1,1,3]);

figure, imshow(Inew);
title('Union Convex Hull');
