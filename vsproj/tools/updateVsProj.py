# coding=utf-8
import getopt, sys, re, os, json, hashlib
from xml.etree import ElementTree

# -------------------------------------------------------------------------------
repattern = re.compile(r'.*[\.]{1}([^\.]+)')
htypefilter = ['h', 'hpp', 'inl']
ctypefilter = ['cc', 'cpp', 'c']
alltypefilter = htypefilter[:]
alltypefilter.extend(ctypefilter)


def getAbsPath(path):
    return os.path.abspath(path)


def adjustPath(outDir):
    outDir = outDir.replace('\\', '/')
    if len(outDir) > 0 and outDir[-1] == '/':
        outDir = outDir[:-1]
    return outDir


def curFileDir():
    path = getAbsPath(sys.argv[0])
    if os.path.isfile(path):
        path = os.path.dirname(path)
    return adjustPath(path)


def getFileList(path, fileList, filters=alltypefilter):
    for parent, dirnames, filenames in os.walk(path):
        for filename in filenames:
            match = repattern.match(filename)
            if match:
                filetype = match.groups()[0]
                if filetype in filters:
                    fileList.append(adjustPath(os.path.join(parent, filename)))


def saveFile(path, data):
    file = open(path, 'w')
    if file:
        file.write(data)
        file.close()
        print('save file: %s ok!' % path) 


def analysisConfig(path):
    configInfo = {}
    try:
        file = open(path)
        if file:
            configInfo = json.load(file)
    except Exception as e:
        print('analysis config exception: %s' % e)
    finally:
        return configInfo


def appendAnalysInfo(analysisInfo, type, info):
    if type in htypefilter:
        if 'ClInclude' not in analysisInfo:
            analysisInfo['ClInclude'] = []
        analysisInfo['ClInclude'].append(info)
    elif type in ctypefilter:
        if 'ClCompile' not in analysisInfo:
            analysisInfo['ClCompile'] = []
        analysisInfo['ClCompile'].append(info)
    else:
        if type not in analysisInfo:
            analysisInfo[type] = []
        for tmp in analysisInfo[type]:
            if tmp == info:
                return
        analysisInfo[type].append(info)


def _fileCompare(fileName, cfgKey):
    if fileName == cfgKey:
        return True
    cfgLen = len(cfgKey)
    fileLen = len(fileName)
    if cfgLen <= 0:
        return False
    cfgHead = (cfgKey[0] == '*')
    cfgEnd = (cfgKey[-1] == '*')
    if cfgHead and cfgEnd:
        return fileName.find(cfgKey[1:-1]) >= 0
    elif cfgHead and fileLen >= cfgLen:
        return fileName[fileLen - cfgLen + 1:] == cfgKey[1:]
    elif cfgEnd and fileLen >= cfgLen:
        return fileName[0:cfgLen - 1] == cfgKey[0:-1]
    return False


def fileCompare(fileName, nameHead, cfgKey):
    if _fileCompare(fileName, cfgKey) == True:
        return True
    if _fileCompare(nameHead, cfgKey) == True:
        return True
    return False


def getUnfoldFilter(projPath, filePath, nskip):
    opath = ''
    strkey = os.path.relpath(filePath, projPath)
    if strkey and len(strkey) > 0:
        strkeys = strkey.lower().replace('\\', '/').split('/')
        for key in strkeys[nskip:-1]:
            if key not in ['.', '..']:
                opath = opath + key + '\\'
    if len(opath) > 0 and opath[-1] == '\\':
        opath = opath[:-1]
    return opath


