with open('volumes-sre.txt', 'r') as file:
    lines = file.readlines()

with open('volumes-sre-formatted.csv', 'w') as output_file:
    output_file.write("NAMESPACE,NAME,STATUS,VOLUME,CAPACITY,ACCESS MODES,STORAGECLASS,AGE\n")
    
    for line in lines:
        columns = line.split()

        if len(columns) >= 8:
            namespace = columns[0]
            name = columns[1]
            status = columns[2]
            volume = columns[3]
            capacity = columns[4]
            
            access_modes = ' '.join(columns[5:-2])
            
            storage_class = columns[-2]
            age = columns[-1]

            output_file.write(f"{namespace},{name},{status},{volume},{capacity},{access_modes},{storage_class},{age}\n")

print("Saída formatada separada em 'volumes-sre.csv'")
