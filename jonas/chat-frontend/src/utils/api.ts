const API_URL = "http://localhost:8000";

function getChatEndpoint(
  botName: "bot_sql" | "bot_document" | "bot_internet",
  conversationId: string
) {
  return `${API_URL}/chat/${botName}/${conversationId}`;
}

const DOCUMENT_UPLOAD_ENDPOINT = `${API_URL}/documents`;

export { getChatEndpoint, DOCUMENT_UPLOAD_ENDPOINT };
