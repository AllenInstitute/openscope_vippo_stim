%% Setup
% Assume that presentation is on a screen of 1920 x 1200
%Generation of frames at 960 x 540
%Padding chosen such that warping does not leave any actual locations on
%the screen as completely unused, like a dead pixel
FullScreen=[540 960]; % Will generate the files at this resolutionFullScreen=[540 960];width or x =960
PixelPad_eachSideX=188;%On each side, 192 here leaves dead pixels
PixelPad_eachSideY=40;%On each side, 40 here leaves dead pixels
ActualXRange=(PixelPad_eachSideX+1) : (960-PixelPad_eachSideX);
ActualYRange=(PixelPad_eachSideY+1) : (540-PixelPad_eachSideY);
%%
FrameRate=60;
WidthInDeg=15;
ScaleForNarrow_Wide=1;
SpeedScaling=1; % make this 4, so that the pillar is 4 times slower
BaseSpeed=2 * FrameRate; %60 is the frame rate, 2 sec for 1 direction travel

ContrastFlip=1;
BoundaryConditionTypes=1;
movementType='loop';

NFramesWithoutVanish=BaseSpeed;

BarWidth=round(WidthInDeg*ScaleForNarrow_Wide/180*length(ActualXRange)); % For left right
%2second stimulus
switch BoundaryConditionTypes
    case 1 % All of the pillar is always visible
        BarPositions=linspace(ActualXRange(1)+BarWidth/2,...
            ActualXRange(end)-BarWidth/2,BaseSpeed*SpeedScaling);
    case 2 %Pillar goes to the edge till exactly that it gets exactly and fully absorbed by the edge
        PixelsPerFrame=(length(ActualXRange)-BarWidth)/(BaseSpeed*SpeedScaling);
        AdditionalFramesNeeded=round(2*BarWidth/PixelsPerFrame);
        BarPositions=linspace(ActualXRange(1)-BarWidth/2,...
            ActualXRange(end)+BarWidth/2,BaseSpeed*SpeedScaling + AdditionalFramesNeeded);
    case 3 % Pillar vanishes for a bit on the sides
        N_BarWidthsToAdd_EachSide=3;
        PixelsPerFrame=(length(ActualXRange)-BarWidth)/(BaseSpeed*SpeedScaling);
        AdditionalFramesNeeded=2*N_BarWidthsToAdd_EachSide*round(BarWidth/PixelsPerFrame);
        BarPositions=linspace(ActualXRange(1)-N_BarWidthsToAdd_EachSide*BarWidth,...
            ActualXRange(end)+N_BarWidthsToAdd_EachSide*BarWidth,BaseSpeed*SpeedScaling + AdditionalFramesNeeded);
end
aa=zeros(length(BarPositions),FullScreen(1),FullScreen(2));
for i=1:length(BarPositions)
    aa(i,1:end,round(BarPositions(i)-BarWidth/2:BarPositions(i)+BarWidth/2))=255;
end
aa=uint8(aa);
switch movementType
    case 'loop'
        bb=[aa;aa(fliplr(1:size(aa,1)),:,:)];
    case 'oneway'
        bb  =aa;
end
if ContrastFlip
    bb=255-bb;
end
NameCurrent=['SAC_Wd' num2str(WidthInDeg*ScaleForNarrow_Wide) ...
    '_Vel' num2str(BaseSpeed*SpeedScaling/FrameRate) ...
    '_Bndry' num2str(BoundaryConditionTypes) ...
    '_Cntst' num2str(ContrastFlip) ...
    '_' movementType ];
writeNPY(bb,[NameCurrent '.npy']);
%% Up down pillar now
FrameRate=60;
WidthInDeg=15;
ScaleForNarrow_Wide=1;
SpeedScaling=1; % make this 4, so that the pillar is 4 times slower
BaseSpeed=2 * FrameRate; %60 is the frame rate, 2 sec for 1 direction travel

ContrastFlip=0;
BoundaryConditionTypes=1;
movementType='loop';

NFramesWithoutVanish=BaseSpeed;

