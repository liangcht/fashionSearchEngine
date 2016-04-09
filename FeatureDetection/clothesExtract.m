orig_img = imread('../sample_image/8386.jpg');
gray_img = rgb2gray(orig_img);
bw = im2bw(gray_img, 0.95);
edge_img = edge(bw, 'Canny');

mask = bwconvhull(edge_img);

mask_region = regionprops(mask,'BoundingBox', 'FilledImage');
bbMatrix = vertcat(mask_region.BoundingBox);

cropped_img = mask_region.FilledImage;
% figure, imshow(cropped_img);
r = regionprops(cropped_img(1:size(cropped_img, 1)/4, :), 'Area');

% chop off head
x_start = bbMatrix(2); 
if r.Area / ((size(cropped_img, 1)/4) * size(cropped_img, 2)) < 0.8
    for i = bbMatrix(2)+bbMatrix(4)/4:-1:bbMatrix(2)
        if sum(bw(round(i), bbMatrix(1):bbMatrix(1)+bbMatrix(3))) > bbMatrix(3)/2 
            x_start = i;
            break;
        end
    end
end
masked_img = imcrop(orig_img, [bbMatrix(1) x_start bbMatrix(3) bbMatrix(4)+bbMatrix(2)-x_start]);

bw = im2bw(rgb2gray(masked_img), 0.8);
w = size(bw, 2);
h = size(bw, 1);

if h / w > 2 % if it is full length picture
    % chop off legs
    A = false;
    len = 0;
    x_end = h;
    white_space_threshold = 18;
    % count white pixels between blacks, if more than
    % white_space_threshold, set as the bottom edge(x_end)
    for i = round(h/2):h
        for j = 1:w
            if bw(i, j) == false && A == false % not white
                A = true;
            end
            if bw(i, j) == true && A == true
                len = 0;
                for k = j:w
                    if bw(i, k) == false
                        j = k;
                        break;
                    end
                    len = len + 1;
                    if len > white_space_threshold
                        x_end = i;
                        break;
                    end
                end
                if x_end < h
                    break;
                end
            end
        end
        if x_end < h
            break;
        end
    end
    masked_img = imcrop(masked_img, [1 1 w x_end]);
end

figure, imshow(masked_img);
title('croped image');
