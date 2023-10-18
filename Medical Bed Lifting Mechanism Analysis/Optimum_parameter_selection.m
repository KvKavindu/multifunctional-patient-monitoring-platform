%5.95,7.37
l1=420;
l2=200;
d1=415;
d2=200;
l3=sqrt(d1^2+d2^2);
l4=370;
l5=450;
d2_to_mattressSurface=250;
Hmin=600;
Hmax=1000;
groundTol5axis=290;
Ycmin=Hmin-groundTol5axis-d2_to_mattressSurface;
Ycmax=Hmax-groundTol5axis-d2_to_mattressSurface;

calc_start=0;
min_h=0;
max_h=0;
max_l=0;
min_l=0;
prev_called=0;

ycRange=Ycmin:Ycmax-1;
%ycRange=flip(ycRange);
d2range=1:400;%225:226;%
l2range=1:400;%236:237;%

Yc=Ycmin;

Y=zeros(length(d2range),length(l2range));
X=zeros(length(d2range),length(l2range));

theeta1=zeros(1,Ycmax-Yc);
theeta2=zeros(1,Ycmax-Yc);
theeta3=zeros(1,Ycmax-Yc);
theeta4=zeros(1,Ycmax-Yc);
theeta3new=zeros(1,Ycmax-Yc);
theeta4new=zeros(1,Ycmax-Yc);
negtheeta1=zeros(1,Ycmax-Yc);
postheeta4new=zeros(1,Ycmax-Yc);

obt_elevation=0;
obt_horizontal_deviation=0;

for j=1:length(d2range)
    d2=d2range(j);
    for k=1:length(l2range)
        l2=l2range(k);
        min_h=0;
        max_h=0;
        prev_called=0;
        
        for i=1:length(ycRange)
            calc_start=1;
            Yc=ycRange(i);
            l3=sqrt(d1^2+d2^2);
            theeta3(i)=acos(d1/l3);
            theeta4(i)=pi-asin((Yc-(l3*sin(theeta3(i))))/l4);
            
            Xc=l5+l3*cos(theeta3(i))-sqrt(l4^2-(Yc-l3*sin(theeta3(i)))^2);
            
            A1=Xc;
            B1=Yc;
            C1=(l1^2-l2^2+Xc^2+Yc^2)/(2*l1);
            
            A4=Xc-l5;
            B4=Yc;
            C4=(l4^2+l5^2-l3^2-(2*Xc*l5)+Xc^2+Yc^2)/(2*l4);
            
            if (A1^2+B1^2-C1^2)<0
                %disp("Maximum limit reached, Limit is : "+Yc)
%                 Y(j,k)=Yc;
%                 X(j,k)=Xc;
                calc_start=0;
                %break;
                
            elseif (Xc>525) || (Xc<375)
                calc_start=0;
                %break;
            elseif (theeta4(i)>(pi+12*pi/180))
                calc_start=0;
                %break;
            end
            
            if (calc_start==1)
                
                theeta1(i)=2*atan((-B1+sqrt(A1^2+B1^2-C1^2))/(-A1-C1));
                negtheeta1(i)=2*atan((-B1-sqrt(A1^2+B1^2-C1^2))/(-A1-C1));
                theeta4new(i)=2*atan((-B1-sqrt(A4^2+B4^2-C4^2))/(-A4-C4));
                postheeta4new(i)=2*atan((-B1+sqrt(A4^2+B4^2-C4^2))/(-A4-C4));
            end
            
            if (theeta1(i)<-8*pi/180)
                calc_start=0;
                %break;
            end
            
            
            theeta2(i)=asin((Yc-l1*sin(theeta1(i)))/l2);
            theeta3new(i)=acos((Xc-l5-l4*cos(theeta4(i)))/l3);
            
            theeta4(i)=asin((Yc-(l3*sin(theeta3(i))))/l4);
            
            if ((calc_start==1) && (prev_called==0))
                min_h=Yc;
                min_l=Xc;
                prev_called=1;
            end
            if ((calc_start==0) && (prev_called==1))
                max_h=Yc;
                max_l=Xc;
                break;
            end
            if (calc_start==1) && (prev_called==1) && (Yc==399)
                max_h=Yc;         
            end
            
        end
        %Y(j,k)=Yc+550;
        obt_elevation=max_h-min_h;
        if obt_elevation<0
            disp(j,k)
        end
        
        obt_horizontal_deviation=max(max_l,min_l);
        Y(j,k)=max_h-min_h;
        %disp("j:"+j+",k:"+k+", v elevation:"+obt_elevation+", H deviation :"+obt_horizontal_deviation);
        X(j,k)=obt_horizontal_deviation;
    end
end


% disp(theeta1/pi*180);
% disp(theeta2/pi*180);
% disp(theeta3/pi*180);
% disp(theeta4/pi*180);
%
% disp(theeta3new/pi*180);
% disp(theeta4new/pi*180);

figure(2)
surfl(Y)
colormap(pink)    % change color map
shading interp

figure(3)
surfl(X)
colormap(pink)    % change color map
shading interp

