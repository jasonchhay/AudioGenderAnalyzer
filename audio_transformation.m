%Code taken from:
%https://www.mathworks.com/help/matlab/math/fourier-transforms.html

files = dir('audio_files/*.wav');
N = length(files);
filename_array = {};
pitch_array = {};
spl_array = {};

for i = 1:N    
    filename = files(i,1).name;
    filename_array = [filename_array; filename];
    filename
    
    [x, fs] = audioread(strcat('audio_files/',filename));
    
    %Find pitch
    [p, idx] = pitch(x, fs);
    pitch_channel_1 = rmoutliers(p(1:length(p),1));
    pitch_all_channels = {};
    [row, col] = size(p);
    %if a second channel exists
    if col > 1
        pitch_channel_2 = rmoutliers(p(1:length(p),2));
        
        %add second channel into the pitch array
        pitch_all_channels = vertcat(pitch_channel_1, pitch_channel_2);
    else
        pitch_all_channels = pitch_channel_1;
    end
        
    avg_pitch = mean(pitch_all_channels);
    
    pitch_array = [pitch_array; avg_pitch];

    %Calculating sound pressure level (SPL)
    SPL = splMeter;
    Lt = SPL(x);
    Lt = Lt(~isinf(Lt)); %removes -Inf values from log(0)
    Lt = rmoutliers(Lt); %removes outliers from SPL
    avg_sound_pressure = mean(Lt); %calculates average SPL
    spl_array = [spl_array; avg_sound_pressure];
end

File_Name = filename_array;
Pitch = pitch_array;
SPL = spl_array;

T = table(File_Name, Pitch, SPL);
writetable(T, 'tabledata.txt');
type tabledata.txt




%{
voice = 'Voice Samples/male_voice.wav';


m = length(x);
time = (0:1/fs:(m-1)/fs);

%Identifying the average pitch
[p, idx] = pitch(x,fs);
pitch_channel_1 = p(1:length(p),1);
pitch_channel_2 = p(1:length(p),2);


pitch_sum = 0;

for i = 1:length(p)
    pitch_sum = pitch_sum + p(i,1);
    pitch_sum = pitch_sum + p(i,2);
end

approx_fund_freq = pitch_sum / (length(p)*2);
approx_fund_freq 
%}


%{
%Identifying the frequencies
n = pow2(nextpow2(m));
y = fft(x, n);
f = (0:n-1)*(fs/n)/10; % frequency vector
power = abs(y).^2/n;   % power spectrum  
plot(f(1:floor(n/2)),power(1:floor(n/2)))

xlabel('Frequency (Hz)')
ylabel('Power (Watt)')
title('Frequency vs Power')
xlim([0 400])
%}
