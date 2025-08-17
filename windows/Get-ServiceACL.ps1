[CmdletBinding(DefaultParameterSetName="ByName")]
param(
        [Parameter(ParameterSetName="ByName")]
        [string[]] $Name,
        [Parameter(ParameterSetName="ByDisplayName")]
        [string[]] $DisplayName,
        [switch] $Help,
        [string] $ComputerName = $env:COMPUTERNAME
)

function Show-Usage {
    $scriptName = if ($PSCommandPath) {
        Split-Path -Leaf $PSCommandPath
    } elseif ($MyInvocation.MyCommand.Path) {
        Split-Path -Leaf $MyInvocation.MyCommand.Path
    } elseif ($MyInvocation.MyCommand.Name) {
        $MyInvocation.MyCommand.Name
    } else {
        'test.ps1'
    }
        @"
Usage: powershell.exe -ExecutionPolicy Bypass -File .\$scriptName -Name <ServiceName>[,<ServiceName>...] [-ComputerName <Host>]
     or: powershell.exe -ExecutionPolicy Bypass -File .\$scriptName -DisplayName <ServiceDisplayName>[,<ServiceDisplayName>...] [-ComputerName <Host>]

Options:
    -Name           One or more service internal names (mutually exclusive with -DisplayName)
    -DisplayName    One or more service display names (mutually exclusive with -Name)
    -ComputerName   Target computer (default: local machine)
    -Help           Show this usage information

Examples:
    .\\$scriptName -Name Spooler
    .\\$scriptName -DisplayName "Print Spooler" -ComputerName SERVER01

Output:
    A table of all ACEs showing ServiceName, IdentityReference, AccessControlType, and ServiceRights.
"@ | Write-Host
}

if ($Help) { Show-Usage; return }

if (-not $PSBoundParameters.ContainsKey('Name') -and -not $PSBoundParameters.ContainsKey('DisplayName')) {
        Show-Usage; return
}

if ($PSBoundParameters.ContainsKey('Name') -and $PSBoundParameters.ContainsKey('DisplayName')) {
        Write-Error "Specify either -Name or -DisplayName, not both."; Show-Usage; return
}

# Define ServiceAccessFlags enum
Add-Type @"
[System.FlagsAttribute]
public enum ServiceAccessFlags : uint
{
    QueryConfig = 1,
    ChangeConfig = 2,
    QueryStatus = 4,
    EnumerateDependents = 8,
    Start = 16,
    Stop = 32,
    PauseContinue = 64,
    Interrogate = 128,
    UserDefinedControl = 256,
    Delete = 65536,
    ReadControl = 131072,
    WriteDac = 262144,
    WriteOwner = 524288,
    Synchronize = 1048576,
    AccessSystemSecurity = 16777216,
    GenericAll = 268435456,
    GenericExecute = 536870912,
    GenericWrite = 1073741824,
    GenericRead = 2147483648
}
"@

# Define the function
function Get-ServiceAcl {
    [CmdletBinding(DefaultParameterSetName="ByName")]
    param(
        [Parameter(Mandatory=$true, Position=0, ValueFromPipeline=$true, ParameterSetName="ByName")]
        [string[]] $Name,
        [Parameter(Mandatory=$true, Position=0, ParameterSetName="ByDisplayName")]
        [string[]] $DisplayName,
        [Parameter(Mandatory=$false, Position=1)]
        [string] $ComputerName = $env:COMPUTERNAME
    )

    # Resolve display names
    switch ($PSCmdlet.ParameterSetName) {
        "ByDisplayName" {
            $Name = Get-Service -DisplayName $DisplayName -ComputerName $ComputerName -ErrorAction Stop | 
                Select-Object -ExpandProperty Name
        }
    }

    # Ensure sc.exe exists
    $ServiceControlCmd = Get-Command "$env:SystemRoot\system32\sc.exe"
    if (-not $ServiceControlCmd) { throw "Could not find $env:SystemRoot\system32\sc.exe command!" }

    # Get service ACLs
    Get-Service -Name $Name | ForEach-Object {
        $CurrentName = $_.Name
        $Sddl = & $ServiceControlCmd.Definition "\\$ComputerName" sdshow "$CurrentName" | Where-Object { $_ }

        try { $Dacl = New-Object System.Security.AccessControl.RawSecurityDescriptor($Sddl) }
        catch {
            Write-Warning "Couldn't get security descriptor for service '$CurrentName': $Sddl"
            return
        }

        $CustomObject = New-Object -TypeName PSObject -Property ([ordered] @{ Name = $_.Name; Dacl = $Dacl })

        # Access property
        $CustomObject | Add-Member -MemberType ScriptProperty -Name Access -Value {
            $this.Dacl.DiscretionaryAcl | ForEach-Object {
                $CurrentDacl = $_
                try { $IdentityReference = $CurrentDacl.SecurityIdentifier.Translate([System.Security.Principal.NTAccount]) }
                catch { $IdentityReference = $CurrentDacl.SecurityIdentifier.Value }

                New-Object -TypeName PSObject -Property ([ordered] @{
                    ServiceName = $this.Name
                    ServiceRights = [ServiceAccessFlags] $CurrentDacl.AccessMask
                    AccessControlType = $CurrentDacl.AceType
                    IdentityReference = $IdentityReference
                    IsInherited = $CurrentDacl.IsInherited
                    InheritanceFlags = $CurrentDacl.InheritanceFlags
                    PropagationFlags = $CurrentDacl.PropagationFlags
                })
            }
        }

        # AccessToString property
        $CustomObject | Add-Member -MemberType ScriptProperty -Name AccessToString -Value {
            $this.Access | ForEach-Object {
                "{0} {1} {2}" -f $_.IdentityReference, $_.AccessControlType, $_.ServiceRights
            } | Out-String
        }

        $CustomObject
    }
}

# Only call function if parameters were passed
if ($PSBoundParameters.ContainsKey('Name')) {
    $svc = Get-ServiceAcl -Name $Name -ComputerName $ComputerName
} elseif ($PSBoundParameters.ContainsKey('DisplayName')) {
    $svc = Get-ServiceAcl -DisplayName $DisplayName -ComputerName $ComputerName
}

if ($null -ne $svc) {
    # Output a detailed, readable table of all ACEs
    $svc | ForEach-Object { $_.Access } |
        Select-Object ServiceName, IdentityReference, AccessControlType, ServiceRights |
        Format-Table -AutoSize -Wrap
}

