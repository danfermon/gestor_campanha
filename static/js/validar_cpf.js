function validarCPF(cpf) {
  cpf = cpf.replace(/[^\d]+/g, '');

  if (cpf.length !== 11 || /^(\d)\1{10}$/.test(cpf)) {
    return false;
  }

  let soma = 0;
  for (let i = 0; i < 9; i++) {
    soma += parseInt(cpf.charAt(i)) * (10 - i);
  }

  let resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;
  if (resto !== parseInt(cpf.charAt(9))) return false;

  soma = 0;
  for (let i = 0; i < 10; i++) {
    soma += parseInt(cpf.charAt(i)) * (11 - i);
  }

  resto = (soma * 10) % 11;
  if (resto === 10 || resto === 11) resto = 0;

  return resto === parseInt(cpf.charAt(10));
}

document.addEventListener('DOMContentLoaded', function () {
  const cpfInput = document.getElementById('cpf');
  let erroMostrado = false;

  cpfInput.addEventListener('blur', function () {
    const cpfValido = validarCPF(cpfInput.value);
    
    if (!cpfValido && !erroMostrado) {
      alert('CPF inválido! Corrija antes de continuar.');
      erroMostrado = true;
    } else if (cpfValido) {
      erroMostrado = false; // Reseta quando o CPF é corrigido
    }
  });

  // Evita envio com CPF inválido
  document.querySelector('form').addEventListener('submit', function (e) {
    if (!validarCPF(cpfInput.value)) {
      alert('CPF inválido! Corrija antes de enviar.');
      e.preventDefault();
    }
  });
});
