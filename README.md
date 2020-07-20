# SFSymbol Converter to png and pdf
This command-line tool makes it quick and easy to convert an SFSymbol into png/pdf format for back-compatibility.

## Installation
- Clone repo to your Mac
- Install the following dependencies using pip
```
argparse
cairosvg
svgpathtools
```
- You may also have to install `cairo` and `libffi` (you can use brew for both)
- Create a symlink for the scripts folder to your path variable
```
sudo ln -s sfsymbolConvert/scripts/* {DIRECTORY_TO_PATH}/.
```

## Usage
- Download the [SF Symbols App](https://developer.apple.com/sf-symbols/)
- Select a symbol and export using CMD-E or File -> Export
- Run the following command in a terminal
```
sfconvert [src_path] [destination_path] 
```

#### Additional Options
###### Style
SFSymbols contain several formatting styles due to their highly adaptive nature. When exporting as a pdf or png format, only one of these styles can be chosen. Other values include Ultralight, Thin, Light, Regular, Medium, Semibold, Bold, Heavy, Black. Each style has S, M, or L appended to it. E.G. `Thin-S`. **The default value is Regular-M.**

###### Type
Export to pdf or png. Both export with transparent backgrounds. The png export option will create three copies @1x, @2x and @3x. When using the png option you can also supply the `--png_size` input which is the size used for the @1x image. The others are scaled accordingly.
 
```
usage: sfconvert [-h] [--style [STYLE]] [--type {pdf,png}]
                 [--png_size [PNG_SIZE]]
                 [src] [dest]

Convert an SFSymbol file type to pdf or png.

positional arguments:
  src                   Path to SFSymbol file
  dest                  Path to save converted file. Include name but not
                        format extension.

optional arguments:
  -h, --help            show this help message and exit
  --symbol [SYMBOL]     The specific symbol to use for export. Default is
                        Regular-M
  --type {pdf,png}
  --png_size [PNG_SIZE]
                        Used for png type, size of 1x image. 2x and 3x will be
                        scaled.
```