BarWidth=round(WidthInDeg*ScaleForNarrow_Wide/180*length(ActualYRange)); % For left right
%2second stimulus
switch BoundaryConditionTypes
    case 1 % All of the pillar is always visible
        BarPositions=linspace(ActualYRange(1)+BarWidth/2,...
            ActualYRange(end)-BarWidth/2,BaseSpeed*SpeedScaling);
    case 2 %Pillar goes to the edge till exactly that it gets exactly and fully absorbed by the edge
        PixelsPerFrame=(length(ActualYRange)-BarWidth)/(BaseSpeed*SpeedScaling);
        AdditionalFramesNeeded=round(2*BarWidth/PixelsPerFrame);
        BarPositions=linspace(ActualYRange(1)-BarWidth/2,...
            ActualYRange(end)+BarWidth/2,BaseSpeed*SpeedScaling + AdditionalFramesNeeded);
    case 3 % Pillar vanishes for a bit on the sides
        N_BarWidthsToAdd_EachSide=3;
        PixelsPerFrame=(length(ActualYRange)-BarWidth)/(BaseSpeed*SpeedScaling);
        AdditionalFramesNeeded=2*N_BarWidthsToAdd_EachSide*round(BarWidth/PixelsPerFrame);
        BarPositions=linspace(ActualYRange(1)-N_BarWidthsToAdd_EachSide*BarWidth,...
            ActualYRange(end)+N_BarWidthsToAdd_EachSide*BarWidth,BaseSpeed*SpeedScaling + AdditionalFramesNeeded);
end
aa=zeros(length(BarPositions),FullScreen(1),FullScreen(2));
for i=1:length(BarPositions)
    aa(i,round(BarPositions(i)-BarWidth/2:BarPositions(i)+BarWidth/2),1:end)=255;
end
aa=uint8(aa);
switch movementType
    case 'loop'
        bb=[aa;aa(fliplr(1:size(aa,1)),:,:)];
    case 'oneway'
        bb  =aa;
end
if ContrastFlip
    bb=255-aa;
end
NameCurrent=['UD_Wd' num2str(WidthInDeg*ScaleForNarrow_Wide) ...
    '_Vel' num2str(BaseSpeed*SpeedScaling/FrameRate) ...
    '_Bndry' num2str(BoundaryConditionTypes) ...
    '_Cntst' num2str(ContrastFlip) ...
    '_' movementType ];
writeNPY(bb,[NameCurrent '.npy']);%% Disk and Ring now
%%
[x,y]=meshgrid(ActualXRange,ActualYRange);
Center=[270.5,480.5];
Dist=sqrt((x-Center(2)).^2 + (y-Center(1)).^2);
RadiusVector=linspace(floor(min(Dist(:))),ceil(max(Dist(:))),120);
RadiusVector2=linspace(floor(min(Dist(:)))-BarWidth,ceil(max(Dist(:)))-BarWidth,120);
aa=zeros(120,FullScreen(1),FullScreen(2));
for i=1:120
    Inside=(Dist < RadiusVector(i))  & ( Dist > RadiusVector2(i)) ;
    %Inside=( Dist < RadiusVector(i)) ;
    temp=uint8(Inside*255);
    aa(i,ActualYRange,ActualXRange)=temp;
end
aa=uint8(aa);
bb=[aa;aa(fliplr(1:120),:,:)];
%bb=255-bb;
writeNPY(bb,'Ring_Wd15_Vel2_Bndry1_Cntst0_loop.npy');

%% Fit the natural movies to this window
BigWindow=zeros(240,540,960);
aa=readNPY('natmovie_CricketsOnARock_480x270.npy');
[x,y]=meshgrid(ActualXRange,ActualYRange);
[x2,y2]=meshgrid(linspace(ActualXRange(1),ActualXRange(end),size(aa,3)),...
    linspace(ActualYRange(1),ActualYRange(end),size(aa,2)));
for i=1:size(aa,1)
    for clr=1:3
        BigWindow(i,round(ActualYRange),round(ActualXRange),clr)=interp2(x2,y2,double(squeeze(aa(i,:,:,clr))),x,y);
    end
