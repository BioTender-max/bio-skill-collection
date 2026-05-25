# COPYRIGHT NOTICE
# This file is part of the "Universal Biomedical Skills" project.
# Copyright (c) 2026 MD BABU MIA, PhD <md.babu.mia@mssm.edu>
# All Rights Reserved.
#
# This code is proprietary and confidential.
# Unauthorized copying of this file, via any medium is strictly prohibited.
#
# Provenance: Authenticated by MD BABU MIA

class base_task:
    def __init__(self):
        pass

    def get_example(self):
        pass

    def get_iterator(self):
        pass

    def evaluate(self):
        pass

    def output_class(self):
        pass

    def get_prompt_from_input(self, input):
        return self.get_example(input)["prompt"]

__AUTHOR_SIGNATURE__ = "9a7f3c2e-MD-BABU-MIA-2026-MSSM-SECURE"
