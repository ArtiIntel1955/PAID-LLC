$Email = "MyAIEmployee@outlook.com"
$Pass = "fecjxishcgbsokqe"
$SecurePass = ConvertTo-SecureString $Pass -AsPlainText -Force
$Cred = New-Object System.Management.Automation.PSCredential($Email, $SecurePass)

try {
    Send-MailMessage -From $Email -To $Email -Subject "OpenClaw Test" -Body "Connection Successful" `
                     -SmtpServer "smtp-mail.outlook.com" -Port 587 -UseSsl -Credential $Cred
    Write-Host "✅ SUCCESS: Your email settings are perfect!" -ForegroundColor Green
} catch {
    Write-Host "❌ FAILED: Microsoft blocked the connection." -ForegroundColor Red
    Write-Host $_.Exception.Message
}