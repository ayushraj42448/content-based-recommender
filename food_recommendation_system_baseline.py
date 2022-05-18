# -*- coding: utf-8 -*-
"""Food-Recommendation-System-Baseline.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1l3gSBVWjH46ArY2Ae9z-YHI5Q0lvqe0F
"""

import pandas as pd
import numpy as np

df = pd.read_excel("Meals_w_Goals_deid_snapshot.xlsx")

df.head()

df.shape

df.drop(df[df.preferred_locale == 'es'].index, inplace=True)

df.shape

cleaned_df = df.drop(columns=['goal_id', 'meal_type', 'goal_short_name', 'expert_assessment', 'user_id', 'meal_id', 'goal_id', 'expert_assessment', 'carbs_grams', 'protein_grams','fat_grams', 'fiber_grams', 'calories', 'carbs_RD_explanation', 'protein_RD_explanation', 'fat_RD_explanation', 'fiber_RD_explanation', 'calories_RD_explanation', 'preferred_locale'])
cleaned_df.head()

cleaned_df['meal_title'] = cleaned_df['meal_title'].drop_duplicates()

# cleaned_df = cleaned_df[pd.notnull(df['meal_title'])]
# df = df[df['EPS'].notna()]
cleaned_df = cleaned_df[cleaned_df['meal_title'].notna()]

cleaned_df['meal_title']

cleaned_df.info()

df["overview"] = cleaned_df["meal_ingredients"].astype(str) +" "+ cleaned_df["expert_explanation"].astype(str)

df.head(1)['overview']

#using Tfidf; converting each record in the overview column into a document matrix
from sklearn.feature_extraction.text import TfidfVectorizer


tfv = TfidfVectorizer(min_df=3,  max_features=None, 
            strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
            ngram_range=(1, 3),
            stop_words = 'english')

# Filling NaNs with empty string
df['overview'] = df['overview'].fillna('')

# Fitting the TF-IDF on the 'overview' text
tfv_matrix = tfv.fit_transform(df['overview'])

df['overview']

tfv_matrix

tfv_matrix.shape

from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity

# Compute the sigmoid kernel. the below is done to find the combination of matrices
#the output give us a probability of relation between the vectors of the matrix which are nothing but two rows in our overview column
sig = cosine_similarity(tfv_matrix, tfv_matrix)

sig[0]

# Reverse mapping of indices and movie titles
indices = pd.Series(cleaned_df.index, index=cleaned_df['meal_title']).drop_duplicates()

indices[0:50]

indices = indices.drop_duplicates()

indices['Salad with turkey burger']

sig[2]

sig[947]

list(enumerate(sig[indices['Quinoa and vegetables']]))

sorted(list(enumerate(sig[indices['Quinoa and vegetables']])), key=lambda x: x[1], reverse=True)

class foodrecommendation:

  def give_rec(self, title, sig=sig):
      # Get the index corresponding to meal_title
      idx = indices[title]

      # Get the pairwsie similarity scores 
      sig_scores = list(enumerate(sig[idx]))

      # Sort the meal_tile 
      sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

      # Scores of the 5 most similar meals
      sig_scores = sig_scores[1:6]

      # meal_title indices
      meal_indices = [i[0] for i in sig_scores]

      # Top 5 most similar meals
      return cleaned_df['meal_title'].iloc[meal_indices]

# Testing the recommendation system
# give_rec('Chicken with mixed vegetables')
#
# foodrecommendation.give_rec('Sandwich')
#
# my_object = foodrecommendation()
#
# my_object.give_rec('Sandwich')

# import pickle
#
# with open('modelpickel1', 'wb') as files:
#     pickle.dump(my_object, files)
#
# import pickle
#
# with open('modelpickel1' , 'rb') as f:
#     lr = pickle.load(f)
#
# print(lr.give_rec('Sandwich'))# similar



# !pip install googletrans==3.1.0a0

# # import the library
# import googletrans
# from googletrans import Translator

# df1 = pd.read_excel('Meals_w_Goals_deid_snapshot.xlsx')

