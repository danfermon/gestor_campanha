def gerar_link_sefaz(chave):
    """
    Gera o link de consulta pública da NFC-e ou CF-e SAT baseado na UF.
    """
    if not chave or len(chave) != 44:
        return ''

    uf_codigo = chave[:2]

    links_sefaz = {
        '11': 'https://www.nfe.sefin.ro.gov.br/consultanfce/seguranca',
        '12': 'https://www.sefaz.ac.gov.br/nfce',
        '13': 'https://sistemas.sefaz.am.gov.br/nfceweb/consultarNFCe.jsp',
        '14': 'https://www.sefaz.rr.gov.br/nfce',
        '15': 'https://www.sefa.pa.gov.br/nfce/consulta',
        '16': 'https://www.sefaz.ap.gov.br/nfce',
        '17': 'https://www.sefaz.to.gov.br/nfce',
        '21': 'https://sistemas.sefaz.ma.gov.br/nfceconsulta',
        '22': 'https://webas.sefaz.pi.gov.br/nfceweb',
        '23': 'https://nfce.sefaz.ce.gov.br',
        '24': 'https://nfce.set.rn.gov.br/portal',
        '25': 'https://www.receita.pb.gov.br/nfce',
        '26': 'https://nfce.sefaz.pe.gov.br',
        '27': 'https://www.sefaz.al.gov.br/nfce',
        '28': 'https://www.nfce.se.gov.br/portal',
        '29': 'https://www.sefaz.ba.gov.br/nfce',
        '31': 'https://nfce.fazenda.mg.gov.br/portalnfce',
        '32': 'https://app.sefaz.es.gov.br/ConsultaNFCe',
        '33': 'https://www4.fazenda.rj.gov.br/consultaNFCe',
        '35': 'https://www.nfce.fazenda.sp.gov.br/consultapublica',
        '41': 'https://www.fazenda.pr.gov.br/nfce',
        '42': 'https://sat.sef.sc.gov.br/nfce',
        '43': 'https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx',
        '50': 'https://www.dfe.ms.gov.br/nfce',
        '51': 'https://www.sefaz.mt.gov.br/nfce',
        '52': 'https://nfe.sefaz.go.gov.br/nfeweb/sites/nfce',
        '53': 'https://www.fazenda.df.gov.br/nfce',
    }

    url_base = links_sefaz.get(uf_codigo, '')
    if url_base:
        return f"{url_base}?chNFe={chave}"
    return ''


