import os
import django
import random
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wavelength.settings")
django.setup()

from app.models import *

# This function assigns a random name to the teams
def get_questions():
    left=[]
    right=[]
    spectrum_list=[]
    with open("app/static/txt/spectrum_bank.csv") as f:
        spectrums = f.readlines()
        for spectrum in spectrums:
            spectrum_word = spectrum.split(",")
            spectrum_list.append(spectrum_word)
        
        for i in spectrum_list:
            left.append(i[0])
            # right_word= i[1].removesuffix('\n')
            # right_nobasht=right_word.removesuffix('\t')
            right.append(i[1])

        all_spectrums = list(zip(left, right))

        return all_spectrums

# print(get_questions())
data = get_questions()

for spectrum in data:
    # print(spectrum[0])
    # print(spectrum[1])
    Question.objects.create(left_spectrum= spectrum[0], right_spectrum=spectrum[1])

if Question.objects.all().exists():
    print("Objects have been created")
else:
    print("Error creating questions")