
import pandas as pd

scraped_df = pd.read_excel (r'estates_excel.xlsx')

scraped_df.dtypes
cols=scraped_df.columns

selected_columns = scraped_df[["blz","lat","lng","price","size","rooms","Zustand_Baujahr",
                               "Zustand_Zustand",]]

simple_df = selected_columns.copy()

simple_df=simple_df.dropna(axis=0, how="any")

simple_df=simple_df.drop([20,116])

simple_df=simple_df.reset_index()

simple_df = simple_df.drop('index', 1)
simple_df = simple_df.drop('blz', 1)


#################### dataset created
## dummies
simple_df.columns

dum_cols=["Zustand_Zustand"]
dummy_df=pd.get_dummies(simple_df,columns=dum_cols)

dummy_df.columns
dummy_df = dummy_df[['lat', 'lng', 'size', 'rooms', 'Zustand_Baujahr',
       'Zustand_Zustand_Erstbezug', 'Zustand_Zustand_Gepflegt',
       'Zustand_Zustand_Modernisiert', 'Zustand_Zustand_Nach Vereinbarung',
       'Zustand_Zustand_Neuwertig', 'Zustand_Zustand_Projektiert',
       'Zustand_Zustand_Rohbau', 'Zustand_Zustand_SanierungsbedÃ¼rftig',
       'Zustand_Zustand_TEIL_VOLLSANIERT',
       'Zustand_Zustand_Teil / Vollrenoviert',
       'Zustand_Zustand_Teil / VollrenovierungsbedÃ¼rftig',
       'Zustand_Zustand_Vollsaniert','price']]

dummy_df.to_csv("dummy_df.csv")


##############################################



selected_columns = scraped_df[["lat","lng","price","size","rooms","Zustand_Baujahr",
                               "Ausstattung_Heizungsart_ETAGE","Ausstattung_Heizungsart_FuÃŸbodenheizung",
                               "Ausstattung_Heizungsart_Zentralheizung",
                               "Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung"]]

simple_df = selected_columns.copy()



simple_df = simple_df[simple_df['lat'].notna()]
simple_df = simple_df[simple_df['size'].notna()]
simple_df = simple_df[simple_df['rooms'].notna()]
simple_df = simple_df[simple_df['Zustand_Baujahr'].notna()]

simple_df=simple_df.drop([20,116])


simple_df=simple_df.fillna(0)

simple_df["Ausstattung_Heizungsart_ETAGE"] = simple_df["Ausstattung_Heizungsart_ETAGE"].astype(int)
simple_df["Ausstattung_Heizungsart_FuÃŸbodenheizung"] = simple_df["Ausstattung_Heizungsart_FuÃŸbodenheizung"].astype(int)
simple_df["Ausstattung_Heizungsart_Zentralheizung"] = simple_df["Ausstattung_Heizungsart_Zentralheizung"].astype(int)
simple_df["Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung"] = simple_df["Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung"].astype(int)

simple_df.to_csv("ausstattung_data.csv")



#################################################


import pandas as pd

scraped_df = pd.read_excel (r'estates_excel.xlsx')

scraped_df.dtypes
cols=scraped_df.columns

selected_columns = scraped_df[["blz","lat","lng","price","size","rooms","Zustand_Baujahr",
                               "Zustand_Zustand","Ausstattung_Heizungsart_ETAGE",
                               "Ausstattung_Heizungsart_FuÃŸbodenheizung",
                               "Ausstattung_Heizungsart_Zentralheizung",
                               "Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung"]]

simple_df = selected_columns.copy()

simple_df = simple_df[simple_df['lat'].notna()]
simple_df = simple_df[simple_df['size'].notna()]
simple_df = simple_df[simple_df['rooms'].notna()]
simple_df = simple_df[simple_df['Zustand_Baujahr'].notna()]
simple_df = simple_df[simple_df['Zustand_Zustand'].notna()]

simple_df=simple_df.drop([20,116])

simple_df=simple_df.reset_index()

simple_df = simple_df.drop('index', 1)
simple_df = simple_df.drop('blz', 1)


simple_df=simple_df.fillna(0)

simple_df["Ausstattung_Heizungsart_ETAGE"] = simple_df["Ausstattung_Heizungsart_ETAGE"].astype(int)
simple_df["Ausstattung_Heizungsart_FuÃŸbodenheizung"] = simple_df["Ausstattung_Heizungsart_FuÃŸbodenheizung"].astype(int)
simple_df["Ausstattung_Heizungsart_Zentralheizung"] = simple_df["Ausstattung_Heizungsart_Zentralheizung"].astype(int)
simple_df["Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung"] = simple_df["Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung"].astype(int)

#################### dataset created
## dummies
simple_df.columns

dum_cols=["Zustand_Zustand"]
dummy_df=pd.get_dummies(simple_df,columns=dum_cols)

dummy_df.columns
dummy_df = dummy_df[['lat', 'lng', 'size', 'rooms', 'Zustand_Baujahr',
       'Zustand_Zustand_Erstbezug', 'Zustand_Zustand_Gepflegt',
       'Zustand_Zustand_Modernisiert', 'Zustand_Zustand_Nach Vereinbarung',
       'Zustand_Zustand_Neuwertig', 'Zustand_Zustand_Projektiert',
       'Zustand_Zustand_Rohbau', 'Zustand_Zustand_SanierungsbedÃ¼rftig',
       'Zustand_Zustand_TEIL_VOLLSANIERT',
       'Zustand_Zustand_Teil / Vollrenoviert',
       'Zustand_Zustand_Teil / VollrenovierungsbedÃ¼rftig',
       'Zustand_Zustand_Vollsaniert','Ausstattung_Heizungsart_ETAGE',
       'Ausstattung_Heizungsart_FuÃŸbodenheizung',
       'Ausstattung_Heizungsart_Zentralheizung',
       'Ausstattung_Heizungsart_Zentralheizung_FuÃŸbodenheizung','price']]

dummy_df.dtypes


dummy_df.to_csv("aus_zus_dummy_data.csv")





