# Bake Pivot to Vertex Color

import maya.cmds as cmds

scriptName = 'BakeVertexColor'

bakeSettings = {
    'pivotPos': 'custom',
    'translateX': 0,
    'translateY': 0,
    'translateZ': 0
}


def createUI(pWindowTitle):
    windowID = 'bakeVertexColor'
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    cmds.window(windowID, title=pWindowTitle,
                sizeable=True, resizeToFitChildren=False)

    mainColumnLayout = cmds.columnLayout(p=windowID, width=256)

    # Title
    # titleLayout = cmds.rowColumnLayout(nc= 3, cw=[(1,)])

    # Pivot Position
    pivotSourceLayout = cmds.rowColumnLayout(nc=2,
                                             cw=[(1, 100), (2, 100)], cal=[(1, "right"), (2, "left")], cs=[(2, 20)], p=mainColumnLayout)

    def updatePivotPositionOptions(item):
        useCustomPivotPos = item == 'Custom'
        cmds.text(ruleOptionText, e=True, en=not useCustomPivotPos)
        cmds.optionMenu(ruleOption, e=True, en=not useCustomPivotPos)
        cmds.floatField(pivotX, e=True, en=useCustomPivotPos)
        cmds.floatField(pivotY, e=True, en=useCustomPivotPos)
        cmds.floatField(pivotZ, e=True, en=useCustomPivotPos)

    cmds.text('Pivot: ', al='right', p=pivotSourceLayout)
    pivotPos = cmds.optionMenu(
        changeCommand=updatePivotPositionOptions, p=pivotSourceLayout)
    cmds.menuItem(label='Custom')
    cmds.menuItem(label='Smallest X')
    cmds.menuItem(label='Largest X')
    cmds.menuItem(label='Smallest Y')
    cmds.menuItem(label='Largest Y')
    cmds.menuItem(label='Smallest Z')
    cmds.menuItem(label='Largest Z')

    ruleOptionText = cmds.text(
        label="Group: ", al='right', en=False, p=pivotSourceLayout)
    ruleOption = cmds.optionMenu(
        en=False, p=pivotSourceLayout)
    # Separate individual islands and bake pivot for each
    cmds.menuItem(label='Separate Island')
    # Find the pivot for all vertices on the object
    cmds.menuItem(label='Selected Vertices')

    pivotPosLayout = cmds.rowColumnLayout(
        nc=3, cs=[(1, 100)], cw=[(1, 50), (2, 50), (3, 50)], p=mainColumnLayout)
    pivotX = cmds.floatField(value=0, ann="tx", en=True)
    pivotY = cmds.floatField(value=0, ann="ty", en=True)
    pivotZ = cmds.floatField(value=0, ann="tz", en=True)

    # Copy/Paste Transforms
    transformUtilLayout = cmds.rowColumnLayout(nc=1, p=mainColumnLayout)
    cmds.text('Copy and Paste Pivot Transform', p=transformUtilLayout)

    execLayout = cmds.columnLayout(p=mainColumnLayout)
    cmds.rowColumnLayout(numberOfColumns=2,
                         columnWidth=[(1, 75), (2, 75)],
                         p=execLayout)
    cmds.button(label='Apply', command=lambda x: paintSelectedVerts(
        getFloatValue(pivotX), getFloatValue(pivotY), getFloatValue(pivotZ)))

    cmds.setParent('..')
    cmds.showWindow()
    print cmds.floatField(pivotX, query=True, value=True)

# Debug


def printSelectedVerts():
    # print selected vertices
    selectedVerts = cmds.ls(sl=True)
    for vertex in selectedVerts:
        vertPos = cmds.xform(vertex, query=True,
                             worldSpace=True, translation=True)
        print '%s' % vertPos


def getFloatValue(floatField):
    print cmds.floatField(floatField, query=True, value=True)
    return cmds.floatField(floatField, query=True, value=True)


def paintSeparateIsland():
    cmds.ls()


def paintSelectedVerts(r, g, b):
    print 'painted'
    cmds.polyColorPerVertex(rgb=(r, g, b))


createUI('Bake Vertex Color')