# df1.head()
#
# df1.drop(df1[df1.preferred_locale == 'en'].index, inplace=True)
#
# df1.head()
#
# df1 = df1[df1['expert_explanation'].notna()]
#
# df1.shape
#
# text = df1['expert_explanation'].to_list()
# text
#
# # translator = Translator()
#
# # text_trans = translator.translate( text, dest='en', src='auto')
#
# # desc = []
# # for trans in text_trans:
# #     a = trans.text
# #     print(f'{trans.text}')
# #     desc.append(a)
#
# import pandas as pd
# import numpy as np
#
# df = pd.read_excel("Meals_w_Goals_deid_snapshot.xlsx")
#
# df.head()
#
# df.shape
#
# df.drop(df[df.preferred_locale == 'es'].index, inplace=True)
#
# cleaned_df = df.drop(columns=['goal_id', 'meal_type', 'goal_short_name', 'expert_assessment', 'user_id', 'meal_id', 'goal_id', 'expert_assessment', 'carbs_grams', 'protein_grams','fat_grams', 'fiber_grams', 'calories', 'carbs_RD_explanation', 'protein_RD_explanation', 'fat_RD_explanation', 'fiber_RD_explanation', 'calories_RD_explanation', 'preferred_locale'])
# cleaned_df.head()
#
# cleaned_df.shape
#
# cleaned_df['meal_title'] = cleaned_df['meal_title'].drop_duplicates()
#
# # cleaned_df = cleaned_df[pd.notnull(df['meal_title'])]
# # df = df[df['EPS'].notna()]
# cleaned_df = cleaned_df[cleaned_df['meal_title'].notna()]
#
# cleaned_df.shape

# !pip install googletrans==3.1.0a0

# # import the library
# import googletrans
# from googletrans import Translator

# translator = Translator()

# translations = {}
# for column in cleaned_df.columns:
#     # unique elements of the column
#     unique_elements = cleaned_df[column].unique()
#     for element in unique_elements:
#         # add translation to the dictionary
#         translations[element] = translator.translate(element).text
    
# print(translations)

# cleaned_df.replace(translations, inplace = True)

# # check translation
# cleaned_df.head()

# cleaned_df.shape

# cleaned_df['meal_title']

# cleaned_df.info()

# df["overview"] = cleaned_df["meal_ingredients"].astype(str) +" "+ cleaned_df["expert_explanation"].astype(str)

# df.head(1)['overview']

# #using Tfidf; converting each record in the overview column into a document matrix
# from sklearn.feature_extraction.text import TfidfVectorizer


# tfv = TfidfVectorizer(min_df=3,  max_features=None, 
#             strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
#             ngram_range=(1, 3),
#             stop_words = 'english')

# # Filling NaNs with empty string
# df['overview'] = df['overview'].fillna('')

# # Fitting the TF-IDF on the 'overview' text
# tfv_matrix = tfv.fit_transform(df['overview'])

# df['overview']

# from sklearn.metrics.pairwise import sigmoid_kernel
# from sklearn.metrics.pairwise import cosine_similarity

# # Compute the sigmoid kernel. the below is done to find the combination of matrices
# #the output give us a probability of relation between the vectors of the matrix which are nothing but two rows in our overview column
# sig = cosine_similarity(tfv_matrix, tfv_matrix)

# # Reverse mapping of indices and movie titles
# indices = pd.Series(cleaned_df.index, index=cleaned_df['meal_title']).drop_duplicates()

# indices[0:50]

# indices = indices.drop_duplicates()

# indices['Salad with turkey burger']

# sig[2]

# sig[947]

# list(enumerate(sig[indices['Quinoa and vegetables']]))

# sorted(list(enumerate(sig[indices['Quinoa and vegetables']])), key=lambda x: x[1], reverse=True)

# def give_rec(title, sig=sig):
#     # Get the index corresponding to meal_title
#     idx = indices[title]

#     # Get the pairwsie similarity scores 
#     sig_scores = list(enumerate(sig[idx]))

#     # Sort the meal_tile 
#     sig_scores = sorted(sig_scores, key=lambda x: x[1], reverse=True)

#     # Scores of the 5 most similar meals
#     sig_scores = sig_scores[1:6]

#     # meal_title indices
#     meal_indices = [i[0] for i in sig_scores]

#     # Top 5 most similar meals
#     return cleaned_df['meal_title'].iloc[meal_indices]

# # Testing the recommendation system
# give_rec('Sandwich')