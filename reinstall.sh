pip uninstall tinkermodellor -y
export TKMROOT=$(pwd)
python -m build > build.log
pip install dist/$(tail -n 1 build.log |cut -d ' ' -f $(tail -n 1 build.log |wc -w))
cd test
pytest . --no-summary
echo "Reinstall complete"
echo "Run 'tkm' to start the app"
