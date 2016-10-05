function b=fly_histo_cut_180_new(file)

% This funtion accepts 1 min activity data flies and does 3 things; 
% 1) It divides the data in 180min (3hours) chunks
% 2) It changes whatever is 0 to 1 and whatever is >1 to 0 (so now we can
% count the inactivity time)
% 3) It counts consecutive ones (time inactive) and puts the sum of ones in
% the bin where the period started.

% The output file will be of the same size of the input size but it will
% have the durations of the inactive periods.
%Steps 2 and 3 mentioned above are done using "fly_histo" funtion.


[x y]= size(file);

if mod(x,180)~=0
    error('Your data file cannot be divided evenly into 3 hour bins!')
end

b=zeros(x,y);
for i=1:(x/180)
    acurrent=file(1+(180*(i-1)):180*i,:);
    b(1+(180*(i-1)):180*i,:)=fly_histo_3hr_new(acurrent);
end


% if x==14400;
% 
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% a57=file(10081:10260,:);
% a58=file(10261:10440,:);
% a59=file(10441:10620,:);
% a60=file(10621:10800,:);
% a61=file(10801:10980,:);
% a62=file(10981:11160,:);
% a63=file(11161:11340,:);
% a64=file(11341:11520,:);
% a65=file(11521:11700,:);
% a66=file(11701:11880,:);
% a67=file(11881:12060,:);
% a68=file(12061:12240,:);
% a69=file(12240:12420,:);
% a70=file(12421:12600,:);
% a71=file(12601:12780,:);
% a72=file(12781:12960,:);
% a73=file(12961:13140,:);
% a74=file(13141:13320,:);
% a75=file(13321:13500,:);
% a76=file(13501:13680,:);
% a77=file(13681:13860,:);
% a78=file(13861:14040,:);
% a79=file(14041:14220,:);
% a80=file(14221:14400,:);
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% b57=fly_histo(a57);
% b58=fly_histo(a58);
% b59=fly_histo(a59);
% b60=fly_histo(a60);
% b61=fly_histo(a61);
% b62=fly_histo(a62);
% b63=fly_histo(a63);
% b64=fly_histo(a64);
% b65=fly_histo(a65);
% b66=fly_histo(a66);
% b67=fly_histo(a67);
% b68=fly_histo(a68);
% b69=fly_histo(a69);
% b70=fly_histo(a70);
% b71=fly_histo(a71);
% b72=fly_histo(a72);
% b73=fly_histo(a73);
% b74=fly_histo(a74);
% b75=fly_histo(a75);
% b76=fly_histo(a76);
% b77=fly_histo(a77);
% b78=fly_histo(a78);
% b79=fly_histo(a79);
% b80=fly_histo(a80);
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52;b53;b54;b55;b56;b57;b58;b59;b60;b61;b62;b63;b64;b65;b66;b67;b68;b69;b70,b71;b72;b73;b74;b75;b76;b77;b78;b79;b80];
% 
% end
% if x==13680;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% a57=file(10081:10260,:);
% a58=file(10261:10440,:);
% a59=file(10441:10620,:);
% a60=file(10621:10800,:);
% a61=file(10801:10980,:);
% a62=file(10981:11160,:);
% a63=file(11161:11340,:);
% a64=file(11341:11520,:);
% a65=file(11521:11700,:);
% a66=file(11701:11880,:);
% a67=file(11881:12060,:);
% a68=file(12061:12240,:);
% a69=file(12240:12420,:);
% a70=file(12421:12600,:);
% a71=file(12601:12780,:);
% a72=file(12781:12960,:);
% a73=file(12961:13140,:);
% a74=file(13141:13320,:);
% a75=file(13321:13500,:);
% a76=file(13501:13680,:);
% 
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% b57=fly_histo(a57);
% b58=fly_histo(a58);
% b59=fly_histo(a59);
% b60=fly_histo(a60);
% b61=fly_histo(a61);
% b62=fly_histo(a62);
% b63=fly_histo(a63);
% b64=fly_histo(a64);
% b65=fly_histo(a65);
% b66=fly_histo(a66);
% b67=fly_histo(a67);
% b68=fly_histo(a68);
% b69=fly_histo(a69);
% b70=fly_histo(a70);
% b71=fly_histo(a71);
% b72=fly_histo(a72);
% b73=fly_histo(a73);
% b74=fly_histo(a74);
% b75=fly_histo(a75);
% b76=fly_histo(a76);
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52;b53;b54;b55;b56;b57;b58;b59;b60;b61;b62;b63;b64;b65;b66;b67;b68;b69;b70,b71;b72;b73;b74;b75;b76];
% 
% end
% 
% if x==12960;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% a57=file(10081:10260,:);
% a58=file(10261:10440,:);
% a59=file(10441:10620,:);
% a60=file(10621:10800,:);
% a61=file(10801:10980,:);
% a62=file(10981:11160,:);
% a63=file(11161:11340,:);
% a64=file(11341:11520,:);
% a65=file(11521:11700,:);
% a66=file(11701:11880,:);
% a67=file(11881:12060,:);
% a68=file(12061:12240,:);
% a69=file(12240:12420,:);
% a70=file(12421:12600,:);
% a71=file(12601:12780,:);
% a72=file(12781:12960,:);
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% b57=fly_histo(a57);
% b58=fly_histo(a58);
% b59=fly_histo(a59);
% b60=fly_histo(a60);
% b61=fly_histo(a61);
% b62=fly_histo(a62);
% b63=fly_histo(a63);
% b64=fly_histo(a64);
% b65=fly_histo(a65);
% b66=fly_histo(a66);
% b67=fly_histo(a67);
% b68=fly_histo(a68);
% b69=fly_histo(a69);
% b70=fly_histo(a70);
% b71=fly_histo(a71);
% b72=fly_histo(a72);
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10;b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30;b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50;b51;b52;b53;b54;b55;b56;b57;b58;b59;b60;b61;b62;b63;b64;b65;b66;b67;b68;b69;b70;b71;b72];
% 
% 
% 
% end
% 
% if x==12240;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% a57=file(10081:10260,:);
% a58=file(10261:10440,:);
% a59=file(10441:10620,:);
% a60=file(10621:10800,:);
% a61=file(10801:10980,:);
% a62=file(10981:11160,:);
% a63=file(11161:11340,:);
% a64=file(11341:11520,:);
% a65=file(11521:11700,:);
% a66=file(11701:11880,:);
% a67=file(11881:12060,:);
% a68=file(12061:12240,:);
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% b57=fly_histo(a57);
% b58=fly_histo(a58);
% b59=fly_histo(a59);
% b60=fly_histo(a60);
% b61=fly_histo(a61);
% b62=fly_histo(a62);
% b63=fly_histo(a63);
% b64=fly_histo(a64);
% b65=fly_histo(a65);
% b66=fly_histo(a66);
% b67=fly_histo(a67);
% b68=fly_histo(a68);
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52;b53;b54;b55;b56;b57;b58;b59;b60;b61;b62;b63;b64;b65;b66;b67;b68];
% 
% 
% end
% 
% if x==11520;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% a57=file(10081:10260,:);
% a58=file(10261:10440,:);
% a59=file(10441:10620,:);
% a60=file(10621:10800,:);
% a61=file(10801:10980,:);
% a62=file(10981:11160,:);
% a63=file(11161:11340,:);
% a64=file(11341:11520,:);
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% b57=fly_histo(a57);
% b58=fly_histo(a58);
% b59=fly_histo(a59);
% b60=fly_histo(a60);
% b61=fly_histo(a61);
% b62=fly_histo(a62);
% b63=fly_histo(a63);
% b64=fly_histo(a64);
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52;b53;b54;b55;b56;b57;b58;b59;b60;b61;b62;b63;b64];
% 
% end
% 
% if x==10800;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% a57=file(10081:10260,:);
% a58=file(10261:10440,:);
% a59=file(10441:10620,:);
% a60=file(10621:10800,:);
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% b57=fly_histo(a57);
% b58=fly_histo(a58);
% b59=fly_histo(a59);
% b60=fly_histo(a60);
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52;b53;b54;b55;b56;b57;b58;b59;b60];
% 
% end
% 
% if x==10080;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% a53=file(9361:9540,:);
% a54=file(9541:9720,:);
% a55=file(9721:9900,:);
% a56=file(9901:10080,:);
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% b53=fly_histo(a53);
% b54=fly_histo(a54);
% b55=fly_histo(a55);
% b56=fly_histo(a56);
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52;b53;b54;b55;b56];
% end
% 
% if x==9360;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% a49=file(8641:8820,:);
% a50=file(8821:9000,:);
% a51=file(9001:9180,:);
% a52=file(9181:9360,:);
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% b49=fly_histo(a49);
% b50=fly_histo(a50);
% b51=fly_histo(a51);
% b52=fly_histo(a52);
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48;b49;b50,b51;b52];
% 
% end
% 
% if x==8640;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% a45=file(7921:8100,:);
% a46=file(8101:8280,:);
% a47=file(8281:8460,:);
% a48=file(8461:8640,:);
% 
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% b45=fly_histo(a45);
% b46=fly_histo(a46);
% b47=fly_histo(a47);
% b48=fly_histo(a48);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44;b45;b46;b47;b48];
% 
% end
% 
% if x==7920;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% a41=file(7201:7380,:);
% a42=file(7381:7560,:);
% a43=file(7561:7740,:);
% a44=file(7741:7920,:);
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% b41=fly_histo(a41);
% b42=fly_histo(a42);
% b43=fly_histo(a43);
% b44=fly_histo(a44);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40;b41;b42;b43;b44];
% 
% 
% end
% 
% 
% 
% if x==7200;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% a37=file(6481:6660,:);
% a38=file(6661:6840,:);
% a39=file(6841:7020,:);
% a40=file(7021:7200,:);
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% b37=fly_histo(a37);
% b38=fly_histo(a38);
% b39=fly_histo(a39);
% b40=fly_histo(a40);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36;b37;b38;b39;b40];
% 
% end
% 
% [x y]= size(file);
% 
% if x==6480;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% a33=file(5761:5940,:);
% a34=file(5941:6120,:);
% a35=file(6121:6300,:);
% a36=file(6301:6480,:);
% 
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% b33=fly_histo(a33);
% b34=fly_histo(a34);
% b35=fly_histo(a35);
% b36=fly_histo(a36);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32;b33;b34;b35;b36];
% 
%    
% end
% 
% [x y]= size(file);
% 
% if x==5760;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% a29=file(5041:5220,:);
% a30=file(5221:5400,:);
% a31=file(5401:5580,:);
% a32=file(5581:5760,:);
% 
% 
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% b29=fly_histo(a29);
% b30=fly_histo(a30);
% b31=fly_histo(a31);
% b32=fly_histo(a32);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28;b29;b30,b31;b32];
% 
% end
% 
% [x y]= size(file);
% 
% if x==5040;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% a25=file(4321:4500,:);
% a26=file(4501:4680,:);
% a27=file(4681:4860,:);
% a28=file(4861:5040,:);
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% b25=fly_histo(a25);
% b26=fly_histo(a26);
% b27=fly_histo(a27);
% b28=fly_histo(a28);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24;b25;b26;b27;b28];
% 
% end
% 
% [x y]= size(file);
% 
% if x==4320;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% a21=file(3601:3780,:);
% a22=file(3781:3960,:);
% a23=file(3961:4140,:);
% a24=file(4141:4320,:);
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% b21=fly_histo(a21);
% b22=fly_histo(a22);
% b23=fly_histo(a23);
% b24=fly_histo(a24);
% 
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10;b11;b12;b13;b14;b15;b16;b17;b18;b19;b20;b21;b22;b23;b24];
% 
% 
% end
% 
% [x y]= size(file);
% 
% if x==3600;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% a17=file(2881:3060,:);
% a18=file(3061:3240,:);
% a19=file(3241:3420,:);
% a20=file(3421:3600,:);
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% b17=fly_histo(a17);
% b18=fly_histo(a18);
% b19=fly_histo(a19);
% b20=fly_histo(a20);
% 
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12;b13;b14;b15;b16;b17;b18;b19;b20];
% 
% end
% [x y]= size(file);
% 
% if x==2880;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% a13=file(2161:2340,:);
% a14=file(2341:2520,:);
% a15=file(2521:2700,:);
% a16=file(2701:2880,:);
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% b13=fly_histo(a13);
% b14=fly_histo(a14);
% b15=fly_histo(a15);
% b16=fly_histo(a16);
% 
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10;b11;b12;b13;b14;b15;b16];
% end
% 
% [x y]= size(file);
% 
% if x==2160;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% a9=file(1441:1620,:);
% a10=file(1621:1800,:);
% a11=file(1801:1980,:);
% a12=file(1981:2160,:);
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% b9=fly_histo(a9);
% b10=fly_histo(a10);
% b11=fly_histo(a11);
% b12=fly_histo(a12);
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8;b9;b10,b11;b12];
% 
% 
% end
% 
% [x y]= size(file);
% 
% if x==1440;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% a5=file(721:900,:);
% a6=file(901:1080,:);
% a7=file(1081:1260,:);
% a8=file(1261:1440,:);
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% b5=fly_histo(a5);
% b6=fly_histo(a6);
% b7=fly_histo(a7);
% b8=fly_histo(a8);
% 
% 
% 
% 
% b=[b1;b2;b3;b4;b5;b6;b7;b8];
% 
% 
% end
% 
% [x y]= size(file);
% 
% if x==720;
% a1=file(1:180,:);
% a2=file(181:360,:);
% a3=file(361:540,:);
% a4=file(541:720,:);
% 
% 
% 
% 
% b1=fly_histo(a1);
% b2=fly_histo(a2);
% b3=fly_histo(a3);
% b4=fly_histo(a4);
% 
% 
% 
% 
% 
% b=[b1;b2;b3;b4];
% 
% end