end
BigWindow=uint8(BigWindow);
writeNPY(BigWindow,'natmovie_CricketsOnARock_540x960Full_584x460Active.npy');
%% I got some video(s) later, so fix them too
Vd=VideoReader('CSP_SnakeOnRoad.avi');
Vd.NumFrames
temp=read(Vd,[1 240]);
montage(temp)
size(temp)
temp=permute(temp,[4 1 2 3]);
clc
[x2,y2]=meshgrid(linspace(ActualXRange(1),ActualXRange(end),size(temp,3)),...
linspace(ActualYRange(1),ActualYRange(end),size(temp,2)));
[x,y]=meshgrid(ActualXRange,ActualYRange);
bb=zeros(240,540,960,3);
for i=1:240;for clr=1:3
bb(i,ActualYRange,ActualXRange,clr)=interp2(x2,y2,double(squeeze(temp(i,:,:,clr))),x,y);
end
end
bb=uint8(bb);
for i=1:120
imshow(squeeze(bb(i,:,:,:)));
pause(0.003)
end
writeNPY(bb,'natmovie_SnakeOnARoad_540x960Full_584x460Active.npy');
%% Curl now, thoda jugaad ahe
aa=readNPY('SAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
Angles=linspace(1.5,180,120);Angles=fliplr(Angles);
aa1=squeeze(aa(60,:,:));aa1=repmat(aa1,10,1);
I3=zeros(120,540,960);I3=uint8(I3);
for i=1:120
I2=imrotate(aa1,Angles(i));
Sz=size(I2);
%{
IDx=Sz(1)/2-271 : Sz(1)/2+270;IDx=IDx(IDx>0 & IDx<Sz(1));IntersectX=mintersect(1:540,round(IDx));
IDy=Sz(2)/2-481 : Sz(2)/2+480;IDy=IDy(IDy>0 & IDy<Sz(2));IntersectY=mintersect(1:960,round(IDy));
%}
com=round(centerOfMass(I2));
try
I3(i,:,:)=I2(com(1)-270:com(1)+269,com(2)-480:com(2)+479);
catch
I3(i,:,:)=I2(com(1)-270:com(1)+269,com(2)-482:com(2)+477);
end
imshow(squeeze(I3(i,:,:)))
pause(0.003);
end
writeNPY(I3,'curl_Wd15_Vel2_Bndry1_Cntst0_oneway.npy');

%% Use a static image file and for each frame of a bar of light, multiply it with that static image, to get a rich texture
aa=readNPY('SAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
temp=zeros(540,960,3);
ids=mod(1:540,30)>15;
temp(ids,:,2)=255;
temp=uint8(temp);
bb=zeros(240,540,960,3);
for i=1:240
for clr=1:3
    bb(i,:,:,clr)=squeeze(aa(i,:,:)).*squeeze(temp(:,:,clr));
end
end
bb=uint8(bb);
writeNPY(bb,'GreenSAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
%%
aa=readNPY('SAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
temp=zeros(540,960,3);
ids=mod(1:540,30)>15;edges=find(diff(ids)~=0);
bb=zeros(240,540,960,3);
for i=1:240
    for e=2:2:length(edges)-1
        rnd=rand(3,1);
        for clr=1:3
            temp(edges(e):edges(e+1),:,clr)=rnd(clr);
        end
    end
    bb(i,:,:,:)=temp.*double(squeeze(aa(i,:,:)));
    imshow(squeeze(uint8(bb(i,:,:,:))));
end
bb=uint8(bb);
writeNPY(bb,'Disco2SAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
%% Not using this currently
aa=readNPY('SAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
temp=imread('songs-of-rainbow.jpg');
[x,y]=meshgrid(1:960,1:540);
[x2,y2]=meshgrid(linspace(1,960,552),...
linspace(1,540,406));
imshow(temp)
bint=zeros(240,540,960,3);
for i=1:240
for clr=1:3
    bint(i,:,:,clr)=uint8(double(squeeze(aa(i,:,:))).*squeeze(interp2(x2,y2,double(squeeze(temp(:,:,clr))),x,y)));
end
i
end
writeNPY(bint,'DiscoSAC_Wd15_Vel2_Bndry1_Cntst0_loop.npy');
