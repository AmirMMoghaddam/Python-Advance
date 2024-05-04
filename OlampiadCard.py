input_count = int(input())
StudentList = []
for i in range(input_count):
    Candidate = input().split(".")
    Candidate[1]=Candidate[1].lower()
    Candidate[1]=Candidate[1].capitalize()
    StudentList.append(Candidate)

for student in StudentList:
    if student[0] == 'f':
        print(student[0]," ",student[1]," ",student[2])
for student in StudentList:
    if student[0] == 'm':
        print(student[0]," ",student[1]," ",student[2])  

   