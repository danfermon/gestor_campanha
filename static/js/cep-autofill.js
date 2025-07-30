// Carrega os estados brasileiros no <select id="uf">
function carregarEstados() {
  const estados = [
    { sigla: 'AC', nome: 'Acre' },
    { sigla: 'AL', nome: 'Alagoas' },
    { sigla: 'AP', nome: 'Amapá' },
    { sigla: 'AM', nome: 'Amazonas' },
    { sigla: 'BA', nome: 'Bahia' },
    { sigla: 'CE', nome: 'Ceará' },
    { sigla: 'DF', nome: 'Distrito Federal' },
    { sigla: 'ES', nome: 'Espírito Santo' },
    { sigla: 'GO', nome: 'Goiás' },
    { sigla: 'MA', nome: 'Maranhão' },
    { sigla: 'MT', nome: 'Mato Grosso' },
    { sigla: 'MS', nome: 'Mato Grosso do Sul' },
    { sigla: 'MG', nome: 'Minas Gerais' },
    { sigla: 'PA', nome: 'Pará' },
    { sigla: 'PB', nome: 'Paraíba' },
    { sigla: 'PR', nome: 'Paraná' },
    { sigla: 'PE', nome: 'Pernambuco' },
    { sigla: 'PI', nome: 'Piauí' },
    { sigla: 'RJ', nome: 'Rio de Janeiro' },
    { sigla: 'RN', nome: 'Rio Grande do Norte' },
    { sigla: 'RS', nome: 'Rio Grande do Sul' },
    { sigla: 'RO', nome: 'Rondônia' },
    { sigla: 'RR', nome: 'Roraima' },
    { sigla: 'SC', nome: 'Santa Catarina' },
    { sigla: 'SP', nome: 'São Paulo' },
    { sigla: 'SE', nome: 'Sergipe' },
    { sigla: 'TO', nome: 'Tocantins' },
  ];

  const selectUF = document.getElementById('uf');
  if (!selectUF) return;

  estados.forEach(estado => {
    const option = document.createElement('option');
    option.value = estado.sigla;
    option.textContent = estado.nome;
    selectUF.appendChild(option);
  });
}

// Consulta o CEP e preenche os campos
function pesquisacep(cep) {
  cep = cep.replace(/\D/g, '');

  if (cep.length !== 8) {
    alert("CEP inválido. Digite 8 dígitos.");
    return;
  }

  const url = `https://viacep.com.br/ws/${cep}/json/`;

  fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error("Erro ao buscar o CEP.");
      }
      return response.json();
    })
    .then(data => {
      if (data.erro) {
        alert("CEP não encontrado.");
        return;
      }

      const ruaInput = document.getElementById('rua');
      const bairroInput = document.getElementById('bairro');
      const cidadeInput = document.getElementById('cidade');
      const ufSelect = document.getElementById('uf');

      if (ruaInput) ruaInput.value = data.logradouro || '';
      if (bairroInput) bairroInput.value = data.bairro || '';
      if (cidadeInput) cidadeInput.value = data.localidade || '';

      if (ufSelect) {
        const options = ufSelect.options;
        for (let i = 0; i < options.length; i++) {
          if (options[i].value === data.uf) {
            ufSelect.selectedIndex = i;
            break;
          }
        }
      }
    })
    .catch(error => {
      console.error("Erro ao consultar o CEP:", error);
      alert("Erro ao consultar o CEP.");
    });
}

// Executa ao carregar a página
document.addEventListener('DOMContentLoaded', function () {
  carregarEstados();
});
