% 图像加密算法 - 修复 bitxor 错误
% 完整可运行版本

% 清理环境
clear all;
close all;
clc;

% ====================== 混沌系统定义 ======================
% Logistic混沌映射
function sequence = logistic_map(z0, mu, iterations)
    sequence = zeros(1, iterations);
    z = z0;
    for i = 1:iterations
        z = mu * z * (1 - z);
        sequence(i) = z;
    end
end

% 2D Logistic-Sine-Coupling Map (2D-LSCM)
function [x_seq, y_seq] = lscm_map(x0, y0, mu, iterations)
    x_seq = zeros(1, iterations);
    y_seq = zeros(1, iterations);
    x = x0;
    y = y0;
    
    for i = 1:iterations
        x_new = sin(pi * (4 * mu * x * (1 - x) + (1 - mu) * sin(pi * y)));
        y_new = sin(pi * (4 * mu * y * (1 - y) + (1 - mu) * sin(pi * x_new)));
        x = x_new;
        y = y_new;
        x_seq(i) = x;
        y_seq(i) = y;
    end
end

% ====================== 密钥生成 ======================
function [x0, y0, mu1, z0, mu, D] = generate_keys(image, init_keys)
    [M, N] = size(image);
    total_pixels = M * N;
    
    % 解包初始密钥
    x0_tilde = init_keys(1);
    y0_tilde = init_keys(2);
    mu1_tilde = init_keys(3);
    z0_tilde = init_keys(4);
    mu_tilde = init_keys(5);
    
    % 计算像素总和和均值
    pixel_sum = sum(image(:));
    D = floor(pixel_sum / total_pixels);
    
    % 计算实际加密密钥
    % 抗零化攻击 + 非线性强化
    x0 = mod(x0_tilde * pixel_sum + x0_tilde, 1);
    y0 = mod(y0_tilde * pixel_sum + y0_tilde, 1);
    mu1 = mod(mu1_tilde * pixel_sum + mu1_tilde, 1);
    z0 = mod(z0_tilde * pixel_sum + z0_tilde, 1);
    % Logistic映射需满足：μ ∈ [3.5699, 4.0]
    mu = mod(mu_tilde * pixel_sum, 0.43) + 3.5699;
end

% ====================== S盒生成 ======================
function S_box = generate_sbox(x0, y0, mu, z0, mu1)
    % 使用Logistic映射生成基础序列
    log_seq = logistic_map(z0, mu1, 256);
    [~, L] = sort(log_seq);  % 保留排序后原索引，舍弃序列
    S1 = reshape(L, 16, 16);  % 转换为16x16矩阵
    
    % 使用2D-LSCM生成混淆序列
    [x_seq, y_seq] = lscm_map(x0, y0, mu, 128);
    [~, idx_x] = sort(x_seq);
    % L1 = 255 - idx_x;  % 行混淆序列 1-128 -> 127-254
    L1 = 257 - idx_x; % 行混淆序列 1-128 -> 129-256
    [~, idx_y] = sort(y_seq);
    % L2 = 255 - idx_y;  % 列混淆序列
    L2 = 257 - idx_y; % 行混淆序列 1-128 -> 129-256
    
    % 行序列混淆
    s1 = S1(:);
    for i = 1:256
        idx = mod(i-1, 128) + 1;  % 确保索引在1-128范围内
        % 交换 i 与 L1(i)数据的位置
        temp = s1(i);
        s1(i) = s1(L1(idx));
        s1(L1(idx)) = temp;
    end
    S2 = reshape(s1, 16, 16);

    
    % 列序列混淆
    s2 = S2(:);
    for i = 1:256
        idx = mod(i-1, 128) + 1;  % 确保索引在1-128范围内
        temp = s2(i);
        s2(i) = s2(L2(idx));
        s2(L2(idx)) = temp;
    end
    S_box = reshape(s2, 16, 16);
end

% ====================== 加密过程 ======================
function [encrypted, keys] = encrypt_image(image, init_keys)
    % 密钥生成
    [x0, y0, mu1, z0, mu, D] = generate_keys(image, init_keys);
    keys = [x0, y0, mu1, z0, mu, double(D)]; % 存储原始D值
    
    % 生成S盒
    S_box = generate_sbox(x0, y0, mu, z0, mu1);
    S_flat = S_box(:);
    
    % 生成置乱序列
    [M, N] = size(image);
    total_pixels = M * N;
    
    % 跳过瞬态
    [~, ~] = lscm_map(x0, y0, mu, 1000);
    
    % 生成有效序列
    [x_seq, y_seq] = lscm_map(x0, y0, mu, total_pixels);
    [~, L1] = sort(x_seq);  % 置乱索引
    
    % 关键修复：转换为整数类型
    L2 = uint8(floor(y_seq * 256));  % 扩散序列 (0-255)
    D_uint8 = uint8(D);              % 转换为整数
    
    % 图像置乱 (像素位置重排)
    p = image(:);
    p1 = zeros(size(p), 'uint8');
    for i = 1:total_pixels
        p1(i) = p(L1(i));
    end
    
    % 图像扩散 (像素值变换)
    p2 = zeros(size(p1), 'uint8');
    
    % 第一个像素特殊处理
    idx = bitxor(bitxor(uint8(p1(L1(1))), D_uint8), L2(L1(1)));
    p2(L1(1)) = S_flat(double(idx) + 1);  % 转换为double用于索引
    
    % 后续像素处理 (修复bitxor错误)
    for i = 2:total_pixels
        % 分别转换每个参数为uint8
        a = uint8(p1(L1(i)));
        b = uint8(p2(L1(i-1)));
        c = L2(L1(i));
        
        % 分步进行bitxor操作
        temp = bitxor(a, b);
        idx = bitxor(temp, c);
        
        p2(L1(i)) = S_flat(double(idx) + 1);
    end
    
    % 重构加密图像
    encrypted = reshape(p2, M, N);
