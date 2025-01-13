function Update-WidgetId {
    param (
        [string]$FieldId,
        [string]$NewWidgetId
    )
    
    $entries = $jsonContent.editorInterfaces.controls | Where-Object { $_.fieldId -eq $FieldId }

    Write-Output "Old widget IDs for $FieldId:"
    foreach ($entry in $entries) {
        Write-Output $entry.widgetId
    }

    foreach ($entry in $entries) {
        $entry.widgetId = $NewWidgetId
    }

    Write-Output "New widget IDs for $FieldId:"
    foreach ($entry in $entries) {
        Write-Output $entry.widgetId
    }
}

# Replace widgetId for imgix-cropper
$ImgixCropperIdDev = $Env:bamboo_ImgixCropperIdDev
Write-Output "imgix-cropper: replacing prod widget id with ($ImgixCropperIdDev)"
Update-WidgetId -FieldId "imgixQueryString" -NewWidgetId $ImgixCropperIdDev

# Replace widgetId for control-options
$ControlOptionsIdDev = $Env:bamboo_ControlOptionsIdDev
Write-Output "control-options: replacing prod widget id with ($ControlOptionsIdDev)"
Update-WidgetId -FieldId "controlOptions" -NewWidgetId $ControlOptionsIdDev
