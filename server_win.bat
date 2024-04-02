@echo off
setlocal enabledelayedexpansion

for /f "tokens=* usebackq" %%i in (`python -c "import inference; print(inference.MODEL)"`) do (
    set "MODEL_NAME=%%i"
)

docker run -it --rm -p 8500:8500 ^
   -v "%cd%/serving_model/%MODEL_NAME%:/models/%MODEL_NAME%" ^
   -e MODEL_NAME=%MODEL_NAME% tensorflow/serving:1.15.0-gpu
