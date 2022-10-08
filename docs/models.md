# MODELS
NOTE: best to view on github (support for markdown)
## USER

|name|type|is unique|
|----|----|---------|
|id|Integer|yes|
|name|String <=256|yes|
|mail|String<=256|yes|
|password|String<=256|no|
|city|String<=1024|no|
|description|String<=4096|no|

## EVENT

|name|type|is unique|
|----|----|---------|
|id|Integer|yes|
|title|String <=256|yes|
|creator|String<=256|no|
|image|String<=256|yes|
|description|String|no|
|date|Python datetime object|no|
|location|String<=1024|False|