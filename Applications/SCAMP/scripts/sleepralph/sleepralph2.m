function [s30]=sleepRalph2(p,o,n,doprint)

%p=name of 1min data file
%o=name of 30min data file
%n= sleep definition (usually 5 or 30 (minutes))
% RALF(O) does Ralf-style multi-actogram plot on DAM data in O

%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Copyright (C)Jeffrey Hall Lab, Brandeis University.             %%
% Use and distribution of this software is free for academic      %%
% purposes only, provided this copyright notice is not removed.   %%
% Not for commercial use.                                         %%
% Unless by explicit permission from the copyright holder.        %%
% Mailing address:                                                %%
% Jeff Hall Lab, Kalman Bldg, Brandeis Univ, Waltham MA 02454 USA %%
% Email: hall@brandeis.edu                                        %%
%%(C)%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
[a,s30]=fly_sleepthresh(p,n);
b=repmat(o(1),1,1);
b.f=s30;




clf

for i=1:size(b.data, 2) % SDL changed from 32
    subplot(4,8,i)
  dam_actogram2(b,i)
%   set(gcf,'PaperOrientation','landscape');
% set(gcf, 'PaperPositionMode', 'manual');
% set(gcf, 'PaperPosition', [0.25 0.25 10.75 8.25]);
% set (gca,'FontSize',6)
% end
% if doprint>0
%    print
end
