[x, fs] = audioread('test.wav');
t = [0:length(x)-1]/fs;
y = fft(x);

msl = fs/1000;
ms20 = fs/50;

Y = fft(x.*hamming(length(x)));
C = fft(log(abs(Y)+eps));

q = (msl:ms20)/fs;
[Maxamp_at_pitch, fx]= max(abs(C(msl:ms20)));
freq_pitch = fs/(msl+fx-1);