def getFileFilter(projPath, file, filename, filterCfg):
    rtnCfg = {
        'firstlvl': False
    }
    if filterCfg != None:
        if 'unfold' in filterCfg and filterCfg['unfold'] == True:
            nskip = 0
            if 'skip' in filterCfg:
                nskip = filterCfg['skip']
            rtnCfg['filter'] = getUnfoldFilter(projPath, file, nskip)
        else:
            if 'filters' in filterCfg:
                filename = filename.lower()
                nameHead = '.'.join(filename.split('.')[:-1])
                for node in filterCfg['filters']:
                    if node == None or 'key' not in node or 'list' not in node:
                        continue
                    filter, cfgs = node['key'], node['list']
                    addFilter = False
                    if 'nokey' not in node or node['nokey'] < 1:
                        if nameHead == filter:
                            rtnCfg['filter'] = filter
                            addFilter = True
                    if addFilter == False:
                        for cfgKey in cfgs:
                            if fileCompare(filename, nameHead, cfgKey):
                                rtnCfg['filter'] = filter
                                break
                    if 'filter' in rtnCfg:
                        break

            if 'finally' in filterCfg and 'filter' not in rtnCfg:
                rtnCfg['filter'] = filterCfg['finally']

            if 'firstlvl' in filterCfg and rtnCfg['filter'] in filterCfg['firstlvl']:
                rtnCfg['firstlvl'] = True

    return rtnCfg


def fileArchiving(projPath, file, filterCfg, analysisInfo):
    fileName = file.split('/')[-1]
    filter = getFileFilter(projPath, file, fileName, filterCfg)
    filter['name'] = file
    appendAnalysInfo(analysisInfo, fileName.split('.')[-1], filter)
    appendAnalysInfo(analysisInfo, 'Filter', filter)


def analysisFileDirs(basePath, outDir, dirPath, analysisInfo, filterCfg):
    fileList = []
    getFileList(getAbsPath('%s/%s' % (basePath, dirPath)), fileList)
    projPath = getAbsPath('%s/%s' % (basePath, outDir))
    for file in fileList:
        fileArchiving(projPath, file, filterCfg, analysisInfo)


def analysisFiles(basePath, outDir, files, analysisInfo, filterCfg):
    projPath = getAbsPath('%s/%s' % (basePath, outDir))
    for file in files:
        fileArchiving(projPath, getAbsPath(file), filterCfg, analysisInfo)


def readXmlFile(path):
    root = None
    try:
        root = ElementTree.parse(path)
    except Exception as e:
        print('read xml file error: %s' % e)
    finally:
        return root


def get_namespace(element):
    m = re.match('\{(.*)\}', element.tag)
    return m.groups()[0] if m else ''


def xmlIndent(elem, level=0):
    i = "\n" + level * '  '
    elemLen = len(elem)
    if elemLen:
        if not elem.text or not elem.text.strip():
            elem.text = i + '  '
        for index in range(elemLen):
            e = elem[index]
            xmlIndent(e, level + 1)
            if not e.tail or not e.tail.strip():
                if index == elemLen - 1:
                    e.tail = i
                else:
                    e.tail = i + '  '
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i
    return elem


def getXmlInfo(xml):
    data = ElementTree.tostring(xml.getroot(), encoding='utf-8')
    return '<?xml version="1.0" encoding="utf-8"?>\n' + bytes.decode(data).replace('ns0:', '').replace(':ns0', '')


def saveXmlPrjNode(itemGroup, analysisInfo, key, cbKey, cbItem):
    itemGroup.clear()
    addNode = False
    if key in analysisInfo:
        keys = {}
        for item in analysisInfo[key]:
            rtn = cbKey(item, key)
            if rtn != None:
                if type(rtn) is list:
                    for tkey in rtn:
                        keys[tkey] = item
                else:
                    keys[rtn] = item
        for xkey in sorted(keys.keys()):
            cbItem(itemGroup, key, xkey, keys[xkey])
            addNode = True
    if addNode == True:
        xmlIndent(itemGroup, 1)
    return addNode


def excludeFile(filename, cfgs):
    filename = filename.lower()
    nameHead = '.'.join(filename.split('.')[:-1])
    for cfgKey in cfgs:
        if fileCompare(filename, nameHead, cfgKey) == True:
            return True
    return False


