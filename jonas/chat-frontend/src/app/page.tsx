"use client";

import { useState } from "react";

const conversation = [
  { role: "user", content: "Hello there!" },
  { role: "assistant", content: "Hi! How can I help you today?" },
  { role: "user", content: "I'm having trouble with my account." },
  {
    role: "assistant",
    content: "I'm sorry to hear that. What seems to be the problem?",
  },
  {
    role: "user",
    content: "I can't seem to log in. Lorem ipsum dolor sit amet.",
  },
  {
    role: "assistant",
    content:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Enim voluptatum facilis debitis, voluptatem animi ea ad corrupti officia molestias est.",
  },
];

const Home = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState(conversation);

  function submitInputIfEnter(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      setMessages((msgs) => [...msgs, { role: "user", content: userInput }]);
      setUserInput("");
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
            <button className="send-button bg-zinc-300 rounded-lg p-1 px-3">
              Send
            </button>
          </div>
        </div>
      </div>
    </main>
  );
};

export default Home;
