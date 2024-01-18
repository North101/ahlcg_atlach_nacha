# Arkham Horror LCG: Atlach-Nacha

A tray designed to hold Atlach-Nacha from The Dream-Eaters cycle

The box was made on a laser cutter. Because each laser cutter is different and you may be using different wood, I haven't provided the final files.

Instead I've created a script where you can adjust the different variables to suit what you need.


## The script

### Required installs

[Python 3](https://wiki.python.org/moin/BeginnersGuide/Download)

Download [this repo](https://codeload.github.com/North101/ahlcg_atlach_nacha/zip/refs/heads/main) and unzip it


```bash
# setup python virtual env
python3 -m venv .venv

# activate virtual env
source .venv/bin/activate

# install required libs
python3 -m pip install -r requirements.txt
```


### Running

Activate python virtual env (if not already done)
```bash
source .venv/bin/activate
```

Generate the files with the default arguments:
```bash
python3 -m ahlcg_atlach_nacha
```

To see all the arguments:
```bash
python3 -m ahlcg_atlach_nacha --help
```


### Default arguments

```bash
# output directory
--output = output/

# width of the card (mm)
--width = 63
# height of card (mm)
--height = 89
# depth of the card stack (mm)
--depth = 4
# thickness of the wood (mm)
--thickness = 3.17
# https://community.glowforge.com/t/kerf-explained-hopefully/2917
--kerf = 0.07
# whether or not to have a hole for the lazy susan
--hole = true

# size of the finger joint tabs (mm)
--tab = 4
# size of the depth finger joint tabs (mm)
--depth_tab = 2
# size of finger cutout in the tray (mm)
--finger_cutout = 20

# icon path (must be an svg)
--icon = icons/agents_of_atlach_nacha.svg
# icon scale
--icon_scale = 2.0
# icon width (mm)
--icon_width = 32
# icon height (mm)
--icon_height = 32
```


### Piece Count

* 1 × ahlcg_atlach_nacha_back.svg
* 16 × ahlcg_atlach_nacha_h_edge.svg
* 12 × ahlcg_atlach_nacha_v_edge.svg
* 4 × ahlcg_atlach_nacha_v_middle.svg


#### If using a lazy susan:
* 1 × ahlcg_atlach_nacha_lock.svg


### Arguments you should probably change

#### `width` / `height` / `depth`

The width, height and depth are the sizes of the cards when unsleeved. If you use sleeves you may want to modify these value.


#### `thickness`

The thickness of the wood is important as it affects the size of everything.


#### `kerf`

[Kerf explained](https://community.glowforge.com/t/kerf-explained-hopefully/2917)

The laser has a width and height to it which causes extra material to be removed. `kerf` is the adjustment made to compensate for that. It is also used to configure how tight the finger joints are.

The script will generate a `kerf_test.svg` to help figure out if you have the correct settings. When pushing the pieces together they should be tight.


## Materials I used

Here are the materials I used. You don't have to use the same ones but if you do you may need to make some adjustments to the arguments

Wood: [Walnut Plywood 12in x 20in (Medium Thickness)](https://shop.glowforge.com/collections/plywood/products/walnut-plywood-finished)

Optional:
Lazy Susan: [2 inch Rotating Swivel Stand](https://www.amazon.co.uk/dp/B0B1ZQTVMH)
