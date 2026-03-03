# Backend Video Call (WebSocket)

Base WS:
- `wss://<backend>/ws/chat?token=<JWT>`
- Também aceita: `wss://<backend>/ws?token=<JWT>`

Auth:
- JWT obrigatório em `query param` `token` (ou header `Authorization: Bearer ...`)

## Fluxo resumido
1. Caller envia `call_initiate` com `receiver_id`
2. Backend cria `call_id` e envia:
- para receiver: `incoming_call`
- para caller: `call_created`
3. Receiver responde com `call_accept` ou `call_reject` (usando `call_id`)
4. Após `accepted`, os dois trocam:
- `sdp_offer`
- `sdp_answer`
- `ice_candidate`
5. Qualquer lado pode encerrar com `call_end`

## Mensagens cliente -> servidor

### 1. Iniciar chamada
```json
{
  "type": "call_initiate",
  "receiver_id": 2
}
```

### 2. Aceitar chamada
```json
{
  "type": "call_accept",
  "content": "CALL_ID_AQUI"
}
```

### 3. Rejeitar chamada
```json
{
  "type": "call_reject",
  "content": "CALL_ID_AQUI"
}
```

### 4. Enviar SDP offer
```json
{
  "type": "sdp_offer",
  "content": "CALL_ID_AQUI",
  "sdp": { "type": "offer", "sdp": "..." }
}
```

### 5. Enviar SDP answer
```json
{
  "type": "sdp_answer",
  "content": "CALL_ID_AQUI",
  "sdp": { "type": "answer", "sdp": "..." }
}
```

### 6. Enviar ICE candidate
```json
{
  "type": "ice_candidate",
  "content": "CALL_ID_AQUI",
  "candidate": { "candidate": "...", "sdpMid": "...", "sdpMLineIndex": 0 }
}
```

### 7. Encerrar chamada
```json
{
  "type": "call_end",
  "content": "CALL_ID_AQUI"
}
```

## Mensagens servidor -> cliente

### Chamada recebida (receiver)
```json
{
  "type": "video_call",
  "action": "incoming_call",
  "data": { "call_id": "CALL_ID", "from_user": 1 }
}
```

### Chamada criada (caller)
```json
{
  "type": "video_call",
  "action": "call_created",
  "data": { "call_id": "CALL_ID" }
}
```

### Aceita/Rejeitada (ambos recebem)
```json
{
  "type": "video_call",
  "action": "call_accepted",
  "data": { "call_id": "CALL_ID", "by_user": 2 }
}
```

```json
{
  "type": "video_call",
  "action": "call_rejected",
  "data": { "call_id": "CALL_ID", "by_user": 2 }
}
```

### Relay de SDP
```json
{
  "type": "video_call",
  "action": "sdp_offer",
  "data": { "call_id": "CALL_ID", "from_user": 1, "sdp": { "...": "..." } }
}
```

```json
{
  "type": "video_call",
  "action": "sdp_answer",
  "data": { "call_id": "CALL_ID", "from_user": 2, "sdp": { "...": "..." } }
}
```

### Relay de ICE
```json
{
  "type": "video_call",
  "action": "ice_candidate",
  "data": { "call_id": "CALL_ID", "from_user": 1, "candidate": { "...": "..." } }
}
```

### Chamada encerrada
```json
{
  "type": "video_call",
  "action": "call_ended",
  "data": { "call_id": "CALL_ID", "ended_by": 1 }
}
```

## Erros conhecidos
- Usuário destino offline ao iniciar:
```json
{ "type": "error", "detail": "Usuario offline" }
```
- Token ausente/inválido: conexão fecha com código WS `1008`

## Regras backend
- `call_accept`/`call_reject` só pelo receiver correto
- `sdp_*` e `ice_candidate` só funcionam após status `accepted`
- `call_reject` remove a call ativa
- `call_end` remove a call ativa

## Nota
- Backend fornece só a sinalização WebRTC.
- Cliente deve configurar STUN/TURN para conectividade real de mídia.
