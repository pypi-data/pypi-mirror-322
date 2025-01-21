class Protocol_Common():
    def ResponseActionComplete(self,sender,receiver,uuid):
        return {
              "headers": {
                "protocol_version": "1.0",
                "timestamp": "2024-11-08T10:00:00Z",
                "sender": sender,
                "receiver": receiver,
                "message_name": "CallWarehouseInbound",
                "conversation_id": uuid,
              },
              "body": { 
                "status": True,
              }
            }