def saveOutFile_proj(basePath, outDir, project, analysisInfo, excludeCfg):
    projectDir = getAbsPath('%s/%s' % (basePath, outDir))
    projectFile = '%s/%s.vcxproj' % (projectDir, project)
    # xml读取文件
    xml = readXmlFile(projectFile)
    if xml == None:
        print('load project %s vcxproj file failed, check file exist!' % project)
        return
    root = xml.getroot()
    namespace = get_namespace(root)

    def projKeyFunc(item, key):
        strkey = os.path.relpath(item['name'], projectDir)
        if excludeCfg != None and excludeFile(strkey, excludeCfg) == True:
            strkey = None
        return strkey

    def projItemFunc(itemGroup, key, xkey, item):
        ElementTree.SubElement(itemGroup, '{%s}%s' % (namespace, key), {
            'Include': xkey
        })
    
    addModelOk = {}
    def replaceItemGroup(itemGroup, key):
        if itemGroup.find('{%s}%s' % (namespace, key)) != None:
            saveXmlPrjNode(itemGroup, analysisInfo, key, projKeyFunc, projItemFunc)
            addModelOk[key] = True
            
    def addItemGroup(key):
        itemGroup = ElementTree.Element('ItemGroup')
        if saveXmlPrjNode(itemGroup, analysisInfo, key, projKeyFunc, projItemFunc) == True:
            root.append(itemGroup)
        addModelOk[key] = True

    for itemGroup in root.findall('{%s}ItemGroup' % namespace):
        if 'Label' in itemGroup.attrib:
            continue
        replaceItemGroup(itemGroup, 'ClInclude')
        ElementTree.SubElement(itemGroup, 'DataFilesToCopyRemotely', { 'Include': "@(ClInclude)" })
        replaceItemGroup(itemGroup, 'ClCompile')

    for key in ['ClInclude', 'ClCompile']:
        if key not in addModelOk:
            addItemGroup(key)
        
    # 保存xml文件
    saveFile(projectFile, getXmlInfo(xml))


