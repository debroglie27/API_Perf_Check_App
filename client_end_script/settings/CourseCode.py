coursecode='CS404'
if __name__=="__main__":
    testname = open("settings/CourseCode.py","r")
    testname.readline()
    name = input("Enter the name of the course : ")
    content= "coursecode='"+name+"'\n"
    content=content+testname.read()
    testname.close()
    testname=open("settings/CourseCode.py","w")
    testname.write(content)                                                                             
