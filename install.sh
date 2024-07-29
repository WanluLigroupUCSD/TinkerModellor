
pip uninstall tinkermodellor -y
export TKMROOT=$(pwd)
python -m build > build.log
if [ $? -ne 0 ]; then
    echo "Build failed"
    exit 1
fi
pip install dist/$(tail -n 1 build.log |cut -d ' ' -f $(tail -n 1 build.log |wc -w)) --force-reinstall
if [ $? -ne 0 ]; then
    echo "Installation failed"
    exit 1
fi

echo "install complete"
echo "Run 'tkm' to start the app"
