%Code taken from:
%https://www.mathworks.com/help/matlab/math/fourier-transforms.html

voice = 'test.wav';
[x, fs] = audioread(voice);
m = length(x);
time = (0:1/fs:(m-1)/fs);

n = pow2(nextpow2(m));
y = fft(x, n);
f = (0:n-1)*(fs/n)/10; % frequency vector
power = abs(y).^2/n;   % power spectrum  
plot(f(1:floor(n/2)),power(1:floor(n/2)))

xlabel('Frequency (Hz)')
ylabel('Power (Watt)')
title('Frequency vs Power')
xlim([0 400])