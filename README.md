# ShortenURL Model
The model layer class for shorten url service 
# Usage
Complete the `init.py` to meet your demand, and use the `ShoternURL` class as below
```python
import ShortURL
func = ShortURL.ShortURL()

# For first time use, initialize the database
func.init()

# add link, return shorted link
result = func.add("https://baidu.com")
print(result)

# check total length
print(func.len())

# check from original link / short link, automatically detect input type
result = func.get("https://baidu.com")
print(result)

# don't forget to close the session at the end
func.close_session()
```
