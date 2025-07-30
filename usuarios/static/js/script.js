function getImagem(id) {
  // Obtém o elemento da imagem
  var imagem = document.getElementById(id);
  // Obtém o nome do arquivo da imagem (após a última barra)
  var nomeImagem = imagem.src.split("/").pop();
 


  // Remove a extensão do arquivo
  //nomeImagem = nomeImagem.split(".")[0];

  // Obtém o elemento do campo de texto
  var campoTexto = document.getElementById("avatar_escolhido");

  // Define o valor do campo de texto com o nome da imagem
  campoTexto.value = nomeImagem;

  /**const avatar = document.getElementById(id);
  alert("Você clicou em: " + avatar.src);**/

}