end

% ====================== 解密过程 ======================
function decrypted = decrypt_image(encrypted, keys)
    % 解包密钥
    x0 = keys(1);
    y0 = keys(2);
    mu1 = keys(3);
    z0 = keys(4);
    mu = keys(5);
    D = uint8(keys(6));  % 转换为整数
    
    [M, N] = size(encrypted);
    total_pixels = M * N;
    
    % 生成S盒和逆S盒
    S_box = generate_sbox(x0, y0, mu, z0, mu1);
    S_flat = S_box(:);
    [~, S_inv] = sort(S_flat);  % 逆S盒
    
    % 生成置乱序列
    [~, ~] = lscm_map(x0, y0, mu, 1000);  % 跳过瞬态
    [x_seq, y_seq] = lscm_map(x0, y0, mu, total_pixels);
    [~, L1] = sort(x_seq);
    
    % 关键修复：转换为整数类型
    L2 = uint8(floor(y_seq * 256));  % 扩散序列 (0-255)
    
    % 逆扩散
    p2 = encrypted(:);
    p1 = zeros(size(p2), 'uint8');
    
    % 第一个像素处理
    idx_val = S_inv(p2(L1(1)) + 1);  % MATLAB索引从1开始
    raw_index = uint8(idx_val - 1);  % 转换为0-255整数
    p1(L1(1)) = bitxor(bitxor(raw_index, D), L2(L1(1)));
    
    % 后续像素处理 (修复bitxor错误)
    for i = 2:total_pixels
        idx_val = S_inv(p2(L1(i))) + 1;
        raw_index = uint8(idx_val - 1);
        
        % 分别转换每个参数为uint8
        a = raw_index;
        b = uint8(p2(L1(i-1)));
        c = L2(L1(i));
        
        % 分步进行bitxor操作
        temp = bitxor(a, b);
        p1(L1(i)) = bitxor(temp, c);
    end
    
    % 逆置乱 (正确实现)
    p = zeros(size(p1), 'uint8');
    for i = 1:total_pixels
        p(L1(i)) = p1(i);
    end
    
    % 重构解密图像
    decrypted = reshape(p, M, N);
end

% ====================== 主程序 ======================
% 1. 加载测试图像
original = imread('Lena.png');
if size(original, 3) == 3
    original = rgb2gray(original);
end

% 显示原始图像
figure('Name', '原始图像');
imshow(original);
title('原始图像');

% 2. 设置初始密钥 (论文中Table 4的值)
init_keys = [0.93319068404931, 0.22066608276058, ...
            0.38037735911743, 0.05822438756343, ...
            0.30619002605018];

% 3. 加密
tic;
[encrypted, keys] = encrypt_image(original, init_keys);
encryption_time = toc;
fprintf('加密时间: %.4f秒\n', encryption_time);

% 显示加密图像
figure('Name', '加密图像');
imshow(encrypted);
title('加密图像');

% 4. 解密
tic;
decrypted = decrypt_image(encrypted, keys);
decryption_time = toc;
fprintf('解密时间: %.4f秒\n', decryption_time);

% 显示解密图像
figure('Name', '解密图像');
imshow(decrypted);
title('解密图像');

% 5. 保存结果
imwrite(encrypted, 'encrypted.png');
imwrite(decrypted, 'decrypted.png');

% 6. 计算PSNR评估质量
mse = sum(sum((double(original) - double(decrypted)).^2)) / numel(original);
psnr = 10 * log10(255^2 / mse);
fprintf('PSNR: %.2f dB\n', psnr);

% 7. 检查是否完美恢复
if isequal(original, decrypted)
    disp('成功：解密图像与原始图像完全相同！');
else
    disp('警告：解密图像与原始图像存在差异！');
    
    % 显示差异
    diff_img = imabsdiff(original, decrypted);
    figure('Name', '差异图像');
    imshow(diff_img, []);
    title(sprintf('差异图像 (最大差异: %d)', max(diff_img(:))));
end