def saveOutFile_filter(basePath, outDir, project, analysisInfo, excludeCfg, filterConfig):
    projectDir = getAbsPath('%s/%s' % (basePath, outDir))
    projectFile = '%s/%s.vcxproj.filters' % (projectDir, project)

    projUnfold = False
    if 'unfold' in filterConfig:
        projUnfold = filterConfig['unfold']
        
    # xml读取文件
    xml = readXmlFile(projectFile)
    if xml == None:
        print('load project %s vcxproj.filters file failed, check file exist!' % project)
        return
    root = xml.getroot()
    namespace = get_namespace(root)

    def filterGetFilter(base, item):
        if 'firstlvl' in item and item['firstlvl'] == True:
            return item['filter']
        else:
            if projUnfold == False:
                return '%s\%s' % (base, item['filter'])
            else:
                return item['filter']

    def filterGetFilterS(item):
        if 'firstlvl' in item and item['firstlvl'] == True:
            return item['filter']
        else:
            rtn = []
            if projUnfold == False:
                for base in ['include', 'src']:
                    rtn.append(base)
                    rtn.append('%s\%s' % (base, item['filter']))
            else:
                sfilter = item['filter']
                tfilter = ''
                for afilter in sfilter.split('\\'):
                    if len(tfilter) > 0:
                        tfilter = '%s\%s' % (tfilter, afilter)
                    else:
                        tfilter = afilter
                    rtn.append(tfilter)
            return rtn

    def filterKeyFunc(item, key):
        if key == 'Filter':
            return filterGetFilterS(item)
        strkey = os.path.relpath(item['name'], projectDir)
        if excludeCfg != None and excludeFile(strkey, excludeCfg) == True:
            strkey = None
        return strkey

    def getMd532(info):
        hashkey = hashlib.md5(info.encode('utf8')).hexdigest()
        return '%s-%s-%s-%s-%s' % (hashkey[:8], hashkey[8:12], hashkey[12:16], hashkey[16:20], hashkey[20:])

    def filterItemFunc(itemGroup, key, xkey, item):
        if len(xkey) > 0:
            elem = ElementTree.SubElement(itemGroup, '{%s}%s' % (namespace, key), {
                'Include': xkey
            })
            if key == 'ClInclude':
                vtxt = filterGetFilter('include', item)
                if len(vtxt) > 0:
                    ElementTree.SubElement(elem, '{%s}Filter' % namespace).text = vtxt
            elif key == 'ClCompile':
                vtxt = filterGetFilter('src', item)
                if len(vtxt) > 0:
                    ElementTree.SubElement(elem, '{%s}Filter' % namespace).text = vtxt
            elif key == 'Filter' and len(xkey) > 0:
                ElementTree.SubElement(elem, '{%s}UniqueIdentifier' % namespace).text = '{%s}' % getMd532(xkey)
        
    addModelOk = {}
    def replaceItemGroup(itemGroup, key):
        if itemGroup.find('{%s}%s' % (namespace, key)) != None:
            saveXmlPrjNode(itemGroup, analysisInfo, key, filterKeyFunc, filterItemFunc)
            addModelOk[key] = True
            
    def addItemGroup(key):
        itemGroup = ElementTree.Element('ItemGroup')
        if saveXmlPrjNode(itemGroup, analysisInfo, key, filterKeyFunc, filterItemFunc) == True:
            root.append(itemGroup)
        addModelOk[key] = True

    for itemGroup in root.findall('{%s}ItemGroup' % namespace):
        if 'Label' in itemGroup.attrib:
            continue
        replaceItemGroup(itemGroup, 'ClInclude')
        replaceItemGroup(itemGroup, 'ClCompile')
        replaceItemGroup(itemGroup, 'Filter')

    for key in ['ClInclude', 'ClCompile', 'Filter']:
        if key not in addModelOk:
            addItemGroup(key)

    # 保存xml文件
    saveFile(projectFile, getXmlInfo(xml))


##========================================================================================
def usage():
    print(
        "Usage %s: [-c|-p|-o|-h] [--config|--project|--out|--help] args ..." % sys.argv[0])


##========================================================================================
if __name__ == '__main__':
    bexit = False
    configFile = 'filterConfig.json'
    project = ''
    outDir = '../vsproj'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:p:o:", ["help", "config=", "project=", "out="])
        for opt, arg in opts:
            if opt in ("-c", "--config"):
                configFile = arg
            elif opt in ("-p", "--project"):
                project = arg
            elif opt in ("-o", "--out"):
                outDir = adjustPath(arg)
            else:
                bexit = True
    except getopt.GetoptError:
        bexit = True

    if bexit == True or len(project) <= 0:
        usage()
        sys.exit(1)

    configPath = adjustPath(getAbsPath(configFile))
    configInfo = analysisConfig(configPath)  # 读取配置文件
    if 'dir' not in configInfo:
        print("config file: %s analysis failed!" % configPath)
        sys.exit(0)

    basePath = adjustPath('/'.join(configPath.split('/')[:-1]))
    filterConfig = {}
    if 'filter' in configInfo:
        filterConfig = configInfo['filter']

    analysisInfo = {}
    for dir in configInfo['dir']:    # 解析目录
        analysisFileDirs(basePath, outDir, dir, analysisInfo, filterConfig)

    if 'files' in configInfo:  # 解析文件
        analysisFiles(basePath, outDir, configInfo['files'], analysisInfo, filterConfig)

    excludeCfg = None
    if 'exclude' in configInfo:
        excludeCfg = []
        for strkey in configInfo['exclude']:
            excludeCfg.append(strkey.replace('\\', '/'))

    saveOutFile_proj(basePath, outDir, project, analysisInfo, excludeCfg)    # 保存工程文件
    saveOutFile_filter(basePath, outDir, project, analysisInfo, excludeCfg, filterConfig)  # 保存filter文件
