coursecode='CS007'
if __name__=="__main__":
    testname = open("CourseCode.py","r")
    testname.readline()
    name = input("Enter the name of the course : ")
    content= "coursecode='"+name+"'\n"
    content=content+testname.read()
    testname.close()
    testname=open("CourseCode.py","w")
    testname.write(content)                                                                             