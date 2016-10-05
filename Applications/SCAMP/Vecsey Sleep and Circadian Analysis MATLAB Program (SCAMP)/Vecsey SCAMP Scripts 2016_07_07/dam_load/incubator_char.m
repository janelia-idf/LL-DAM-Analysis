function i=incubator_char(c)
% return character corresponding to incubator

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
switch(c)
 case {'f','F'}
  i=1;
 case {'E','e'}
  i=2;
 case {'Z','z'}
  i=3;
 case {'D','d'}
  i=4;
 case{'n','N'}
  i=5;
 otherwise
  fprintf('%s is not a valid incubator, so no daylight available\n',c)
  i = 0;
end
