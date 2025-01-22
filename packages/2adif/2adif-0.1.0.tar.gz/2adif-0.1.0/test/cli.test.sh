#!/bin/bash

echo "python: " $(python --version)
echo "pipx  : " $(pipx --version)
pipx run --python python"$python_version" --spec . 2adif ./test/ 
