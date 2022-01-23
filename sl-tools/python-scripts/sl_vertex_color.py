import maya.cmds as cmds

# create duplicate mesh(es) with R,G,B,A Color Sets

def createColorMesh():
    sel = cmds.ls(sl=1)
    newObjs = cmds.duplicate(sel)
    # print(str(newObj[0]))

    for i in range(len(newObjs)):

        cmds.select(newObjs[i])

        cmds.rename(str(sel[i]) + "_col")

        allColorSets = cmds.polyColorSet(query=True, allColorSets=True)

        if(allColorSets is not None):
            for i in range(len(allColorSets)):
                cmds.polyColorSet(delete=True)

        cmds.polyColorSet(create=True, colorSet='R',
                          representation="RGB", perInstance=False)
        cmds.polyColorSet(create=True, colorSet='G',
                          representation="RGB", perInstance=False)
        cmds.polyColorSet(create=True, colorSet='B',
                          representation="RGB", perInstance=False)
        cmds.polyColorSet(create=True, colorSet='A',
                          representation="A", perInstance=False)


def transferSingleColorsFromSelection():
    sel = cmds.ls(sl=1)
    if len(sel) < 2:
        cmds.warning("Please select multiple objects")
        return

    # build mesh and color mesh lists
    sel.sort()
    colorSuffix = "_col"
    sources = [x for x in sel if str(x).endswith(colorSuffix)]
    destinations = [x for x in sel if x not in sources]

    colDict = {}
    j = 0
    for i in range(len(sources)):
        size = len(str(sources[i]))
        sourceName = str(sources[i])[:size - len(colorSuffix)]
        prevJ = j
        while j < len(destinations):
            destName = str(destinations[j])
            # found matching color mesh
            if(destName == sourceName):
                colDict[sources[i]] = destinations[j]
                j += 1
                break
            j += 1

        # a mesh doesn't have matching color mesh
        if j == len(destinations):
            j = prevJ

    for key in colDict:
        transferColorsPerChannel(key, colDict[key])
    cmds.select(sel)


# transfer vertex colors from one mesh's R, G, B, A Color Sets
# to another mesh's RGBA Color Set
def transferColorsPerChannel(src, dest):
    cmds.transferAttributes(str(src), str(
        dest), transferColors=2, sampleSpace=0)
    cmds.select(dest)

    # add or overwrite merged Color Set
    cmds.polyColorSet(delete=True, allColorSets=True)
    cmds.polyColorSet(create=True, colorSet='RGBA', perInstance=False)
    allColorSets = cmds.polyColorSet(query=True, allColorSets=True)

    hasR = "R" in allColorSets
    hasG = "G" in allColorSets
    hasB = "B" in allColorSets
    hasA = "A" in allColorSets

    vertices = cmds.ls(str(dest) + '.vtx[*]', fl=True)
    setVertexColors(vertices, hasR, hasG, hasB, hasA)
    cmds.select(dest)
    cmds.polyColorSet(delete=True, colorSet='R')
    cmds.polyColorSet(delete=True, colorSet='G')
    cmds.polyColorSet(delete=True, colorSet='B')
    cmds.polyColorSet(delete=True, colorSet='A')


def setVertexColors(vertices, setR, setG, setB, setA):
    if(setR and setG and setB and setA):
        for vertex in vertices:
            cmds.select(vertex)
            if setR:
                cmds.polyColorSet(currentColorSet=True, colorSet='R')
                r = cmds.polyColorPerVertex(query=True, r=True)[0]

            if setG:
                cmds.polyColorSet(currentColorSet=True, colorSet='G')
                g = cmds.polyColorPerVertex(query=True, g=True)[0]

            if setB:
                cmds.polyColorSet(currentColorSet=True, colorSet='B')
                b = cmds.polyColorPerVertex(query=True, b=True)[0]

            if setA:
                cmds.polyColorSet(currentColorSet=True, colorSet='A')
                a = cmds.polyColorPerVertex(query=True, a=True)[0]

            cmds.polyColorSet(currentColorSet=True, colorSet='RGBA')

            if(r is not 0):
                cmds.polyColorPerVertex(r=r)
            if(g is not 0):
                cmds.polyColorPerVertex(g=g)
            if(b is not 0):
                cmds.polyColorPerVertex(b=b)
            if(a is not 0):
                cmds.polyColorPerVertex(a=a)


def deleteColorSet(name):
    allColorSets = cmds.polyColorSet(query=True, allColorSets=True)

    if(allColorSets is not None):
        for colorSet in allColorSets:
            if(str(colorSet) == name):
                cmds.polyColorSet(delete=True, colorSet=name)
