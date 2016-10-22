function grouperrorbarAllD2(doprint,s30,groupnames)

A=[];
AE=[];
raw=[];
    for i=1:length(s30)
        [r c]=size(s30{i});
        if c==1
            
            raw=[raw;s30{i}'];
            
        else
            A=[A;nanmean(s30{i}')];
            AE=[AE;nansem(s30{i}')];
        end
    end

    [x y]=size(s30{1});
    j=x/48;
 
    if j<=12
        for n=1:j
        subplot(4,3,n);
            if ~isempty(raw)
                plot(raw(:,48*(n-1)+1:48*n)','linewidth',1.25);
            end
            
            if ~isempty(A)
                errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)','linewidth',1.25)
            end

            xlim([0 48]),ylim([0 35]);
            set(gca,'Fontsize',10,'Xtick',[0 12 24 36 48],'XTickLabel',{'0';'6';'12';'18';'24'});
            ylabel('Sleep (min/30min)'),xlabel('ZT/CT');
        end
    else
        for n=1:j
        subplot(5,4,n);
        
            if ~isempty(raw)
                plot(raw(:,48*(n-1)+1:48*n)','linewidth',1.25);
            end

            if ~isempty(A)
                errorbar (A(:,48*(n-1)+1:48*n)',AE(:,48*(n-1)+1:48*n)','linewidth',1.25)
            end
            
            xlim([0 48]),ylim([0 35]);
            set(gca,'Fontsize',10,'Xtick',[0 12 24 36 48],'XTickLabel',{'0';'6';'12';'18';'24'});
            ylabel('Sleep (min/30min)'),xlabel('ZT/CT');
        end
    end

set(gcf,'PaperOrientation','landscape');
set(gcf, 'PaperPositionMode', 'manual');
set(gcf, 'PaperPosition', [0.25 0.25 10.75 8.25]);
legend(groupnames);
if doprint>0
   print
end