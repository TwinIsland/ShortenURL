# ShortenURL Model
The model layer class for shorten URL service 
# Usage
Complete the `init.py` to meet your demand, and use the `ShoternURL` class as below
```python
import ShortURL
func = ShortURL.ShortURL()

# add link
result = func.add("https://sougo.com")	# 1000 items in 1.7s safe mode

# check total length
print(func.len())

# check from original link / short link
result = func.get("https://sougo.com")

# don't forget to close the session
func.close()
```

