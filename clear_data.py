def save_csv(file_path, csv_list):
    with open(file_path.replace('.txt','.csv'), 'w') as f:
        for line in csv_list:
            f.write(line)


def clear_uf(file_path):
    csv_list = ['SIGLA,UF,NAO_RECEBE,RECEBE,SEM_RESPOSTA,TOTAL\n']
    # read txt file
    with open(file_path, 'r') as f:
        data = f.readlines()
        for i, line in enumerate(data):
            if '-' in line:
                csv_list.append(line.replace('-',' ').replace(' ',','))
    save_csv(file_path, csv_list)

def clear_br(file_path):
    csv_list = ['BRASIL,NAO_RECEBE,RECEBE,SEM_RESPOSTA,TOTAL\n']
    # read txt file
    with open(file_path, 'r') as f:
        data = f.readlines()
        line = data[3]
        csv_list.append(line.replace(' ',','))

    save_csv(file_path, csv_list)