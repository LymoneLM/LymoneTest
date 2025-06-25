
clear all;
close all;
clc;

function sequence = logistic_map(z0, mu, iterations)
    sequence = zeros(1, iterations);
    z = z0;
    for i = 1:iterations
        z = mu * z * (1 - z);
        sequence(i) = z;
    end
end


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

function [x0, y0, mu1, z0, mu, D] = generate_keys(image, init_keys)
    [M, N] = size(image);
    total_pixels = M * N;
    

    x0_tilde = init_keys(1);
    y0_tilde = init_keys(2);
    mu1_tilde = init_keys(3);
    z0_tilde = init_keys(4);
    mu_tilde = init_keys(5);
    
    pixel_sum = sum(image(:));
    D = floor(pixel_sum / total_pixels);

    x0 = mod(x0_tilde * pixel_sum + x0_tilde, 1);
    y0 = mod(y0_tilde * pixel_sum + y0_tilde, 1);
    mu1 = mod(mu1_tilde * pixel_sum + mu1_tilde, 1);
    z0 = mod(z0_tilde * pixel_sum + z0_tilde, 1);
    mu = mod(mu_tilde * pixel_sum, 0.43) + 3.5699;
end

function S_box = generate_sbox(x0, y0, mu, z0, mu1)

    log_seq = logistic_map(z0, mu1, 256);
    [~, L] = sort(log_seq);  
    S1 = reshape(L, 16, 16); 

    [x_seq, y_seq] = lscm_map(x0, y0, mu, 128);
    [~, idx_x] = sort(x_seq);
    L1 = 255 - idx_x; 
    [~, idx_y] = sort(y_seq);
    L2 = 255 - idx_y;  

    s1 = S1(:);
    for i = 1:256
        idx = mod(i-1, 128) + 1; 
        temp = s1(i);
        s1(i) = s1(L1(idx));
        s1(L1(idx)) = temp;
    end
    S2 = reshape(s1, 16, 16);
    
    s2 = S2(:);
    for i = 1:256
        idx = mod(i-1, 128) + 1; 
        temp = s2(i);
        s2(i) = s2(L2(idx));
        s2(L2(idx)) = temp;
    end
    S_box = reshape(s2, 16, 16);
end

function [encrypted, keys] = encrypt_image(image, init_keys)

    [x0, y0, mu1, z0, mu, D] = generate_keys(image, init_keys);
    keys = [x0, y0, mu1, z0, mu, double(D)]; 
    
   
    S_box = generate_sbox(x0, y0, mu, z0, mu1);
    S_flat = S_box(:);
    

    [M, N] = size(image);
    total_pixels = M * N;
    
 
    [~, ~] = lscm_map(x0, y0, mu, 1000);
    

    [x_seq, y_seq] = lscm_map(x0, y0, mu, total_pixels);
    [~, L1] = sort(x_seq);  

    L2 = uint8(floor(y_seq * 256));  
    D_uint8 = uint8(D);              

    p = image(:);
    p1 = zeros(size(p), 'uint8');
    for i = 1:total_pixels
        p1(i) = p(L1(i));
    end
    
    p2 = zeros(size(p1), 'uint8');

    idx = bitxor(bitxor(uint8(p1(L1(1))), D_uint8), L2(L1(1)));
    p2(L1(1)) = S_flat(double(idx) + 1);  

    for i = 2:total_pixels
       
        a = uint8(p1(L1(i)));
        b = uint8(p2(L1(i-1)));
        c = L2(L1(i));
        
        
        temp = bitxor(a, b);
        idx = bitxor(temp, c);
        
        p2(L1(i)) = S_flat(double(idx) + 1);
    end

    encrypted = reshape(p2, M, N);
end


function decrypted = decrypt_image(encrypted, keys, init_keys)

    x0 = keys(1);
    y0 = keys(2);
    mu1 = keys(3);
    z0 = keys(4);
    mu = keys(5);
    D = uint8(keys(6));  
    
    [M, N] = size(encrypted);
    total_pixels = M * N;
 
    S_box = generate_sbox(x0, y0, mu, z0, mu1);
    S_flat = S_box(:);
    [~, S_inv] = sort(S_flat);  
    

    [~, ~] = lscm_map(x0, y0, mu, 1000);  
    [x_seq, y_seq] = lscm_map(x0, y0, mu, total_pixels);
    [~, L1] = sort(x_seq);

    L2 = uint8(floor(y_seq * 256));  
    
 
    p2 = encrypted(:);
    p1 = zeros(size(p2), 'uint8');
    
  
    idx_val = S_inv(p2(L1(1)) + 1);  
    raw_index = uint8(idx_val - 1);  
    p1(L1(1)) = bitxor(bitxor(raw_index, D), L2(L1(1)));
    

    for i = 2:total_pixels
        idx_val = S_inv(p2(L1(i))) + 1;
        raw_index = uint8(idx_val - 1);
        
 
        a = raw_index;
        b = uint8(p2(L1(i-1)));
        c = L2(L1(i));
        
        temp = bitxor(a, b);
        p1(L1(i)) = bitxor(temp, c);
    end
    

    p = zeros(size(p1), 'uint8');
    for i = 1:total_pixels
        p(L1(i)) = p1(i);
    end

    decrypted = reshape(p, M, N);
end


original = imread('Lena.png');
if size(original, 3) == 3
    original = rgb2gray(original);
end

figure('Name', '原始图像');
imshow(original);
title('原始图像');

init_keys = [0.93319068404931, 0.22066608276058, ...
            0.38037735911743, 0.05822438756343, ...
            0.30619002605018];


tic;
[encrypted, keys] = encrypt_image(original, init_keys);
encryption_time = toc;
fprintf('加密时间: %.4f秒\n', encryption_time);

figure('Name', '加密图像');
imshow(encrypted);
title('加密图像');


tic;
decrypted = decrypt_image(encrypted, keys, init_keys);
decryption_time = toc;
fprintf('解密时间: %.4f秒\n', decryption_time);


figure('Name', '解密图像');
imshow(decrypted);
title('解密图像');


imwrite(encrypted, 'encrypted.png');
imwrite(decrypted, 'decrypted.png');


mse = sum(sum((double(original) - double(decrypted)).^2)) / numel(original);
psnr = 10 * log10(255^2 / mse);
fprintf('PSNR: %.2f dB\n', psnr);


if isequal(original, decrypted)
    disp('成功：解密图像与原始图像完全相同！');
else
    disp('警告：解密图像与原始图像存在差异！');
    

    diff_img = imabsdiff(original, decrypted);
    figure('Name', '差异图像');
    imshow(diff_img, []);
    title(sprintf('差异图像 (最大差异: %d)', max(diff_img(:))));
end