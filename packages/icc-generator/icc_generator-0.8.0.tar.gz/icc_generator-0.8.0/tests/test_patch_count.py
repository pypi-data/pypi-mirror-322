# -*- coding: utf-8 -*-

from icc_generator.api import ICCGenerator, PaperSizeLibrary


def main():
    ig = ICCGenerator()
    ig.printer_brand = "Epson"
    ig.printer_brand = "Epson"
    ig.printer_model = "ET-8550"
    ig.paper_brand = "Lustre"
    ig.paper_model = "Prestige"
    ig.paper_finish = "Matte"
    ig.paper_finish = "Satin"
    ig.paper_size = PaperSizeLibrary.LetterR
    ig.use_high_density_mode = True
    ig.ink_brand = "Epson"
    ig.gray_patch_count = 256
    ig.generate_target()
    ig.generate_tif()
    # ig.print_charts()


if __name__ == "__main__":
    main()
