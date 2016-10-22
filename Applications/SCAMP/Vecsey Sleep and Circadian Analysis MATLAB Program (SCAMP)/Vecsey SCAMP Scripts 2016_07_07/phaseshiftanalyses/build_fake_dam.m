
function o=build_fake_dam(a,int,start,name)
o.f=a;
o.start=start;
o.x=(start+(0:size(a,1)-1)*int/60)';
o.data=o.f;
o.lights=[];
o.int=int;
for i=1:size(a,2)
    o.names{i}=sprintf('%s %d',name,i);
end