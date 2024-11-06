interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  finished?: boolean;
}

const decoder = new TextDecoder("utf-8");

function getWritable(
  setCurrentMessage: (text: string) => void,
  onFinished: Function
) {
  let text = "";
  return new WritableStream({
    write(chunk) {
      const decodedChunk = decoder.decode(chunk);
      text += decodedChunk;
      setCurrentMessage(text);
    },
    close() {
      onFinished((messages: ChatMessage[]) => {
        setCurrentMessage("");
        return [
          ...messages,
          { role: "assistant", content: text, finished: true },
        ];
      });
    },
  });
}

export { getWritable };
