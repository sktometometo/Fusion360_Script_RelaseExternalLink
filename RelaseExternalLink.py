#Author-
#Description-ファイル内の外部への参照リンクをすべて解除する

import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface

        # Get root rootComponent
        product = app.activeProduct
        design = adsk.fusion.Design.cast(product)
        rootComp = design.rootComponent

        # progress dialog
        progressDialog = ui.createProgressDialog()
        progressDialog.cancelButtonText = "Cancel"
        progressDialog.isBackgroundTranslucent = False
        progressDialog.isCancelButtonShown = True
        progressDialog.isValid = True

        
        occurrences = rootComp.occurrences
        progressDialog.show("counting objects...", \
                            "Counting target objects : %p %", 0, occurrences.count, 1)
        numtotaloccs = 0
        for occ in occurrences:
            progressDialog.message = "Counting objects in " + occ.name + " : %p \%"
            numtotaloccs += countTargetLink( occ )
            progressDialog.progressValue += 1
            if progressDialog.wasCancelled:
                # TODO
                break
        progressDialog.hide()
        progressDialog.reset()

        #
        ret = True
        progressDialog.show("breaking external link", \
                            "breaking external link : %p %", 0, numtotaloccs, 1)
        for occ in occurrences:
            ret = breakExternalLink( occ, progressDialog )
            if ret == "DialogCancel":
                progressDialog.reset()
                progressDialog.hide()
            elif ret == False:
                ui.messageBox("failed to break some external link.")
        progressDialog.hide()
        progressDialog.reset()

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))

def countTargetLink( occurrence ):
    """
    """
    ret = 1
    childOccs = occurrence.childOccurrences
    for childOcc in childOccs:
        ret += countTargetLink( childOcc )
    return ret

def breakExternalLink( occurrence, progressDialog ):
    """
    """
    ret = True

    progressDialog.message = "breaking external link of " + occurrence.name + "...." + "\n" + "progress : %p"
    progressDialog.progressValue += 1

    if occurrence.isReferencedComponent:
        ret = occurrence.breakLink()

    progressDialog.message = "breaking external link of " + occurrence.name + " has been broken." + "\n" + "progress : %p"

    if progressDialog.wasCancelled:
        return "DialogCancel"

    childOccs = occurrence.childOccurrences
    for childOcc in childOccs:
        tempret = breakExternalLink( childOcc, progressDialog )
        if tempret == "DialogCancel":
            return "DialogCancel"
        elif tempret:
            ret = True
        else:
            ret = False

    return ret
