"""
Fait un Pixel Art.

Arguments : 
    image_path : Chemin de l'image à convertir en Pixel Art.
    output : Répertoire de sortie de l'image avec le nom de l'image.
    save_image : True si tu veux enregistrer l'image, False si tu ne veux pas l'enregistrer. Tu peux te servir de cette fonction avec cet argument sur False si tu veux simplement mettre les pixels avec leur couleur dans une variable.
    colors : Fait le Pixel Art avec les couleurs de votre choix. Tu peux aussi choisir le nombre de couleurs, voici les choix : 1 bit, 4 bits, 8 bits, 16 bits et Shades of gray.
    by : Tu décides le Pixel Art est par combien en conservant les proportions.
    warning : True : Afficher les avertissements
              False : Masquer les avertissements

Versions :
    1 : Convertit une image en Pixel Art.
    2 : Amélioration des choix de couleurs de Pixel Art
        Argument n renommé par by
        Argument output_path_and_image_name renommé par output
    3 : Option 16 bits ajoutée à l'argument colors, son utilité : faire un Pixel Art avec les couleurs 16 bits. Avertissement : En utilisant cette option, terminer le Pixel Art peut prendre beaucoup de temps. 
        Options renommées dans l'argument colors : 2_COLORS → 1 bit, 16_VGA_COLORS → 4 bits, 256_VGA_COLORS → 8 bits
    4 : Petite optimisation pour l'option 16 bits dans l'argument colors.
        Ajout de l'option Shades of gray dans l'argument colors pour faire un image avec des nuances de gris.
        Ajout de l'argument warnings pour afficher ou masquer les avertissements.
        Option 1 bit supprimée car elle n'était pas très utile. Si vous voulez encore l'utiliser, ajoutez [(255, 255, 255, 255), (0, 0, 0, 255)] à l'argument colors.
    5 : Options renommées dans l'argument colors : 4 bits → 16, 8 bits → 256, 16 bits → 65336, Shades of gray → shades_of_gray
    6 : En réalité, l'option 256 de colors était fausse, car elle convertissait les images en Pixel Art en 512 couleurs et non 256. Alors l'option 256 se renomme par 512.

     
Make a Pixel Art.

Arguments:
    image_path: Path of the image to convert to Pixel Art.
    output: Output directory of the image with the name of the image.
    save_image: True if you want to save the image, False if you don't want to save it. You can use this function with this argument set to False if you just want to put the pixels with their color into a variable.
    colors: Make the Pixel Art with the colors of your choice. You also can choose the number of colors, here is the choices : 1 bit, 4 bits, 8 bits, 16 bits and Shades of gray.
    by: You decide the Pixel Art is by how much while keeping the proportions.
    warnings: True: Show warnings
              False: Hide warnings

Versions:
    1: Convert an image to Pixel Art.
    2: Improved Pixel Art color choices
        n argument renamed to by
        output_path_and_image_name renamed argument renamed to output
    3: "16 bits" option added to the colors argument, his use: make a Pixel Art with 16-bit colors. Warning: Using this option can take a lot of time to finish the Pixel Art.
        Renamed options in the colors argument: 2_COLORS → 1 bit, 16_VGA_COLORS → 4 bits, 256_VGA_COLORS → 8 bits
    4: Small optimization for the "16 bit" option in the color argument.
        Added "Shades of gray" option to colors argument to make image with shades of gray.
        Added warnings argument to show or hide warnings.
        Removed "1 bit" option because it wasn't very useful. If you still want to use it, add [(255, 255, 255, 255), (0, 0, 0, 255)] to colors argument.
    5: Renamed options in the colors argument: 4 bits → 16, 8 bits → 256, 16 bits → 65336, Shades of gray → shades_of_gray
    6: Actually the 256 color option was wrong, because it converted the Pixel Art images to 512 colors, not 256. So the 256 option is renamed to 512.
"""

from PIL import Image
from collections import Counter
from math import sqrt
import numpy as np

