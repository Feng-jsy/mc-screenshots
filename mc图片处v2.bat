@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ========== 请确认源目录是否正确 ==========
set "SOURCE_DIR=D:\MC  PCL2\.minecraft\versions"

:: 目标目录：桌面上的“输出文件夹”
set "DESKTOP=%USERPROFILE%\Desktop"
set "TARGET_DIR=%DESKTOP%\输出文件夹"

echo ========================================
echo 源目录: %SOURCE_DIR%
echo 目标目录: %TARGET_DIR%
echo ========================================
echo.
echo 请确认目标目录是您期望的位置（应为桌面上的“输出文件夹”）。
echo 如果正确，按任意键继续；否则关闭窗口修改脚本。
pause >nul

:: 检查源目录
if not exist "%SOURCE_DIR%" (
    echo 错误：源目录 "%SOURCE_DIR%" 不存在！
    pause
    exit /b 1
)

:: 创建目标文件夹（如果不存在）
if not exist "%TARGET_DIR%" (
    echo 正在创建目标文件夹 "%TARGET_DIR%"...
    mkdir "%TARGET_DIR%" 2>nul
    if errorlevel 1 (
        echo 错误：无法创建目标文件夹！请检查权限或路径。
        pause
        exit /b 1
    )
) else (
    echo 目标文件夹已存在，将直接使用。
)

echo.
echo 正在扫描图片，请稍候...
echo.

set "EXTENSIONS=.jpg .jpeg .png .bmp .gif .tiff .tif .webp"
set count=0
set found=0

for /r "%SOURCE_DIR%" %%f in (*) do (
    set "fullname=%%f"
    set "ext=%%~xf"
    for %%e in (%EXTENSIONS%) do (
        if /i "!ext!"=="%%e" (
            set found=1
            set "filename=%%~nxf"
            set "relpath=!fullname:%SOURCE_DIR%=!"
            if "!relpath:~0,1!"=="\" set "relpath=!relpath:~1!"
            for /f "delims=\" %%a in ("!relpath!") do set "version=%%a"
            if defined version (
                set "newfilename=!version!_!filename!"
            ) else (
                set "newfilename=!filename!"
            )
            :: 复制到目标文件夹（并显示完整目标路径，便于调试）
            copy /y "%%f" "%TARGET_DIR%\!newfilename!" >nul
            if errorlevel 1 (
                echo 复制失败: !newfilename!
            ) else (
                set /a count+=1
                set /a mod=!count! %% 100
                if !mod!==0 (
                    echo 已处理 !count! 个文件...
                ) else (
                    set /p "=." <nul
                )
            )
        )
    )
)

echo.
if %found%==0 (
    echo 未找到图片文件。
) else (
    echo 复制完成，共处理 %count% 个图片文件。
    echo 所有文件已保存到：%TARGET_DIR%
)

echo.
echo 按任意键退出...
pause >nul