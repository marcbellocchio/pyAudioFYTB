'''
Created on 28 déc. 2017

@author: mbl
'''
import unittest


class Test(unittest.TestCase):


    def testName(self):
        print("test strip replace string")
        mystr = "Ultimate Best of Justice / 2006-2011 / HQ Audio quality  \\ tititit"
        outstring = mystr.strip("/")
        print(outstring)
        outstring1 =  mystr.replace("/","_")
        outstring1 =  outstring1.replace("\\","_")
        print(outstring1)
        print("end")


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()