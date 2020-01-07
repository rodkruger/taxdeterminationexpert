from engine.TaxDetKnowledge import *


class TaxDeterminationApi:
    engine = TaxDeterminationEngine()

    def findTax(ncm, source, target, operNatur):
        engine.reset()
        engine.declare(Ncm(code=ncm))
        engine.declare(Source(uf=source))
        engine.declare(Target(uf=target))
        engine.declare(OperationNature(code=operNatur))
        engine.run()
