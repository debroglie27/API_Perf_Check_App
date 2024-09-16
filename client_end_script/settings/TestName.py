quizid='CS404.GU'
if __name__=="__main__":
    testname = open("settings/TestName.py","r")
    testname.readline()
    name = input("Enter the name of the quiz instance : ")
    content= "quizid='"+name+"'\n"
    content=content+testname.read()
    testname.close()
    testname=open("settings/TestName.py","w")
    testname.write(content)