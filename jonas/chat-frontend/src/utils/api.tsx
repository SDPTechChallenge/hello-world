const API_URL = "http://localhost:8000";

function getChatEndpoint(
  botName: "internet" | "sql" | "document",
  conversationId: string
) {
  return `${API_URL}/chat/${botName}/${conversationId}`;
}

export { getChatEndpoint };
