#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""This is the advanced GUI version of the Windows Command Line script
that does the ICC Profile creation.

Workflow:

from icc_generator.api import ICCGenerator, PaperSizeLibrary

ig = ICCGenerator()

# Set Printer Details
ig.printer_brand = "Epson"
ig.printer_model = "ET8550"

# Set Paper Details
ig.paper_brand = "Kodak"
ig.paper_model = "UPPP"
ig.paper_finish = "Glossy"
ig.paper_size = PaperSizeLibrary.A4  # Or generate a custom size.

# Set Ink Details
ig.ink_brand = "Epson"

# Profiling workflow, run the following commands in the given order:
ig.gray_patch_count = 128  # default is 128, which should be quite enough.
ig.generate_target()
ig.generate_tif()  # This will output TIF file paths
ig.print_charts()  # Can be skipped and TIF file paths can be directly used.
ig.read_charts()
ig.generate_profile()
ig.check_profile(True)  # Look to the first couple of rows for high errors (dE > 3).

# Optional
# To fix misread patches (patches with too high dE values)
# re-read the chart in resume mode
ig.read_charts(resume=True, read_mode=0) # use read_mode=1 for patch-by-patch

# Finally install the profile
ig.install_profile()
"""
import logging

from icc_generator.version import __version__


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
