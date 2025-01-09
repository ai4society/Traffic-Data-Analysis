import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('../../../sc_data/sc_loc2018.csv', low_memory=False)

df.rename(columns={'ano': 'Collision Number', 'tway': 'Trafficway', 'typ': 'Type of Record (L-Location data)',
                   'day': 'Day of Week',
                   'rai': 'On Route Auxiliary', 'loa': 'Lane Number of Collision', 'odr': 'Base Distance Direction',
                   'alc': 'Light Condition', 'wcc': 'Weather Condition',
                   'ahc': 'Road Condition', 'rsc': 'Road Surface Conition', 'hel': 'First Harmful Event Location',
                   'xwk': 'Crosswalk Indicator', 'dat': 'Date of Collision', 'als': 'On Route Street Name',
                   'jur': 'Investigating Jurisdiction Code',
                   'fat': 'Number of Fatalities', 'inj': 'Number of Non-Fatal Injuries',
                   'acd': 'Amended or Corrected Indicator', 'bir': 'Base Intersection Route Category',
                   'bra': 'Base Intersection Route Auxiliary', 'sic': 'Second Intersection Route Category',
                   'sra': 'Second Intersection Route Auxiliary', 'alsb': 'Base Intersection Street Name',
                   'bus': 'Number of Buses', 'trm': 'Number of Persons Transported Immediately',
                   'tow': 'Number of Towed Units',
                   'lat': 'Latitude of Collision (special format)', 'lon': 'Longitude of Collision (special format)',
                   'jct': 'Junction Type', 'ocf1': 'Other Contributing Factor 1', 'ocf2': 'Other Contributing Factor 2',
                   'ocf3': 'Other Contributing Factor 3',
                   'ocf4': 'Other Contributing Factor 4', 'ibus': 'School Bus Involved', 'wzn': 'Work Zone Indicator',
                   'wzt': 'Work Zone Type',
                   'wzl': 'Work Zone Location', 'wpr': 'Workers Present Indicator',
                   'bno': 'Currently Junk field, was Badge Number of Investigating Officer',
                   'tct': 'Traffic Control Type', 'unt': 'Number of Units (Vehicle and Non-Motorists)',
                   'cty': 'County of Collision',
                   'fhe': 'First Harmful Event', 'prc': 'Primary Contributing Factor', 'rct': 'On Route Category',
                   'adid': 'Alcohol/Drug Involved Driver in Collision',
                   'dlr': 'Direction of Lane', 'rtn': 'On Route Street Number', 'brn': 'Base Intersetion Street Number',
                   'srn': 'Second Intersection Street Number', 'tim': 'Military Time of Collision',
                   'bdo': 'Base Distance Offset (from collision location to the base intersection in miles)',
                   'pnt': 'Military Time of Police Notification', 'pat': 'Military Time of Police Arrival at Scene',
                   'alss': 'Second Intersection Street Name', 'hzd': 'Currently Junk field'}, inplace=True)

county_mapping = {
    1: 'Abbeville', 2: 'Aiken', 3: 'Allendale', 4: 'Anderson', 5: 'Bamberg', 6: 'Barnwell',
    7: 'Beaufort', 8: 'Berkeley', 9: 'Calhoun', 10: 'Charleston', 11: 'Cherokee', 12: 'Chester',
    13: 'Chesterfield', 14: 'Clarendon', 15: 'Colleton', 16: 'Darlington', 17: 'Dillon', 18: 'Dorchester',
    19: 'Edgefield', 20: 'Fairfield', 21: 'Florence', 22: 'Georgetown', 23: 'Greenville', 24: 'Greenwood',
    25: 'Hampton', 26: 'Horry', 27: 'Jasper', 28: 'Kershaw', 29: 'Lancaster', 30: 'Laurens',
    31: 'Lee', 32: 'Lexington', 33: 'McCormick', 34: 'Marion', 35: 'Marlboro', 36: 'Newberry',
    37: 'Oconee', 38: 'Orangeburg', 39: 'Pickens', 40: 'Richland', 41: 'Saluda', 42: 'Spartanburg',
    43: 'Sumter', 44: 'Union', 45: 'Williamsburg', 46: 'York'
}

