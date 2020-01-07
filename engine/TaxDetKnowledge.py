import pandas as pd

from experta import *


class Ncm(Fact):
    pass


class Source(Fact):
    pass


class Target(Fact):
    pass


class OperationNature(Fact):
    pass


class TaxDeterminationEngine(KnowledgeEngine):
    tax_lines = pd.DataFrame({'NCM', 'Source', 'Target', 'OperationNature', 'ICMS'})

    def findTax(self, ncm, source, target, operNatur):
        tax_line = self.tax_lines.loc[
                    self.tax_lines.NCM == ncm &
                    self.tax_lines.Source == source &
                    self.tax_lines.Target == target &
                    self.tax_lines.OperationNature == operNatur]

        if tax_line is None:
            """ Call IOB """
            pass
        else:
            return tax_line.ICMS
