%read data example: Import columns as column vectors 
X = csvread('ttest.csv');


xlist = data(1,:);
ylist = data(2,:);
zlist = data(3,:);


scatter3(xlist, ylist, zlist);
title('3D Scanner Visualization')
xlabel('distance (cm)');
ylabel('distance (cm)');
zlabel('distance (cm)');