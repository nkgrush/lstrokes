# lstrokes
Re-draw painting into a grid of strokes

## Run
`python -m lstrokes file.jpg`

## Reason
Neural networks can be used to generate paintings from noise, but the output is low-resolution and the colors are off. How can it be easily fixed? 
By rendering *less strokes* instead of individual pixels.

## Usage
This module can be used to increase perceived image resolution by turning individual pixels into polygons and rendering them in a fancy way. Using fixed pallet can ensure bright colors. The output looks like a simple painting.

It can also be used to reduce big images with a diverse color pallet into smaller ones, which still look good. `Grid.__cells` is just a numpy array and it has all the data needed to render an image!

![landscape](https://user-images.githubusercontent.com/25302233/111865584-86889900-899a-11eb-8d54-22ae71b996df.jpeg)
![out](https://user-images.githubusercontent.com/25302233/111865586-89838980-899a-11eb-9d96-8aa187d3d895.jpg)
