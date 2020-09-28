if command -v nodemon &> /dev/null
then
    clear && nodemon  --exec "pytest ./tests/call_test.py" -w ./tests/*.*
else
    echo "You don't have nodemon installed"
fi
