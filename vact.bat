@echo off
: if no arguments
if not [%1] == [] goto one_param

@echo on
"%~dp0venv\Scripts\activate"
goto ext

:one_param
@echo on
"%~dp0%1\Scripts\activate"

:ext