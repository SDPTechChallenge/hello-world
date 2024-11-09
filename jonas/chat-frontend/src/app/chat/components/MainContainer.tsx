"use client";

import { getChatEndpoint } from "@/utils/api";
import ChatContainer from "./ChatContainer";
import UserInputArea from "./UserInputArea";
import { useState } from "react";
import { getWritable } from "@/utils/chat-helpers";
import Header from "./Header";
import { Toaster } from "@/components/ui/toaster";
import ChatProvider from "@/providers/ChatProvider";

const MainContainer = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState<
    { role: string; content: string; isVisibleToUser: boolean }[]
  >([]);
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const [currentMessage, setCurrentMessage] = useState<string | null>(null);
  const [files, setFiles] = useState<FileList | null>(null);
  const [chatOption, setChatOption] = useState("bot_sql");
  const [modelName, setModelName] = useState("gpt-4o-mini");

  async function callChatEndpoint(message: string) {
    setMessages((msgs) => [
      ...msgs,
      { role: "user", content: message, isVisibleToUser: true },
    ]);
    setUserInput("");
    setWaitingForResponse(true);

    const endpoint = getChatEndpoint(chatOption, "abcd1234");
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: message, model: modelName }),
    });

    if (response && response.ok) {
      setWaitingForResponse(false);
      if (response.headers.get("Content-Type")?.includes("application/json")) {
        const data = await response.json();
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.response, isVisibleToUser: true },
        ]);
      } else {
        response.body?.pipeTo(getWritable(setCurrentMessage, setMessages));
      }
    } else {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Erro ao ler a resposta.",
          isVisibleToUser: true,
        },
      ]);
    }
  }

  return (
    <ChatProvider>
      <Toaster />
      <header className="fixed w-full h-16  flex flex-rows items-center justify-between bg-zinc-800 px-4 z-10">
        <Header />
      </header>
      <div className="chat-outer-container relative pt-14 h-full overflow-hidden">
        <ChatContainer
          messages={messages}
          currentMessage={currentMessage}
          waitingForResponse={waitingForResponse}
        />
      </div>
      <footer className="user-input-area-container absolute inset-0 top-auto p-2 bg-white">
        <UserInputArea
          userInput={userInput}
          setUserInput={setUserInput}
          callChatEndpoint={callChatEndpoint}
        />
      </footer>
    </ChatProvider>
  );
};

export default MainContainer;
