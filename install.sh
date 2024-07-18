python -m build > build.log
pip install dist/$(tail -n 1 build.log |cut -d ' ' -f $(tail -n 1 build.log |wc -w)) --force-reinstall
# cd test
# pytest . -v 
echo "install complete"
echo "Run 'tkm' to start the app"
