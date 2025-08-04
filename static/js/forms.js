document.addEventListener('DOMContentLoaded', function () {
  // Máscara para data de nascimento (dd/mm/aaaa)
  var dtNasc = document.getElementById('dt_nasc');
  if (dtNasc) {
    IMask(dtNasc, { mask: '00/00/0000' });
  }

  // Máscara para CPF
  var cpf = document.getElementById('cpf');
  if (cpf) {
    IMask(cpf, { mask: '000.000.000-00' });
  }

  // Máscara para telefone fixo
  /*var telefone = document.getElementById('telefone');
  if (telefone) {
    IMask(telefone, { mask: '(00) 0000-0000' });
  }*/

  // Máscara para celular
  var celular = document.getElementById('celular');
  if (celular) {
    IMask(celular, { mask: '(00) 00000-0000' });
  }

  // Máscara para CEP
  var cep = document.getElementById('cep');
  if (cep) {
    IMask(cep, { mask: '00000-000' });
  }
});