import json
admin_info = {}


# with open("access_control.json", 'r') as f:
#         access_control = json.load(f)


# print(access_control)    

# name =  "Tursunov Toshmat"
# chat_id = 172248234

# # for e in access_control:
# # 	if e["full_name"] == name:
# # 		e["id"] = chat_id

# # with open("access_control.json", 'w') as f:
# # 	json.dump(access_control,f, indent=4)	


# print(access_control)    


# with open("register_access.json", 'r') as f:
#         register_access = json.load(f)

# group = "314-17"

# if group in register_access:
# 	gr_stu = register_access[group]

# full_n = "Eshmat"
# if not full_n in gr_stu:
# 	print("Fuuuu")

# print(gr_stu)


full_name = "Saidmahmudov Saidkarim"

fam, ism = full_name.split(" ")

print(ism)