quizid='CS007.27802MV'
if __name__=="__main__":
    testname = open("TestName.py","r")
    testname.readline()
    name = input("Enter the name of the quiz instance : ")
    content= "quizid='"+name+"'\n"
    content=content+testname.read()
    testname.close()
    testname=open("TestName.py","w")
    testname.write(content)