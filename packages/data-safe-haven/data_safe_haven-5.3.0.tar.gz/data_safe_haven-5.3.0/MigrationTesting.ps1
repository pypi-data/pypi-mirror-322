# Need to update Az.Compute and install Az.Maintenance

# Follow steps here at the link below to automatically generate data collection rules
# https://github.com/microsoft/AzureMonitorCommunity/tree/master/Azure%20Services/Azure%20Monitor/Agents/Migration%20Tools/DCR%20Config%20Generator
New-AzResourceGroupDeployment -ResourceGroupName RG_SHM_BLUE_MONITORING -TemplateFile ./linux_dcr_arm_template.json

# Alternatively, you can manually create a data collection rule
New-AzDataCollectionRule -RuleName shm-blue-dcr -Location uksouth -ResourceGroupName RG_SHM_BLUE_MONITORING

# There are different Azure Monitor Agents for Windows and Linux.
Set-AzVMExtension -Name AzureMonitorLinuxAgent -ExtensionType AzureMonitorLinuxAgent -Publisher Microsoft.Azure.Monitor -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS -VMName GITLAB-SRE-T2GUAC -Location uksouth -TypeHandlerVersion 1.30.3 -EnableAutomaticUpgrade $true

$dcr = Get-AzDataCollectionRule -ResourceGroupName RG_SHM_BLUE_MONITORING -Name shm-blue-migrate-linux
$vmId = (Get-AzVM -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS -Name GITLAB-SRE-T2GUAC).id

New-AzDataCollectionRuleAssociation -TargetResourceId $vmId -DataCollectionRuleId $dcr.id

# Need to add an appropriate NSG rule for AzureResourceManager to allow the VM to communicate with the Log Analytics workspace?
# No, already covered by private links. Need to add it to private link dns zone instead

# Need to have a data collection endpoint

New-AzDataCollectionEndpoint -ResourceGroupName RG_SHM_BLUE_MONITORING -DataCollectionRuleId $dcr.id -Name shm-blue-migrate-linux

