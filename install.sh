conda env create -n tkm -f env.yml
conda activate tkm
pip uninstall tinkermodellor -y
export TKMROOT=$(pwd)
python -m build > build.log
if [ $? -ne 0 ]; then
    echo "Build failed"
    exit 1
fi
pip install dist/$(tail -n 1 build.log |cut -d ' ' -f $(tail -n 1 build.log |wc -w))
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi
cd test
pytest . -n auto
if [ $? -ne 0 ]; then
    echo "Tests failed"
    exit 1
fi

echo "install complete"
echo "Run 'tkm' to start the app"
