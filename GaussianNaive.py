import csv
import math
import statistics

#Retrieves the data from all the audiofiles
def init_audiofiles():
    audiofiles = []
    with open('C:/Users/Jason/Documents/MATLAB/audio_information.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            audiofiles.append(row)
    return audiofiles


#Calculates class probabilities based on size of class a and b
def __calculate_class_probability(a, b):
    total_size = a + b
    prob_a = a/total_size
    prob_b = 1 - prob_a

    return prob_a, prob_b


#Calculates the mean and standard deviation for pitch and SPL based on gender
def parse_audiofiles(audiofiles):
    pitch_m = []
    pitch_f = []
    spl_m = []
    spl_f = []

    for file in audiofiles:
        if file['Gender'] == 'M':
            pitch_m.append(float(file['Pitch']))
            spl_m.append(float(file['SPL']))
        else:
            pitch_f.append(float(file['Pitch']))
            spl_f.append(float(file['SPL']))

    male_stat = {}
    female_stat = {}

    male_stat['Pitch Mean'] = statistics.mean(pitch_m)
    male_stat['Pitch StDev'] = statistics.stdev(pitch_m)
    male_stat['SPL Mean'] = statistics.mean(spl_m)
    male_stat['SPL StDev'] = statistics.stdev(spl_m)

    female_stat['Pitch Mean'] = statistics.mean(pitch_f)
    female_stat['Pitch StDev'] = statistics.stdev(pitch_f)
    female_stat['SPL Mean'] = statistics.mean(spl_f)
    female_stat['SPL StDev'] = statistics.stdev(spl_f)

    prob_m, prob_f = __calculate_class_probability(len(pitch_m), len(pitch_f))
    return [male_stat, female_stat], [prob_m, prob_f]


#Calculates probability based on normalized probability density function
def normal_pdf(x, mean, stdev):
    y = 1/(math.sqrt(2*math.pi*stdev))
    z = -((x-mean)**2)/(2*stdev)

    return y*(math.e**z)


#Determines the gender of a supplied pitch and SPL based on Gaussian Naive Bayes
def gaussian_naive(audiofiles, user_pitch, user_spl):

    stat, gender_prob = parse_audiofiles(audiofiles)

    condit_prob_m = normal_pdf(user_pitch, stat[0]['Pitch Mean'], stat[0]['Pitch StDev'])
    condit_prob_m *= normal_pdf(user_spl, stat[0]['SPL Mean'], stat[0]['SPL StDev'])
    condit_prob_m *= gender_prob[0]

    condit_prob_f = normal_pdf(user_pitch, stat[1]['Pitch Mean'], stat[1]['Pitch StDev'])
    condit_prob_f *= normal_pdf(user_spl, stat[1]['SPL Mean'], stat[1]['SPL StDev'])
    condit_prob_f *= gender_prob[1]

    prob_m = (condit_prob_m/(condit_prob_m+condit_prob_f))
    prob_f = (condit_prob_f/(condit_prob_m+condit_prob_f))

    #print("Probability male:", prob_m)
    #print("Probability female:", prob_f)

    if(prob_m > prob_f):
        return 'M'
    else:
        return 'F'


#Retrieves an ordered list of all the genders in the audiofiels
def get_gender(audiofiles):
    gender = []

    for file in audiofiles:
        if file['Gender'] == 'M':
            gender.append('M')
        else:
            gender.append('F')

    return gender


audiofiles = init_audiofiles()

#Demo for Gaussian Naive
'''
user_pitch = float(input("Insert pitch: "))
user_spl = float(input("Insert SPL: "))
print(gaussian_naive(audiofiles, user_pitch, user_spl))
'''

#Used to determine accuracy

gender = get_gender(audiofiles)
correct_count = 0

for i in range(len(gender)):
    predicted_gender = gaussian_naive(audiofiles, float(audiofiles[i]['Pitch']), float(audiofiles[i]['SPL']))

    if gender[i] == predicted_gender:
        correct_count += 1

print("Guassian Naive percent correct:",correct_count/len(gender))
