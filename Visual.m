%Visualizer for Python processed data.


%reads from 3D data file
data = csvread('test3d.csv');

%splits into 3 arrays, one for each axis.
xlist = data(1,:);
ylist = data(2,:);
zlist = data(3,:);

%plots a scatter plot to represent data.
scatter3(xlist, ylist, zlist);
title('3D Scanner Visualization')
xlabel('X Distance (cm)');
ylabel('Y Distance (cm)');
zlabel('Z Distance (cm)');
axis([-60 60 -50 100 -50 100])

%reads from 2D data file
data2 = csvread('test2d.csv');

%splits into 2arrays, one for each axis.
xlist = data2(1,:);
ylist = data2(2,:);

%plots a scatter plot to represent data.
figure
scatter(xlist, ylist, 'filled');
title('2D Scanner Visualization')
xlabel('X Distance (cm)');
ylabel('Y Distance (cm)');
axis([-40 40 0 50])
