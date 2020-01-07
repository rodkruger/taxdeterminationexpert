import datetime

import numpy as np
import zeep

# Authentication data
USER = 'fh@systax.com.br'
PASSWORD = '09SKL77O'

# Endpoint for Systax Web Service
wsdl = 'http://wscockpit.systax.com.br/TaxEngineNCM/TaxEngine.svc?wsdl'

# Creating a client to consume the services
client = zeep.Client(wsdl=wsdl)

# Referencing the datatypes from the services
factory = client.type_factory('ns2')


# Read taxes for an specific NF-item
def get_taxes_from_source(ncm, unit_value, date, source, target, nf_type):
    ID = '1'
    NAT_OP = '120'
    PERFIL_REM = '1'
    PERFIL_DEST = '140'
    ORIG = '0'
    Q_TRIB = '1'
    SESSION_ID = 'AGENT-0001'
    SIS_ORIG = '001'

    item = factory.Item(
        id=ID,
        natOp=NAT_OP,
        perfilRem=PERFIL_REM,
        perfilDest=PERFIL_DEST,
        orig=ORIG,
        NCM=ncm,
        vProdUni=unit_value,
        qTrib=Q_TRIB
    )

    items = factory.ArrayOfItem([item])

    header = factory.Cabecalho(
        usuario=USER,
        senha=PASSWORD,
        sessionID=SESSION_ID,
        sisOrig=SIS_ORIG,
        dtCalc=date,
        ufOrig=source,
        ufDest=target,
        CNAERem=target,
        tpNF=nf_type
    )

    response = factory.Chamada(cabecalho=header, itens=items)

    return client.service.Calcular(response)


def get_cabecalho(docnum):
    return df_j_1bnfdoc.loc[docnum]


def get_centro(werks):
    return df_t001w.loc[werks]


def get_stx(docnum, itmnum):
    return df_j_1bnfstx[(df_j_1bnfstx.DOCNUM == docnum) &
                        (df_j_1bnfstx.ITMNUM == itmnum) &
                        (df_j_1bnfstx.TAXTYP == 'ICM1')]


###############################################################################
# Teste Unitário do Serviço

import pandas as pd

print("Abrindo arquivos de dados", end='')
df_j_1bnfdoc = pd.read_csv("/home/rkruger/ContinentalVQA_559A/data/csv/df_nfdocs_2019.csv", low_memory=False)
df_j_1bnfdoc = df_j_1bnfdoc.replace(np.nan, '', regex=True)
print('.', end='')
df_j_1bnflin = pd.read_csv("/home/rkruger/ContinentalVQA_559A/data/csv/df_nfitems_2019.csv", low_memory=False)
df_j_1bnflin = df_j_1bnflin.replace(np.nan, '', regex=True)
print('.', end='')
df_j_1bnfstx = pd.read_csv("/home/rkruger/ContinentalVQA_559A/data/csv/df_nfitems_tax_2019.csv", low_memory=False)
df_j_1bnfstx = df_j_1bnfstx.replace(np.nan, '', regex=True)
print('.', end='')
df_t001w = pd.read_csv("/home/rkruger/ContinentalVQA_559A/data/csv/df_t001w.csv", low_memory=False)
print('.', end='')
print("[ OK ]")

df_j_1bnfdoc.set_index("DOCNUM", inplace=True)
df_t001w.set_index("WERKS", inplace=True)

df_result = pd.DataFrame()

lines = len(df_j_1bnflin)

count = 0

for i, row in df_j_1bnflin.iterrows():

    docnum = row['DOCNUM']
    itmnum = row['ITMNUM']
    werks = row['WERKS']

    if not werks.strip():
        continue

    l_j_1bnfdoc = get_cabecalho(docnum)
    l_t001w = get_centro(werks)

    natOp = row['CFOP'].strip()
    ncm = row['NBM'].strip()
    valorUnit = row['NETWR']
    data = datetime.datetime.strptime(str(l_j_1bnfdoc['PSTDAT']), '%Y%m%d')
    origem = l_t001w['REGIO']
    destino = l_j_1bnfdoc['REGIO']
    tpNf = l_j_1bnfdoc['DIRECT']

    if not natOp:
        continue

    if ncm == '99999999' or ncm == '00000000':
        continue

    if not origem or not destino:
        continue

    if origem == 'XX' or destino == 'XX':
        continue

    natOp = natOp[0:4]

    taxes_target = get_stx(docnum, itmnum)
    if not taxes_target.empty:
        icms_target = taxes_target.iloc[0]['RATE']

    icms_source = 0.0

    taxes_source = get_taxes_from_source(natOp, ncm, valorUnit, data, origem, destino, tpNf)
    taxes_source_items = taxes_source.itens.Item[0]

    if taxes_source_items:
        if not taxes_source_items.NFe:
            df_result_row = pd.DataFrame(
                {"DOCNUM": [docnum],
                 "ITMNUM": [itmnum],
                 "EXPECTED": [0.0],
                 "INFORMED": [icms_target],
                 "INFADPROD": ['Regra não encontrada']})

            df_result = df_result.append(df_result_row)
        else:
            taxes_source_imposto = taxes_source_items.NFe.imposto
            if taxes_source_imposto:
                if taxes_source_imposto.ICMS.ICMS00:
                    icms_source = taxes_source_imposto.ICMS.ICMS00.pICMS
                elif taxes_source_imposto.ICMS.ICMS10:
                    icms_source = taxes_source_imposto.ICMS.ICMS10.pICMS
                elif taxes_source_imposto.ICMS.ICMS20:
                    icms_source = taxes_source_imposto.ICMS.ICMS20.pICMS
                elif taxes_source_imposto.ICMS.ICMS30:
                    icms_source = taxes_source_imposto.ICMS.ICMS30.pICMS
                elif taxes_source_imposto.ICMS.ICMS40:
                    icms_source = 0.0
                elif taxes_source_imposto.ICMS.ICMS51:
                    icms_source = taxes_source_imposto.ICMS.ICMS51.pICMS
                elif taxes_source_imposto.ICMS.ICMS60:
                    icms_source = taxes_source_imposto.ICMS.ICMS60.pICMS
                elif taxes_source_imposto.ICMS.ICMS70:
                    icms_source = taxes_source_imposto.ICMS.ICMS70.pICMS
                elif taxes_source_imposto.ICMS.ICMS90:
                    icms_source = taxes_source_imposto.ICMS.ICMS90.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN101:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN101.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN102:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN102.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN201:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN201.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN202:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN202.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN500:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN500.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN900:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN900.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN300:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN300.pICMS
                elif taxes_source_imposto.ICMS.ICMSSN400:
                    icms_source = taxes_source_imposto.ICMS.ICMSSN400.pICMS

            icms_source = float(icms_source)
            icms_infAdProd = taxes_source.itens.Item[0].NFe.infAdProd

            if icms_source != icms_target:
                df_result_row = pd.DataFrame(
                    {"DOCNUM": [docnum],
                     "ITMNUM": [itmnum],
                     "EXPECTED": [icms_source],
                     "INFORMED": [icms_target],
                     "INFADPROD": [icms_infAdProd]})

                df_result = df_result.append(df_result_row)

    count = count + 1

    if count % 100 == 0:
        print('Analisando notas [{0} / {1}]'.format(count, lines))

    if count == 500:
        break

df_result.to_csv(r'df_result.csv', index=None, header=True)
