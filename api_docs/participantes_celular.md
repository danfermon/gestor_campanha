# 🔍 Buscar Participante por Celular

**URL:** `/api/participantes/buscar-por-celular/`  
**Método:** `POST`  
**Autenticação:** Token (via `Authorization: Token <seu_token>`)

---

## 🎯 Descrição

Este endpoint busca os dados de um participante cadastrado com base no número de celular informado no corpo da requisição.

---

## 🔐 Autenticação

Este endpoint exige que o cliente esteja autenticado usando o token da API:

```http
Authorization: Token seu_token

## 📥 Corpo da Requisição
{
  "celular": "11988887777"
}

| Campo     | Tipo     | Obrigatório | Descrição                                          |
| --------- | -------- | ----------- | -------------------------------------------------- |
| `celular` | `string` | Sim         | Número de celular do participante (sem formatação) |

## 📤 Respostas
- ✅ 200 OK
```
{
  "id": 1,
  "nome": "João da Silva",
  "dt_nasc": "1990-05-01",
  "cpf": "12345678900",
  "telefone": "1122334455",
  "celular": "11988887777",
  "email": "joao@email.com",
  "uf": "SP",
  "cidade": "São Paulo",
  "cep": "01001000",
  "rua": "Rua das Flores",
  "bairro": "Centro",
  "num": 123
}
```

## ❌ 400 Bad Request
```
{
  "detail": "O número de celular é obrigatório."
}
```

## ❌ 404 Not Found
```
{
  "detail": "Participante não encontrado."
}
```

## ❌ 401 Unauthorized
```
{
  "detail": "Token inválido."
}
```

## 📌 Exemplo de Requisição com curl
```
curl -X POST http://127.0.0.1:8000/api/participantes/buscar-por-celular/ \
     -H "Authorization: Token seu_token" \
     -H "Content-Type: application/json" \
     -d '{"celular": "11988887777"}'
```