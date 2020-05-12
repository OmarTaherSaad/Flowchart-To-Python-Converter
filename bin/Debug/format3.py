import os

# import sys
'''
Start	 	Not Set
x=3	 	Not Set
Is
x>2	 	Not Set
Z=2	 	True
Ena	 	Not Set
Z=3	 	False
'''
# tokens1=["Start","x=3","Is\nx>2","Z=2","Ena","Z=3"]
# tokens2=["Not Set","Not Set","Not Set","True","Not Set","False"]
'''
Start	 	Not Set
x=3	 	Not Set
w=3	 	Not Set
T=w-x	 	Not Set
Print T	 	Not Set
Ena	 	Not Set
'''
# tokens1=["Start","x=3","w=3","T=w-x","Print T","Ena"]
# tokens2=["Not Set","Not Set","Not Set","Not Set","Not Set","Not Set"]
'''
Start	 	Not Set
Read y	 	Not Set
Read x	 	Not Set
Z=y-x	 	Not Set
Print z	 	Not Set
Gud	 	Not Set
'''
# tokens1=["Start","Read y","Read x","Z=y-x","Print Z","End"]
# tokens2=["Not Set","Not Set","Not Set","Not Set","Not Set","Not Set"]

'''
Start	 	Not Set
Read X	 	Not Set
{Ss
X > 20	 	Not Set
X=X-2	 	False
Print x	 	Not Set
Ena	 	Not Set
Print x	 	True
X=X-S	 	Not Set
'''


# tokens1=["Start","Read x","{Ss\nx>20","x=x-2","Print x","gud","Print x","X=X-2"]
# tokens2=["Not Set","Not Set","Not Set","False","Not Set","Not Set","True","Not Set"]
def adjust_token(x):
    for i in range(len(x)):
        if x[i] >= 'A' and x[i] <= 'Z':
            x[i] = x[i].lower()
    return x


def adjust_list2(l):
    for i in range(len(l)):
        if l[i] == "True":
            x = i
            while x < len(l) and l[x] != "False":
                l[x] = "True"
                x = x + 1
        elif l[i] == "False":
            x = i
            while x < len(l) and l[x] != "True":
                l[x] = "False"
                x = x + 1
    return l


def adjust_both_lists(l1, l2):
    for i in range(len(l1)):
        x = l1[i].lower()
        if len(l1[i]) == 3 and (x[0] == 'e' or x[0] == 'g' or x[1] == 'n' or x[2] == 'd'):
            index1 = i
            l1.pop(index1)
            l2.pop(index1)
            break

    return l1, l2


def formatting(tokens1, tokens2):
    file = open("output.py", "w")
    tokens2 = adjust_list2(tokens2)
    tokens1, tokens2 = adjust_both_lists(tokens1, tokens2)
    # print(tokens2)
    # print(tokens1)
    state = 0  # 0 normal input 1 if 2 for
    string_true = ""
    string_false = ""
    string_if = ""
    state_if = 0  # 1 true 2 false
    next_is_condition = 0
    for i in range(len(tokens1)):
        x = tokens1[i].lower()
        # print(x)
        if state == 1:
            if tokens2[i] == "True":

                while i < len(tokens1) and tokens2[i] == "True":
                    y = tokens1[i].lower()
                    if y[:5] == "print":
                        out = "print(" + y[6:] + ")"
                        y = out

                    if string_true != "":
                        string_true = string_true + "\n	" + y
                    else:
                        string_true = string_true + y
                    i = i + 1

                while i < len(tokens1) and tokens2[i] == "False":
                    y = tokens1[i].lower()
                    if y[:5] == "print":
                        out = "print(" + y[6:] + ")"
                        y = out
                    if string_false != "":
                        string_false = string_false + "\n	" + y
                    else:
                        string_false = string_false + y

                    i = i + 1
                state = 0
                file.write(string_if)
                file.write("	")
                file.write(string_true)
                file.write("\n")
                file.write("else:\n	")
                file.write(string_false)
                file.write("\n")
                string_true = ""
                string_false = ""
                string_if = ""
                if i == len(tokens1):
                    break
            else:
                while i < len(tokens1) and tokens2[i] == "False":
                    y = tokens1[i].lower()
                    # print(y)
                    if y[:5] == "print":
                        out = "print(" + y[6:] + ")"
                        y = out
                    # print(x)
                    if string_false != "":
                        string_false = string_false + "\n	" + y
                    else:
                        string_false = string_false + y

                    i = i + 1
                # print(string_false)

                # print(string_false)
                while i < len(tokens1) and tokens2[i] == "True":
                    y = tokens1[i].lower()
                    if y[:5] == "print":
                        out = "print(" + y[6:] + ")"
                        y = out
                    if string_true != "":
                        string_true = string_true + "\n	" + y
                    else:
                        string_true = string_true + y
                    i = i + 1
                # print(string_true)
                state = 0
                file.write(string_if)
                file.write("	")
                file.write(string_true)
                file.write("\n")
                file.write("else:\n	")
                file.write(string_false)
                file.write("\n")
                string_true = ""
                string_false = ""
                string_if = ""
                if i == len(tokens1):
                    break

        elif (x == "start") and state == 0:  # start
            continue;
        elif state == 0 and (x[:3] == "{ss" or x[:2] == "is" or tokens2[i] == "Bool"):
            # print("here is 1")
            state = 1
            if (x[:3] == "{ss" or x[:3] == "is"):
                string_if = "if " + x[4:] + ":\n"
            else:
                string_if = "if " + x[3:] + ":\n"
            '''
			if tokens2_ex1[i+1]=="True":
				state_if=1
			elif tokens2_ex1[i+1]=="False":
				state_if=2		
			'''
        elif x[:4] == "read" and state == 0:
            file.write(x[5:]);
            file.write("=int(input())\n")
        elif (x[0] == "e") and (x[1] == "n") and state == 0:
            continue

        elif state == 0:
            # print("state is 0")
            if x[:5] == "print":
                out = "print(" + x[6:] + ")"
                file.write(out)
                file.write("\n")
            else:
                file.write(x)
                file.write("\n")

    '''
	#handle last if before termination
	print(state_if)
	print(state)
	print(string_false)
	print(string_if)
	print(string_true)
	if state==1 and state_if==1:
		if string_false !="":#we have finished parsing if
				state=0
				file.write(string_if)
				file.write("	")
				file.write(string_true)
				file.write("\n")
				file.write("elif:\n	")
				file.write(string_false)
				file.write("\n")
				string_true=""
				string_false=""
				string_if=""
				state_if=0
	elif state==1 and state_if==2:
		if string_true !="":#we have finished parsing if
				state=0
				file.write(string_if)
				file.write("	")
				file.write(string_true)
				file.write("\n")
				file.write("elif:\n	")
				file.write(string_false)
				file.write("\n")
				string_true=""
				string_false=""
				string_if=""
				state_if=0
	'''
    file.close()

    # return os.path.abspath(os.getcwd()) + '/output.py'
    return 'output.py'
# os.system("python test.py")

# argv=sys.argv
# image_path=argv[1]
# print(image_path)

# print(formatting(tokens1,tokens2))