# Need to add some additional private link stuff.
$PrivateLinkDomains = @(
    "agentsvc.azure-automation.net",
    "azure-automation.net", # note this must come after 'agentsvc.azure-automation.net'
    "blob.core.windows.net",
    "monitor.azure.com",
    "ods.opinsights.azure.com",
    "oms.opinsights.azure.com"
)
foreach ($DnsConfig in $DnsConfigs) {
    $BaseDomain = $PrivateLinkDomains | Where-Object { $DnsConfig.Fqdn.Endswith($_) } | Select-Object -First 1 # we want the first (most specific) match
$privateZone = Deploy-PrivateDnsZone -Name "privatelink.${BaseDomain}" -ResourceGroup $config.network.vnet.rg
$recordName = $DnsConfig.Fqdn.Substring(0, $DnsConfig.Fqdn.IndexOf($BaseDomain) - 1)
$null = Deploy-PrivateDnsRecordSet -Name $recordName -ZoneName $privateZone.Name -ResourceGroupName $privateZone.ResourceGroupName -PrivateIpAddresses $DnsConfig.IpAddresses -Ttl 10

# Modify the ASC default policy to stop auto installing linux monitoring agent/OMS

$params = @{
    dcrName,
    dcrLocation,
    logAnalyticsWorkspaceArmId
}

Deploy-ArmTemplate -TemplatePath (Join-Path $PSScriptRoot ".." "arm_templates" "shm-monitoring-template.json") -TemplateParameters $params -ResourceGroupName $config.dc.rg



$paramtest = @{
    dcrName = "shm-blue-test"
    dcrLocation = "uksouth"
    logAnalyticsWorkspaceArmId = "/subscriptions/3f1a8e26-eae2-4539-952a-0a6184ec248a/resourcegroups/RG_SHM_BLUE_MONITORING/providers/microsoft.operationalinsights/workspaces/shm-blue-loganalytics"
}

# How does automation work?
# User hybrid worker groups are also being retired - but we use system hybrid worker groups and they are *not* being retired.
# possibly need to cut out automation use and switch to new update management
# new AMA not compatible with automation using system hybrid worker groups

$paramsmaint = @{
    maintenanceConfigName = "testingmaint"
    maintenanceConfigLocation  = "uksouth"
    maintenanceScope = "InGuestPatch"
}

$maintenanceCfg = @{

}

# Create Maintenance Configuration

New-AzMaintenanceConfiguration -ResourceGroupName RG_SHM_BLUE_MONITORING -Name testingmaint -Location uksouth -MaintenanceScope InGuestPatch -StartDateTime "2024-04-09 01:00" -Duration 03:55 -TimeZone "GMT Standard Time" -RecurEvery 1Day -ExtensionProperty @{inGuestPatchMode = "User" } -LinuxParameterClassificationToInclude @('Critical', 'Security') -WindowParameterClassificationToInclude @('Critical', 'Security') -InstallPatchRebootSetting "IfRequired"

$maintcfg = Get-AzMaintenanceConfiguration -ResourceGroupName RG_SHM_BLUE_MONITORING -Name testingmaint

# Assign Maintenance Configuration to a VM
New-AzConfigurationAssignment -ResourceGroupName "RG_SHM_BLUE_SRE_T2GUAC_DATABASES" -Location "uksouth" -ResourceType "VirtualMachines" -ProviderName "Microsoft.Compute" -MaintenanceConfigurationId $maintcfg.Id -ResourceName "PSTGRS-T2GUAC" -ConfigurationAssignmentName "testingmaint"
New-AzResourceGroupDeployment -ResourceGroupName RG_SHM_BLUE_MONITORING -TemplateFile ./newupdatemanager.json -TemplateParameterObject $paramsmaint



# Testing on an SRD that requires security updates.
#
# Step 1 - install the Azure Monitor Linux Agent
Set-AzVMExtension -Name AzureMonitorLinuxAgent -ExtensionType AzureMonitorLinuxAgent -Publisher Microsoft.Azure.Monitor -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_COMPUTE -VMName "SRE-T2GUAC-161-SRD-20-04-2024032000" -Location uksouth -TypeHandlerVersion 1.30 -EnableAutomaticUpgrade $true
# Step 2 - Associate this with a data collection rule
$vmId = (Get-AzVM -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_COMPUTE -Name "SRE-T2GUAC-161-SRD-20-04-2024032000").id
$dcr = Get-AzDataCollectionRule -ResourceGroupName RG_SHM_BLUE_MONITORING -Name shm-blue-migrate-linux
$dcrEndpoint = Get-AzDataCollectionEndpoint -ResourceGroupName RG_SHM_BLUE_MONITORING -Name t2guacwbapps
# This bit is WEIRD. Cannot specify both endpoint and rule. AssociationName doesn't need to be anything in particular when specifying rule
New-AzDataCollectionRuleAssociation -TargetResourceId $vmId -DataCollectionRuleId $dcr.id -AssociationName "testingrule"
# if specifying endpoint, Assoc name must be configurationAccessEndpoint
New-AzDataCollectionRuleAssociation -TargetResourceId $vmId -AssociationName "configurationAccessEndpoint" -DataCollectionEndpointId $dcrEndpoint.id

$maintcfg = Get-AzMaintenanceConfiguration -ResourceGroupName RG_SHM_BLUE_MONITORING -Name testingmaint
# need to change the VM: "Please set the patchMode to AutomaticByPlatform and bypassPlatformChecksOnUserSchedule as true"

$VirtualMachine = Get-AzVM -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_COMPUTE -Name "SRE-T2GUAC-161-SRD-20-04-2024032000"
Set-AzVMOperatingSystem -VM $VirtualMachine -Linux -PatchMode "AutomaticByPlatform"
$AutomaticByPlatformSettings = $VirtualMachine.OSProfile.LinuxConfiguration.PatchSettings.AutomaticByPlatformSettings

if ($null -eq $AutomaticByPlatformSettings) {
    $VirtualMachine.OSProfile.LinuxConfiguration.PatchSettings.AutomaticByPlatformSettings = New-Object -TypeName Microsoft.Azure.Management.Compute.Models.LinuxVMGuestPatchAutomaticByPlatformSettings -Property @{BypassPlatformSafetyChecksOnUserSchedule = $true }
} else {
    $AutomaticByPlatformSettings.BypassPlatformSafetyChecksOnUserSchedule = $true
}

Update-AzVM -VM $VirtualMachine -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_COMPUTE

New-AzConfigurationAssignment -ResourceGroupName "RG_SHM_BLUE_SRE_T2GUAC_COMPUTE" -Location "uksouth" -ResourceType "VirtualMachines" -ProviderName "Microsoft.Compute" -MaintenanceConfigurationId $maintcfg.Id -ResourceName "SRE-T2GUAC-161-SRD-20-04-2024032000" -ConfigurationAssignmentName "testingmaint"

# Note that one update failed - this may have been because the update required manual acceptance of a license agreement


# Trying this now on a machine that doesn't have periodic assessment switched on

$VirtualMachine = Get-AzVM -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS -Name "CODIMD-SRE-T2GUAC"
Set-AzVMOperatingSystem -VM $VirtualMachine -Linux -PatchMode "AutomaticByPlatform"
$AutomaticByPlatformSettings = $VirtualMachine.OSProfile.LinuxConfiguration.PatchSettings.AutomaticByPlatformSettings

if ($null -eq $AutomaticByPlatformSettings) {
    $VirtualMachine.OSProfile.LinuxConfiguration.PatchSettings.AutomaticByPlatformSettings = New-Object -TypeName Microsoft.Azure.Management.Compute.Models.LinuxVMGuestPatchAutomaticByPlatformSettings -Property @{BypassPlatformSafetyChecksOnUserSchedule = $true }
} else {
    $AutomaticByPlatformSettings.BypassPlatformSafetyChecksOnUserSchedule = $true
}

Update-AzVM -VM $VirtualMachine -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS


# this machine does not have periodic assessment turned on
# periodic assessment can be enforced using policy or using the REST API


# $patchParams = @{ResourceGroupName = "RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS"; VMName = "CODIMD-SRE-T2GUAC"; PatchMode = "AutomaticByPlatform"; BypassPlatformSafetyChecksOnUserSchedule = $true}
# Invoke-AzRestMethod

# possibly try Set-AzVMOperatingSystem -VM $VirtualMachine -Linux -AssessmentMode "AutomaticByPlatform"

# I have not turned on periodic assessment for gitlab-sre-t2guac and have not run it manually - let's see if it updates.
$VirtualMachine = Get-AzVM -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS -Name "GITLAB-SRE-T2GUAC"
Set-AzVMOperatingSystem -VM $VirtualMachine -Linux -PatchMode "AutomaticByPlatform"
$AutomaticByPlatformSettings = $VirtualMachine.OSProfile.LinuxConfiguration.PatchSettings.AutomaticByPlatformSettings

if ($null -eq $AutomaticByPlatformSettings) {
    $VirtualMachine.OSProfile.LinuxConfiguration.PatchSettings.AutomaticByPlatformSettings = New-Object -TypeName Microsoft.Azure.Management.Compute.Models.LinuxVMGuestPatchAutomaticByPlatformSettings -Property @{BypassPlatformSafetyChecksOnUserSchedule = $true }
} else {
    $AutomaticByPlatformSettings.BypassPlatformSafetyChecksOnUserSchedule = $true
}

Update-AzVM -VM $VirtualMachine -ResourceGroupName RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS

New-AzConfigurationAssignment -ResourceGroupName "RG_SHM_BLUE_SRE_T2GUAC_WEBAPPS" -Location "uksouth" -ResourceType "VirtualMachines" -ProviderName "Microsoft.Compute" -MaintenanceConfigurationId $maintcfg.Id -ResourceName "GITLAB-SRE-T2GUAC" -ConfigurationAssignmentName "testingmaint"

# Confirmed that periodic assessment is NOT necessary