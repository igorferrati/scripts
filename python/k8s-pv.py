with open('pv-sre.txt', 'r') as file:
    lines = file.readlines()

with open('pv-sre.csv', 'w') as output_file:
    output_file.write("NAME,CAPACITY,ACCESS MODES,RECLAIM POLICY,STATUS,CLAIM,STORAGECLASS,REASON,AGE\n")

    for line in lines[1:]:
        name = line[0:41].strip()
        capacity = line[41:54].strip()
        access_modes = line[54:69].strip()
        reclaim_policy = line[69:86].strip()
        status = line[86:97].strip()
        claim = line[97:211].strip()
        storage_class = line[211:226].strip()
        reason = line[226:235].strip()
        age = line[235:].strip()

        output_file.write(f"{name},{capacity},{access_modes},{reclaim_policy},{status},{claim},{storage_class},{reason},{age}\n")

print("Saída formatada separada em 'pv-sre.csv'")

