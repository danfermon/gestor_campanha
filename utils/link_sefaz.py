def gerar_link_sefaz(chave):
    """
    Gera o link de consulta CFe via API InfoSimples baseado na UF.
    A chave deve ter 44 caracteres.
    """

    if not chave or len(chave) != 44:
        return ''

    # Código numérico da UF (primeiros dois dígitos da chave)
    uf_codigo = chave[:2]

    # Mapeamento código -> sigla UF
    codigos_uf = {
        11:'ro', # — Rondônia (RO);
        12:'ac', # — Acre (AC);
        13:'am', # — Amazonas (AM);
        14:'rr', # — Roraima (RR);
        15:'pa', # — Pará (PA);
        16:'ap', # — Amapá (AP);
        17:'to', # — Tocantins (TO);
        21:'ma', # — Maranhão (MA);
        22:'pi', # — Piauí (PI);
        23:'ce', # — Ceará (CE);
        24:'rn', # — Rio Grande do Norte (RN);
        25:'pb', # — Paraíba (PB);
        26:'pe', # — Pernambuco (PE);
        27:'al', # — Alagoas (AL);
        28:'se', # — Sergipe (SE);
        29:'ba', # — Bahia (BA);
        31:'mg', # — Minas Gerais (MG);
        32:'es', # — Espírito Santo (ES);
        33:'rj', # — Rio de Janeiro (RJ);
        35:'sp', # — São Paulo (SP);
        41:'pr', # — Paraná (PR);
        42:'sc', # — Santa Catarina (SC);
        43:'rs', # — Rio Grande do Sul (RS);
        50:'ms', # — Mato Grosso do Sul (MS);
        51:'mt', # — Mato Grosso (MT);
        52:'go', # — Goiás (GO);
        53:'df', # — Distrito Federal (DF).
                    
    }

    # Endpoints nfce InfoSimples
    links_infosimples = {
        'ac': "https://api.infosimples.com/api/v2/consultas/sefaz/ac/nfce",
        'al': "https://api.infosimples.com/api/v2/consultas/sefaz/al/nfce",
        'ap': "https://api.infosimples.com/api/v2/consultas/sefaz/ap/nfce",
        'am': "https://api.infosimples.com/api/v2/consultas/sefaz/am/nfce",
        'ba': "https://api.infosimples.com/api/v2/consultas/sefaz/ba/nfce",
        'ce': "https://api.infosimples.com/api/v2/consultas/sefaz/ce/nfce",
        'df': "https://api.infosimples.com/api/v2/consultas/sefaz/df/nfce",
        'es': "https://api.infosimples.com/api/v2/consultas/sefaz/es/nfce",
        'go': "https://api.infosimples.com/api/v2/consultas/sefaz/go/nfce",
        'ma': "https://api.infosimples.com/api/v2/consultas/sefaz/ma/nfce",
        'mt': "https://api.infosimples.com/api/v2/consultas/sefaz/mt/nfce",
        'ms': "https://api.infosimples.com/api/v2/consultas/sefaz/ms/nfce",
        'mg': "https://api.infosimples.com/api/v2/consultas/sefaz/mg/nfce",
        'pa': "https://api.infosimples.com/api/v2/consultas/sefaz/pa/nfce",
        'pb': "https://api.infosimples.com/api/v2/consultas/sefaz/pb/nfce",
        'pr': "https://api.infosimples.com/api/v2/consultas/sefaz/pr/nfce", #parana   
        'pe': "https://api.infosimples.com/api/v2/consultas/sefaz/pe/nfce",
        'pi': "https://api.infosimples.com/api/v2/consultas/sefaz/pi/nfce",
        'rj': "https://api.infosimples.com/api/v2/consultas/sefaz/rj/nfce",
        'rn': "https://api.infosimples.com/api/v2/consultas/sefaz/rn/nfce",
        'rs': "https://api.infosimples.com/api/v2/consultas/sefaz/rs/nfce",
        'ro': "https://api.infosimples.com/api/v2/consultas/sefaz/ro/nfce",
        'rr': "https://api.infosimples.com/api/v2/consultas/sefaz/rr/nfce",
        'sc': "https://api.infosimples.com/api/v2/consultas/sefaz/sc/nfce",
        'sp': "https://api.infosimples.com/api/v2/consultas/sefaz/sp/nfce",
        'se': "https://api.infosimples.com/api/v2/consultas/sefaz/se/nfce",
        'to': "https://api.infosimples.com/api/v2/consultas/sefaz/to/nfce"
    }

    uf_sigla = codigos_uf.get(uf_codigo)

    if uf_sigla and uf_sigla in links_infosimples:
        # Retorna o endpoint base - não há parâmetro de chave no link da documentação InfoSimples
        return links_infosimples[uf_sigla]

    return ''
