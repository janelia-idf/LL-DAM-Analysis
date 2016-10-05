function o=blurb(s)
% inside-window text blurb for plot

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
% location of reporting text
TEXT_X = .5;
TEXT_Y = .8;

textx = txtpos(TEXT_X, 'XLim');
texty = txtpos(TEXT_Y, 'YLim');
o=text(textx, texty, s);

% text position normalized to axes
function pos = txtpos(s, xory)
lim = get(gca, xory);
pos = lim(1) + s * (lim(2) - lim(1));


