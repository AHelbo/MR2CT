# list = ["1PA014-01","1PA014-02","1PA014-10","1PA014-03"]
test_list = ["1PA014-","1PA014-","1PA014-","1PA014-"]

new_list = []
for i,elm in zip([1,2,10,3],test_list):
    new_list.append(f"elm{i:03}")

print(new_list)

new_list.sort()

print(new_list)