county_category_mapping = {
    'Abbeville': 'Mostly Rural',
    'Aiken': 'Urban',
    'Allendale': 'Mostly Rural',
    'Anderson': 'Urban',
    'Bamberg': 'Mostly Rural',
    'Barnwell': 'Mostly Rural',
    'Beaufort': 'Urban',
    'Berkeley': 'Urban',
    'Calhoun': 'Rural',
    'Charleston': 'Urban',
    'Cherokee': 'Mostly Rural',
    'Chester': 'Mostly Rural',
    'Chesterfield': 'Mostly Rural',
    'Clarendon': 'Mostly Rural',
    'Colleton': 'Mostly Rural',
    'Darlington': 'Mostly Rural',
    'Dillon': 'Mostly Rural',
    'Dorchester': 'Urban',
    'Edgefield': 'Mostly Rural',
    'Fairfield': 'Mostly Rural',
    'Florence': 'Urban',
    'Georgetown': 'Mostly Rural',
    'Greenville': 'Urban',
    'Greenwood': 'Mostly Rural',
    'Hampton': 'Mostly Rural',
    'Horry': 'Urban',
    'Jasper': 'Mostly Rural',
    'Kershaw': 'Mostly Rural',
    'Lancaster': 'Urban',
    'Laurens': 'Mostly Rural',
    'Lee': 'Mostly Rural',
    'Lexington': 'Urban',
    'McCormick': 'Rural',
    'Marion': 'Mostly Rural',
    'Marlboro': 'Mostly Rural',
    'Newberry': 'Mostly Rural',
    'Oconee': 'Mostly Rural',
    'Orangeburg': 'Urban',
    'Pickens': 'Urban',
    'Richland': 'Urban',
    'Saluda': 'Mostly Rural',
    'Spartanburg': 'Urban',
    'Sumter': 'Urban',
    'Union': 'Mostly Rural',
    'Williamsburg': 'Mostly Rural',
    'York': 'Urban'
}

df['County of Collision'] = df['County of Collision'].map(county_mapping)
df['County Category'] = df['County of Collision'].map(county_category_mapping)

# Set the style and color palette
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette('tab20')

# Create the crosstab
crosstab = pd.crosstab(df['Trafficway'], df['County Category'])

# Define the mapping for x-axis labels
label_mapping = {
    1: "Two-Way,\nNot Divided",
    2: "Two-Way, Divided,\nUnprotected Median",
    3: "Two-Way,\nDivided, Barrier",
    4: "One-Way",
    8: "Other"
}

# Rename the index of crosstab
crosstab.index = crosstab.index.map(label_mapping)

# Create the stacked bar plot
fig, ax = plt.subplots(figsize=(14, 9))
crosstab.plot(kind='bar', stacked=True, ax=ax, width=0.8)

# Customize the plot with adjusted font sizes
plt.title('Traffic Way Class Distribution Across County Categories for 2018',
          fontsize=28, fontweight='bold', pad=20, loc='left')
plt.xlabel('Traffic Way Class', fontsize=24, labelpad=10)
plt.ylabel('Collision Count (log scale)', fontsize=24, labelpad=10)
plt.yscale('log')

# Rotate x-axis labels and adjust their position
plt.xticks(rotation=0, ha='center', fontsize=22)
plt.gca().tick_params(axis='both', which='major', labelsize=18)

# Customize legend
plt.legend(title='County Category', title_fontsize=26, fontsize=24, loc='upper right', 
           frameon=True, shadow=True, edgecolor='black')

# Adjust layout and save the plot
plt.tight_layout()
plt.savefig("../../output/Alive-25-analysis/road_type_2018.png", dpi=300, bbox_inches='tight')
plt.show()
