param (
    [string]$InputFolder,
    [string]$OutputCsv
)

# Load native CRC32 function from ntdll.dll
Add-Type -MemberDefinition @'
    [DllImport("ntdll.dll")]
    public static extern uint RtlComputeCrc32(uint dwInitial, byte[] pData, int iLen);
'@ -Name "CRC32" -Namespace "Utils" -PassThru

function Get-CRC32 {
    param (
        [string]$FilePath
    )
    $Bytes = [System.IO.File]::ReadAllBytes($FilePath)
    $Hash = [Utils.CRC32]::RtlComputeCrc32(0, $Bytes, $Bytes.Length)
    return ('0x' + $Hash.ToString("X8"))
}

# Initialize result list
$results = @()

# Add directory entries
$dirs = Get-ChildItem -Path $InputFolder -Recurse -Directory
foreach ($dir in $dirs) {
    $relativePath = "." + $dir.FullName.Substring($InputFolder.Length)
    $results += [PSCustomObject]@{
        Path = $relativePath
        CRC32 = '[DIR]'
        Size = '~'
    }
}

# Add file entries
$files = Get-ChildItem -Path $InputFolder -Recurse -File
foreach ($file in $files) {
    $relativePath = "." + $file.FullName.Substring($InputFolder.Length)
    $crc = Get-CRC32 -FilePath $file.FullName
    $size = $file.Length
    $results += [PSCustomObject]@{
        Path = $relativePath
        CRC32 = $crc
        Size = $size
    }
}

# Output to CSV
$results | Sort-Object Path | Export-Csv -Path $OutputCsv -NoTypeInformation -Encoding UTF8
