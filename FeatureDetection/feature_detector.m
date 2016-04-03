function feature_detector (in_dir, out_dir)
%in_dir = '/Users/cyan/GitHub/fashionSearchEngine/amazon/crawlImages/';

fnames = dir(fullfile(in_dir, '*.jpg'));
fileNames = {fnames.name};

for i = 1:size(fileNames,2)
    im = imread(fullfile(in_dir, fileNames{i}));
    hog = extractHOGFeatures (im); 
    lbp = efficientLBP (im); 
    
    crop = strfind(fileNames{i}, '.jpg');
    namestring = fileNames{i} (1: crop-1); 
    num = str2num (namestring); 
    saved = sprintf ('%d.mat', num);
    mkdir('hog');
    mkdir('lbp');
    hogSave = strcat (out_dir, 'hog/', 'hog', saved);
    lbpSave = strcat (out_dir, 'lbp/', 'lbp', saved);
    save (hogSave, 'hog');
    save (lbpSave, 'lbp'); 
end
