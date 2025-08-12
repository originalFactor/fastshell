Remove-Item dist/*
python -m poetry build
python -m twine upload dist/*