$btAdapter = Get-NetAdapter | Where-Object {$_.InterfaceDescription -like "*Bluetooth*"}
foreach ($adapter in $btAdapter) {
    if ($adapter.Status -eq "Up") {
        Disable-NetAdapter -Name $adapter.Name -Confirm:$false
    } else {
        Enable-NetAdapter -Name $adapter.Name -Confirm:$false
    }
}
Write-Output "Bluetooth toggled"