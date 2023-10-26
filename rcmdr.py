import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors

def run(wt, age, sex, icd, cond, med):
    


# Load data from peptic4.csv
    data = pd.read_csv("peptic.csv")    
    proc_data = data.drop(['medication','clusters', 'Unnamed: 0'], axis=1)
    
    knn = NearestNeighbors(n_neighbors=5, metric='cosine')
    knn.fit(proc_data)
    
    new_d = [{'gender':sex, 'anchor_age':age,'icd_code':icd, 'result_value':wt}]
    new_d = pd.DataFrame(new_d)
    #new_d = new_d.drop(columns=new_d.columns[0])
    try:
        
        for i in new_d['anchor_age'].index:
            if int(new_d['anchor_age'][i]) >= 1 or int(new_d['anchor_age'][i]) <= 65:
                 new_d['anchor_age'][i] = 0
            elif int(new_d['anchor_age'][i]) > 65:
                 new_d['anchor_age'][i] = 1
            else:
                err = 'Invalid age value'
                return '', err
        #distances, indices = knn.kneighbors(new_d)
    except ValueError:
        err = "Please check that all fields are filled"
        return '', err
    
    if wt == '' or int(wt) < 1:
        err = 'Invalid weight value'
        return '', err
    for i in new_d['gender'].index:
        if  new_d['gender'][i] == 'male':        
            new_d['gender'][i] = 1
        elif new_d['gender'][i] == 'female':
            new_d['gender'][i] = 0
        else:
            err = 'Select a sex value'
            return '', err
    for i in new_d['icd_code'].index:
        if new_d['icd_code'][i].upper() == 'V1271':
            new_d['icd_code'][i] = 11
        elif new_d['icd_code'][i].upper() == 'Z8711':
            new_d['icd_code'][i] = 12
        elif new_d['icd_code'][i].upper() == 'K274':
            new_d['icd_code'][i] = 7
        elif new_d['icd_code'][i].upper() == '53370':
            new_d['icd_code'][i] = 5
        elif new_d['icd_code'][i].upper() == '53340':
            new_d['icd_code'][i] = 3
        elif new_d['icd_code'][i].upper() == '53350':
            new_d['icd_code'][i] = 4
        elif new_d['icd_code'][i].upper() == 'K277':
            new_d['icd_code'][i] = 10
        elif new_d['icd_code'][i].upper() == 'K276':
            new_d['icd_code'][i] = 9
        elif new_d['icd_code'][i].upper() == 'K270':
            new_d['icd_code'][i] = 6
        elif new_d['icd_code'][i].upper() == '53300':
            new_d['icd_code'][i] = 0
        elif new_d['icd_code'][i].upper() == 'K275':
            new_d['icd_code'][i] = 8
        elif new_d['icd_code'][i].upper() == '53311':
            new_d['icd_code'][i] = 2
        elif new_d['icd_code'][i].upper() == '53310':
            new_d['icd_code'][i] = 1
        else:
            err = "ICD_Code is Invalid for Peptic Ulcer"
            return '', err
    distances, indices = knn.kneighbors(new_d)
    new_patient_cluster = data.iloc[indices.flatten()]['clusters'].values[0]
    #new_patient_cluster = clusters[indices]
    #print(new_patient_cluster)
    drugs_for_cluster = data[data['clusters'] == new_patient_cluster]['medication'].unique()

    drugs_for_cluster = drugs_for_cluster.tolist()
    for i in range(len(drugs_for_cluster)):
        if drugs_for_cluster[i] == 2:
            drugs_for_cluster[i] = 'Omeprazole'
        if drugs_for_cluster[i] == 1:
            drugs_for_cluster[i] = 'Glycopyrrolate'
        if drugs_for_cluster[i] == 0:
            drugs_for_cluster[i] = 'Famotidine'
        if drugs_for_cluster[i] == 4:
            drugs_for_cluster[i] = 'Ranitidine'
        if drugs_for_cluster[i] == 3:
            drugs_for_cluster[i] = 'Pantoprazole'
    print(drugs_for_cluster, sep=(', '))
    
    #Data for the Knowledge based filtering
    drug_info_check = {'Pantoprazole':[['acalabrutinib','atazanavir', 'nelfinavir', 'rilpivirine','belumosudil', 
                                         'gefitinib', 'infigratinib', 'pazopanib', 'pexidartinib', 'selpercatinib',
                                         'sotorasib','dacomitinib', 'neratinib','dasatinib', 'erlotinib','methotrexate'],
                                     ['clostridium difficile-associated diarrhea (cdad)','hepatic impairment','osteoporosis',
                                      'hypomagnesemia','diarrhea','seizures' ]],
                        'Omeprazole':[['mavacamten','acalabrutinib','atazanavir', 'nelfinavir', 'rilpivirine','belzutifan', 
                                      'cilostazol', 'citalopram','clipodogrel','dasatinib', 'erlotinib','dacomitinib', 'neratinib',
                                      'belumosudil', 'gefitinib', 'infigratinib', 'pazopanib', 'pexidartinib', 'selpercatinib', 
                                       'sotorasib','methotrexate','tacrolimus'],
                                      ['diarrhea','hypomagnesemia ','osteoporosis','pseudomembranous colitis','liver disease', 'lupus']],
                        'Famotidine':[['tizanidine','bepridil', 'cisapride', 'dronedarone', 'levoketoconazole', 'mesoridazine', 'pimozide', 
                                       'piperaquine', 'saquinavir', 'sparfloxacin', 'terfenadine', 'thioridazine', 'ziprasidone'],
                                      ['gastrointestinal hemorrhage','congenital long qt syndrome', 'cardiac diseases', 
                                        'conduction abnormalities', 'electrolyte disturbances', 'kidney disease']],
                        'Ranitidine':[['siponimod', 'cimetidine', 'famotidine', 'nizatidine', 'atazanavir', 'dasatinib'],
                                      ['gastrointestinal hemorrhage', 'porphyria','headache', 'constipation', 'nausea', 'vomiting', 'stomach pain']],
                        'Glycopyrrolate':[['topiramate', 'zonisamide'],
                                          ['glaucoma','urinary retention','infectious diarrhea','myasthenia gravis',
                                           'ulcerative colitis', 'psychoses', "down's syndrome", 'hypertension']]}
    final_rec = []
    cond = cond[0].split(',')
    med = med[0].split(',')

    for i in drugs_for_cluster:
        chk = 'valid'
        if i in drug_info_check.keys():
            for cm in med:            
                if cm.lower().strip() in drug_info_check[i][0]:
                    chk = 'invalid'
            for mc in cond:                
                if mc.lower().strip() in drug_info_check[i][1]:
                    chk = 'invalid'
            if chk == 'valid':
                    final_rec.append(i)
    print(final_rec)
    fin_res = []
    for i in final_rec:
        x = i+(', ')
        fin_res.append(x)
    err = ''
    return fin_res, err

