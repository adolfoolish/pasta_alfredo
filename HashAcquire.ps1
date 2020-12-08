<#
.synopsis
Obtiene el hash junto con el nombre de los archivos

- El usuario especifica el equipo objetivo
- El usuario especifica el directorio objetivo

Este script creara un archivo que contiene
SHA-256Hash y FilePath

.Description
Este script obtiene el hash junto con el nombre de los archivos

.parameter TargetFolder
La carpeta de donde se extraeran los hash

.parameter ResultFile
El archivo donde se creara el documento

.example

HashAcquire 
Obtiene el hash junto con el nombre de los archivos
#>


# Parameter Definition Section
param(  
    [string]$TargetFolder="C:/Windows/System32/drivers/",
    [string]$ResultFile="baseline.txt"
)


Get-ChildItem $TargetFolder | Get-FileHash | Select-Object -Property Hash, Path | Format-Table -HideTableHeaders | Out-File $ResultFile -Encoding ascii

