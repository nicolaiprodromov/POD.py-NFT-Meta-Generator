# 🥚 POD.py | A simple nft metadata generator | WIP  🐣

## How to use 🐸

> Need python v > 3

1. Edit the file `POD.config.json` to configure your collection
2. Place **all** objects that you want **distributed** inside the folder -> *POD/Objects/*
3. Edit the file @**Attributes/`Attributes.config.json`** with the type of attributes that each token must have
4. Run the pod.py file

```shell
python3 pod.py -supply:100 -verbose:True -obj:obj -clean:True
```

 Download, cd into folder and run above command. Your output should be something like this:
```
[POD][NFT Metadata generator]
[
 Collection: Test_NFT
  Symbol: TST
  Supply: 100
  Price per Unit: 0.02/Token
  Hash: 0x9458a6ddfa501799ea3d9f8da861c4a743807501a28dac6fa77b193ff4465c57
 [Clean up in ./Metadata]-[※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※]
 [Creating tokens]-[※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※]
 [Loading Objects]/[※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※]
 [Dumping tokens to file]-[※※※※※※※※※※※※※※※※※※※※※※※※※※※※※※]
 [Success]
]
```

---

## Details 🦎

### ⬛ Attributes

> Note: ATM only Opensea type of metadata structure is outputed

Each attribute you will add to the file will at most be something like this:

```json
  {
    "type" : "number_display",
    "trait_type": "example_type", 
    "min": 0,
    "max" : 100,
    "display_type": "boost_percentage"
  }
```
Where:

1. `type` ---------- is an internal indicator that can be one of: *`number_display, number, date, object`*
2. `trait_type` --- is the trait type
3. `min` ----------- is the lowest value possible (only applies when type *number* or *number_display* is chosen)
4. `max` ----------- is the highest value possible (only applies when type *number* or *number_display* is chosen)
5. `display_type`--- is the type of display on Opensea (only applies when type *number_disply* is chosen)

### ⬛ Objects

Objects need to be placed inside */POD/Objects* folder and have to named after the following convention:

``{property} {object}.{extension}`` e.g $ **Red Hat.obj**

If you don't need files to represent objects you can simply create empty files with whatever extension you wish as long as you pass the argument `-obj:{yourextension}`

---