__version__ = "0.3.3"

def PixelArt(image_path: str, by: int, output: str = "./PixelArt.png", save_image: bool = True, colors=None, warnings: bool = True):
    if save_image != True or False:
        save_image = True

    if colors == 16:
        mode = 16
        colors = [(0, 0, 0, 255), (0, 0, 170, 255), (0, 170, 0, 255), (0, 170, 170, 255), (170, 0, 0, 255), (170, 0, 170, 255), (170, 85, 0, 255), (170, 170, 170, 255), (85, 85, 85, 255), (85, 85, 255, 255), (85, 255, 85, 255), (85, 255, 255, 255), (255, 85, 85, 255), (255, 85, 255, 255), (255, 255, 85, 255), (255, 255, 255, 255)]
    elif colors == 512:
        mode = 512
        colors = [(r, g, b, 255) for r in [0, 36, 72, 109, 145, 182, 218, 255] for g in [0, 36, 72, 109, 145, 182, 218, 255] for b in [0, 36, 72, 109, 145, 182, 218, 255]]
    elif colors == 65336:
        mode = 65336
        colors = [((r * 255) // 31, (g * 255) // 63, (b * 255) // 31, 255) for r in range(32) for g in range(64) for b in range(32)]
    elif colors == "shades_of_gray":
        mode = "shades_of_gray"
        colors = [(c, c, c, 255) for c in range(0, 255)]
    elif colors != None:
        mode = "other"
    else:
        mode = None

    image = Image.open(image_path)
    image = image.convert("RGBA")
    x, y = image.size

    too_small_image_error_message = f"Image trop petite pour y en faire un Pixel Art {by}×{by}.\n\nToo small image to make a {by}×{by} Pixel Art."

    if x < by or y < by:
        raise ValueError(too_small_image_error_message)

    if mode == "16 bits":
        if warnings != False:
            print('Utiliser le paramètre 16 bits peut prendre beaucoup de temps. Pour ne pas afficher cet avertissement, ajouter warnings=False à la fonction PixelArt.\n\nUsing the "16 bits" setting can take a lot of time. To avoid displaying this warning, add warnings=False to the PixelArt function.')

    if x == y:
        new_x = by
        new_y = by
    elif x >= y:
        new_x = int(by * x / y)
        new_y = by
    else:
        new_x = by
        new_y = int(by * y / x)

    x_sections = x // new_x
    y_sections = y // new_y

    pixels = {}
    pixel_art = {}

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            pixels[(X, Y)] = []

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            try:
                pixels[(X, Y)].append(image.getpixel((x_sections * (X - 1), y_sections * (Y - 1))))
            except IndexError:
                pass

    for X in range(1, new_x + 1):
        for Y in range(1, new_y + 1):
            if pixels[(X, Y)]:
                if mode == None:
                    pixel_art[(X, Y)] = Counter(pixels[(X, Y)]).most_common(1)[0][0]
                elif mode not in [65336, 512, "shades_of_gray"]:
                    pixel_art[(X, Y)] = min(colors, key=lambda c: sqrt(sum((Counter(pixels[(X, Y)]).most_common(1)[0][0][i] - c[i])**2 for i in range(4))))
                elif mode in [65336, 512, "shades_of_gray"]:
                    pixel_art[(X, Y)] = tuple(colors[np.argmin(np.sqrt(np.sum((np.array(colors)[:, :3] - np.array(Counter(pixels[(X, Y)]).most_common(1)[0][0][:3])) ** 2, axis=1)))]) 

    if save_image == True:
        pixel_art_image = Image.new("RGBA", (new_x, new_y), (0, 0, 0, 0))

        pixels_in_pixel_art = pixel_art_image.load()

        for X in range(0, new_x):
            for Y in range(0, new_y):
                try:
                    pixels_in_pixel_art[X, Y] = pixel_art[X+1, Y+1]
                except KeyError:
                    pass

        pixel_art_image.save(output)

    return pixel_art