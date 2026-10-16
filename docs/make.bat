@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
if "%SPHINXINTL%" == "" (
	set SPHINXINTL=sphinx-intl
)
set SOURCEDIR=.
set BUILDDIR=_build
set LANG_ARGS=-l fa

if "%1" == "" goto help

REM --- i18n targets that are not Sphinx builders (sphinx-intl driven) -------
if "%1" == "gettext" (
	%SPHINXBUILD% -M gettext %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
	goto end
)
if "%1" == "update-intl" (
	%SPHINXBUILD% -M gettext %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
	%SPHINXINTL% update -p %BUILDDIR%/gettext %LANG_ARGS%
	goto end
)
if "%1" == "mo" (
	%SPHINXINTL% -c conf.py build %LANG_ARGS%
	goto end
)
if "%1" == "html-en" (
	%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%/html/en %SPHINXOPTS% %O%
	goto end
)
if "%1" == "html-fa" (
	%SPHINXINTL% -c conf.py build %LANG_ARGS%
	%SPHINXBUILD% -b html -D language=fa %SOURCEDIR% %BUILDDIR%/html/fa %SPHINXOPTS% %O%
	goto end
)
if "%1" == "bilingual" (
	%SPHINXBUILD% -b html %SOURCEDIR% %BUILDDIR%/html/en %SPHINXOPTS% %O%
	%SPHINXINTL% -c conf.py build %LANG_ARGS%
	%SPHINXBUILD% -b html -D language=fa %SOURCEDIR% %BUILDDIR%/html/fa %SPHINXOPTS% %O%
	echo Built %BUILDDIR%\html\en and %BUILDDIR%\html\fa
	goto end
)

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.http://sphinx-doc.org/
	exit /b 1
)

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
