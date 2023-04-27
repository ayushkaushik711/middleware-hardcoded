import os
import regex as re

hardCodedString = r"(['\"])(?:(?!\1).)*?\1"
hardCodedNumber = r"[-+]?\d*\.?\d+"
hardCodedArray = r"\[[^[\]]*(?:(?R)[^[\]]*)*\]"
hardCodedObject = r"\{[^{}]*(?:(?R)[^{}]*)*\}"
# hardCodedFunction = r"function\s*\([^)]*\)\s*\{[^{}]*(?:(?R)[^{}]*)*\}"
# hardCodedClass = r"class\s+\w+\s*\{[^{}]*(?:(?R)[^{}]*)*\}"
hardCodedVariable = r"(const|let|var)\s+\w+\s*=\s*(?!require|import)\S+"
hardCodedEnvVariable = r"process\.env\.\w+"
hardCodedUrl = r"(https?|ftp|file)://\S+"
hardCodedFilePath = r"['\"].*(?<!\\)['\"]"
hardCodedPassword = r"(password|passwd|pwd)[\s:=]+(['\"])[^'\"]*\2"                   

importRequireStatement = r'(import\s+[\w{},*\s]+\s+from\s+[\'"][\w\s./-]+[\'"])|(require\s*\([\'"][\w\s./-]+[\'"]\))'

regexes = {
    hardCodedString: "hardcoded string",
    hardCodedNumber: "hardcoded number",
    hardCodedArray: "hardcoded array",
    hardCodedObject: "hardcoded object",
    # hardCodedFunction: "hardcoded function",
    # hardCodedClass: "hardcoded class",
    hardCodedVariable: "hardcoded variable",
    hardCodedEnvVariable: "hardcoded environment variable",
    hardCodedUrl: "hardcoded URL",
    hardCodedFilePath: "hardcoded file path",
    hardCodedPassword: "hardcoded password",
}

def isJavascriptFile(inputFile):
    return inputFile.endswith('.js') or inputFile.endswith('.jsx')


def findPatternsInRegex(inputFile, outputFile):
    if not isJavascriptFile(inputFile):
        return    
    f_out = open(outputFile, 'a')
    with open(inputFile, 'r') as f_in:
        lines = f_in.readlines()
        for i, line in enumerate(lines):
            for pattern, description in regexes.items():
                match = re.search(pattern, line)
                if match:
                    line_number = i+1
                    if description == "hardcoded string" :
                        match2 = re.search(importRequireStatement, line)
                        if(match2):
                            continue
                    output_str = f"{inputFile}:{line_number}:{description}:{line}"
                    f_out.write(output_str)
                    break


def searchFiles(inputFiles, outputFiles):
    excludedFiles = ["node_modules", "public",".gitignore",".husky","README.md","package.json","package-lock.json","uat-scripts",".github",".DS_Store",".git"]

    for fileName in os.listdir(inputFiles):
        if fileName in excludedFiles:
            continue
        else :
            inputFilePath=os.path.join(inputFiles, fileName) # inputFilePath
            outputFilePath=os.path.join(outputFiles,fileName) # outputFilePath

            newFile = 'duplicate.txt'
            newFilePath = os.path.join(outputFiles,newFile)
            if os.path.isdir(inputFilePath):
                if not os.path.exists(outputFilePath):
                    os.makedirs(outputFilePath)
                    file = open(newFilePath, "w") # initialise duplicate.txt file in desired folder
                searchFiles(inputFilePath,outputFilePath)

            else :
                findPatternsInRegex(inputFilePath,newFilePath)
                # print(filePath)
        

inputFile = 'microservices-middleware/'
# inputFile = "planner"
outputFile = 'duplicates/'
searchFiles(inputFile,outputFile)
