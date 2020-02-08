clc
clear  

num = [3,6,11,12,13,15,17,18];
for i= 1:length(num)
    src_domain = readtable(['sv_feature.' num2str(num(i)) '.csv']);
    for j= 1:length(num)
        if i~=j
            tar_domain = readtable(['sv_feature.' num2str(num(j))  '.csv']);
            Xs = table2array(src_domain(:,1:20));
            Ys = table2array(src_domain(:,21));
            Xt = table2array(tar_domain(:,1:20));
            Yt = table2array(tar_domain(:,21));
            options.gamma = 2; % the parameter for kernel
            options.kernel_type = 'linear';
            options.lambda = 1.0;
            options.dim = 15;
            [X_src_new,X_tar_new,A] = TCA(Xs,Xt,options);
            src_data = table(X_src_new);
            src_data.label = Ys;
            writetable(src_data,['src_data.' num2str(num(i)) '_' num2str(num(j)) '.csv']);
            tar_data = table(X_tar_new);
            tar_data.label = Yt;
            writetable(tar_data,['tar_data.' num2str(num(i)) '_' num2str(num(j)) '.csv']);
        end
    end
end

