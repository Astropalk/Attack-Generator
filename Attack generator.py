import pandas as pd
import random
import os

random.seed(123)
# constant values
DEL_AVG_ARRAY = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950, 1000]
RO_MAL_ARRAY = [0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80]
START_DATE_M = '2016-04-01'  # day number 90
END_DATE_M = '2016-05-30'  # day number 152
ATTACK_YEAR = 2016

# date format 2014 file : 2014-01-30
# date format 2015 file : 2015-01-30
# date format 2016 file : 2016-01-30


# define dictionary for training data 2015 and 2014 years
TRAINING_DATA = {
    "2014": "C:/Users/abedz/OneDrive - Western Michigan "
            "University/PhD/Research/Diversity/Adv_Poisoning_ST/Adv_Poisoning_ST/resource/2014.csv",
    "2015": "C:/Users/abedz/OneDrive - Western Michigan "
            "University/PhD/Research/Diversity/Adv_Poisoning_ST/Adv_Poisoning_ST/resource/2015.csv",
    "2016": "C:/Users/abedz/OneDrive - Western Michigan "
            "University/PhD/Research/Diversity/Adv_Poisoning_ST/Adv_Poisoning_ST/resource/2016.csv",
}


# read data files:

def read_file_data(filePath):
    df = pd.read_csv(filePath)
    df['use'] = df['use'] * 1000
    return df


df_2014 = read_file_data(TRAINING_DATA["2014"])
df_2015 = read_file_data(TRAINING_DATA["2015"])
df_2016 = read_file_data(TRAINING_DATA["2016"])


# generate attacked data with different romal and delta average
class AttackGenerator:
    def __init__(self, file_data, start_date, end_date):
        self.file_data = file_data
        self.start_date = start_date
        self.end_date = end_date

    def perform_additive_attack(self, romal, delavg):
        file_data_copied = self.file_data.copy()
        allMeters = file_data_copied.dataid.unique()
        numberofitems = (len(allMeters) * romal)
        compromisedMeters = random.sample(allMeters.tolist(), int(numberofitems))
        mask = (file_data_copied['localminute'] >= self.start_date) & \
               (file_data_copied['localminute'] <= self.end_date) & \
               (file_data_copied['dataid'].isin(compromisedMeters))
        df = file_data_copied.loc[mask]
        file_data_copied.loc[mask, 'use'] = df['use'].apply(lambda x: x + delavg)
        return file_data_copied, numberofitems, allMeters, compromisedMeters

    def perform_deductive_attack(self, romal, delavg):
        file_data_copied = self.file_data.copy()
        allMeters = file_data_copied.dataid.unique()
        numberofitems = (len(allMeters) * romal)
        compromisedMeters = random.sample(allMeters.tolist(), int(numberofitems))
        mask = (file_data_copied['localminute'] >= self.start_date) & \
               (file_data_copied['localminute'] <= self.end_date) & \
               (file_data_copied['dataid'].isin(compromisedMeters))
        df = file_data_copied.loc[mask]
        file_data_copied.loc[mask, 'use'] = df['use'].apply(lambda x: x - delavg)
        return file_data_copied, numberofitems, allMeters, compromisedMeters

    def generate_attacks(self, del_avg_array, ro_mal_array, attack_type):
        for delavg_tr in del_avg_array:
            for romal_tr in ro_mal_array:
                if attack_type == 'ded':
                    attack_data, numberofitems, allMeters, attack_meters = self.perform_additive_attack(
                        romal_tr, delavg_tr)
                else:
                    attack_data, numberofitems, allMeters, attack_meters = self.perform_deductive_attack(
                        romal_tr, delavg_tr)

                save_directory = "C:/Users/abedz/OneDrive - Western Michigan University/PhD/Summer2021/New folder/navid w/New attacked data duration 4Mths/Test_attack_2016_2M"
                file_name = f"attacked_data_del_{delavg_tr}_romal_{romal_tr}_type_{attack_type}_2016.csv"
                file_path = os.path.join(save_directory, file_name)
                attack_data.to_csv(file_path, index=False)

                # Print the attack_meters for each file
                #print(f"Attack Meters for {file_name}: {attack_meters}")
                #print(f"Attack Meters for {file_name}: {numberofitems}")


attack_generator = AttackGenerator(df_2016, START_DATE_M, END_DATE_M)

attack_generator.generate_attacks(DEL_AVG_ARRAY, RO_MAL_ARRAY, 'ded')
