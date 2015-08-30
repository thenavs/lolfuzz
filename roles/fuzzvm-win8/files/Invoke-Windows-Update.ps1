# author: Jason Huggins (git @sonjz)
# date created: 20150223
# Windows Update using PSWindowsUpdate but with a scheduled job.
# In your ansible task, add the following:
#    # NOTE: win_updates not working as expected, created scheduled job fix
#    - name: "Perform Windows Updates"
#      script: assets/Invoke-WindowsUpdate.ps1
#
#    # NOTE: can we please get wait_for path in Windows !
#    #       retry for 60 min, every 15 sec, 3600/15 = 240 retries
#    - name: "Waiting for Windows Update to complete"
#      win_stat: path=C:\PSWindowsUpdate.DONE
#      register: shell_output
#      until: shell_output.stat.exists == true
#      retries: 240
#      delay: 15
#    - raw: powershell -ExecutionPolicy ByPass -Command Get-Content C:\PSWindowsUpdate.DONE
#
# Uses PSWindowsUpdate:
# - https://gallery.technet.microsoft.com/scriptcenter/2d191bcd-3308-4edd-9de2-88dff796b0bc
#
# Solution drawn from:
# - https://gallery.technet.microsoft.com/scriptcenter/Force-Install-Updates-on-ef821f9a
#
# Why not win_Update:
# There is an issue with using Microsoft.Update.Session::CreateUpdateDownloader remotely
# additionally, PSWindowsUpdate::Invoke-WUInstall appeared to have a similar issue remotely
function Invoke-WindowsUpdate {

  $invokeScript = {
    $baseFile = "C:\PSWindowsUpdate";

    if (Test-Path("$baseFile.DONE")) {
      Move-Item "$baseFile.DONE" "$baseFile.$((Get-Date -Format O) -replace ':','').BAK" ;
    }
    Import-Module PSWindowsUpdate ;
    Get-WUInstall -AcceptAll -IgnoreReboot | Out-File "$baseFile.PROCESSING" ;

    # NOTE: personally removing KB2966828", otherwise server can't webpi .NET 3.5 if desired later
    wusa.exe /uninstall /kb:2966828 /quiet /log /norestart >> "$baseFile.PROCESSING" ;
    Move-Item "$baseFile.PROCESSING" "$baseFile.DONE" ;
  } ;

  # remove the job (if exists), create a new one.
  # NOTE: this will clobber any previous job
  $jobName = "Invoke-WindowsUpdate" ;
  $result = Get-ScheduledJob | Where { $_.Name -eq "$jobName" } ;
  if ($result) {
    Unregister-ScheduledJob -Name "$jobName" ;
  }
  Register-ScheduledJob -Name "$jobName" -RunNow -ScriptBlock $invokeScript ;
}

Invoke-WindowsUpdate ;
