
d2_to_mattressSurface=250;
l1=420;

l2=225;%y
d2=236;%x

d1=418;
l3=sqrt(d1^2+d2^2);
l4=370;
l5=450;
Hmin=600;
Hmax=1000;
groundTol5axis=290;
Ycmin=Hmin-d2_to_mattressSurface-groundTol5axis;
Ycmax=Hmax-d2_to_mattressSurface-groundTol5axis;
ycRange=Ycmin:Ycmax-1;
HRange=Hmin:Hmax-1;
Yc=Ycmin;


theeta1=zeros(1,Ycmax-Yc);
theeta2=zeros(1,Ycmax-Yc);
theeta3=zeros(1,Ycmax-Yc);
theeta4=zeros(1,Ycmax-Yc);
theeta3new=zeros(1,Ycmax-Yc);
theeta4new=zeros(1,Ycmax-Yc);
negtheeta1=zeros(1,Ycmax-Yc);
postheeta4new=zeros(1,Ycmax-Yc);

for i=1:length(ycRange)
    Yc=ycRange(i);
    theeta3(i)=acos(d1/l3);
    theeta4(i)=pi-asin((Yc-(l3*sin(theeta3(i))))/l4);
    
    Xc=l5+l3*cos(theeta3(i))-sqrt(l4^2-(Yc-l3*sin(theeta3(i)))^2);
    
    A1=Xc;
    B1=Yc;
    C1=(l1^2-l2^2+Xc^2+Yc^2)/(2*l1);
    
    A4=Xc-l5;
    B4=Yc;
    C4=(l4^2+l5^2-l3^2-(2*Xc*l5)+Xc^2+Yc^2)/(2*l4);
    
    %disp("t4: "+theeta4(i)/pi*180)
    if (A1^2+B1^2-C1^2)<0
        disp("Maximum limit reached, Limit is : "+Yc)
        break
    
    elseif (theeta4(i)>(pi+12*pi/180))
        disp ("Minimum limit is(t4) : "+Yc)
        theeta4(i)=0;
        theeta1(i)=0;
        continue
        
        
         
    end
    
    
    theeta1(i)=2*atan((-B1+sqrt(A1^2+B1^2-C1^2))/(-A1-C1));
    negtheeta1(i)=2*atan((-B1-sqrt(A1^2+B1^2-C1^2))/(-A1-C1));
    theeta4new(i)=2*atan((-B1-sqrt(A4^2+B4^2-C4^2))/(-A4-C4));
    postheeta4new(i)=2*atan((-B1+sqrt(A4^2+B4^2-C4^2))/(-A4-C4));
    
    if (theeta1(i)<-8*pi/180)
        disp ("Minimum limit is(t1) : "+Yc);
        theeta4(i)=0;
        theeta1(i)=0;
        continue
        
    end
    
    theeta2(i)=asin((Yc-l1*sin(theeta1(i)))/l2);
    theeta3new(i)=acos((Xc-l5-l4*cos(theeta4(i)))/l3);
    
    theeta4(i)=asin((Yc-(l3*sin(theeta3(i))))/l4);
    
end

%disp(theeta1/pi*180);
%disp(theeta2/pi*180);
%disp(theeta3/pi*180);
%disp(theeta4/pi*180);

%disp(theeta3new/pi*180);
%disp(theeta4new/pi*180);

figure(1)
plot(HRange,theeta1/pi*180)
hold on
plot(HRange,theeta4/pi*180)
title('Lifting Height vs Actuating Joint Angle');
xlabel('Height');
ylabel('Angle');
legend('Theeta1','Theeta4');

