# SI671_final_project

Author: Shukai Fan, Dongjian Chen, Tianyi Ge

In this project, we use data mining and machine learning skills to build a ensemble user-based steam game retrieval system. We build our retrieval system based on the traditional game search engine based on query-document matching and add a ensemble recommendation model which use additional user features and item features to predict users' preferences for items. The combination of search model and recommendation can provide results not only based on searching query but also based on user preference. After the design and implementation of the models, we also design a specific evaluation process.

This repo mainly contains 7 python files for our user based retrieval system in ./search/. 

+ BM25.py defines the BM25 algorithm and inverted index calculations.
+ evaluation.py is used for performance evaluation and comparison between user-based system and original retrieval system
+ interactive.py implemented some Apis and classes for using the original system, construct the high level architecture of the retrieval system
+ retrieval.py implemented the basic function and class for naive retrieval function.
+ srank.py calculated the static rank of the games, cache the static ranks of the game.
+ user.py (abandoned class)
+ userretrieval.py implemented user-based retrieval system with architecture introduced in the report.


Datas are too large which can be download from:
https://cseweb.ucsd.edu/~jmcauley/datasets.html#steam_data
https://www.kaggle.com/nikdavis/steam-store-games?select=steam.csv

The models we used is contained in the ./search/models/ folder and ./search/user_game/ folder contains the user_based cleaned dataset we preprocessed.
The game infomation dataset is in ./search/steam_clean.xlsx.

The report is attached in this repo: si671_project.pdf.

Model Trainers are included in ./search/trainer/ with 4 python files.

+ Data_process.ipynb is for processing data.
+ Model.ipynb is for building machine leaning models
+ predict.py is for using recommendation model to predict scores
+ rate.ipynb is for building memory-based models.
