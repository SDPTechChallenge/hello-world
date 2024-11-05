"use client";

import { getChatEndpoint } from "@/utils/api";
import { useState } from "react";

const Home = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState<
    { role: "user" | "assistant"; content: string }[]
  >([]);
  const [waitingForResponse, setWaitingForResponse] = useState(false);

  async function callChatEndpoint(message: string) {
    setMessages((msgs) => [...msgs, { role: "user", content: userInput }]);
    setUserInput("");
    setWaitingForResponse(true);

    const endpoint = getChatEndpoint("sql", "abcd1234");
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: message }),
    });

    if (response.ok) {
      const data = await response.json();
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: data.response },
      ]);
    } else {
      setMessages((msgs) => [
        ...msgs,
        { role: "assistant", content: "CONNECTION ERROR" },
      ]);
    }
  }

  function submitInputIfEnter(e: any) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      callChatEndpoint(userInput);
    }
  }

  return (
    <main>
      <div className="chat-outer-container relative pt-4 h-screen">
        <div className="chat-messages-container max-w-[660px] mx-auto">
          {messages.map((message, index) => {
            let classString = "";
            classString =
              message.role === "user"
                ? "user-message w-fit max-w-[300px] lg:max-w-[600px] ml-auto rounded-lg bg-zinc-300 p-1 px-2"
                : "assistant-message";
            return (
              <div
                className={`chat-message mb-[.625rem] ${classString}`}
                key={index}
              >
                {message.content}
              </div>
            );
          })}
          {waitingForResponse && (
            <div className="assistant-message">Escrevendo...</div>
          )}
        </div>
        <div className="user-input-area-container absolute inset-0 top-auto p-2">
          <div className="user-input-area max-w-[660px] mx-auto">
            <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={submitInputIfEnter}
              placeholder="Escreva sua mensagem aqui"
              className="user-input rounded-lg bg-zinc-300 p-1 px-2 w-full resize-none outline-none"
            ></textarea>
            <button
              className="send-button bg-zinc-300 rounded-lg p-1 px-3"
              onClick={() => callChatEndpoint(userInput)}
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Home;
