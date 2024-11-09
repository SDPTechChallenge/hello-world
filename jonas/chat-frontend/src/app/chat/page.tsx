"use client";

import Header from "./components/Header";
import ChatContainer from "./components/ChatContainer";
import UserInputArea from "./components/UserInputArea";
import { useState } from "react";
import { getChatEndpoint } from "@/utils/api";
import { getWritable } from "@/utils/chat-helpers";
import Toaster from "@/components/custom/Toaster";
import useToast from "@/components/custom/Toaster";

const Home = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] = useState<
    { role: string; content: string; isVisibleToUser: boolean }[]
  >([]);
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const [currentMessage, setCurrentMessage] = useState<string | null>(null);
  const [files, setFiles] = useState<FileList | null>(null);
  const [chatOption, setChatOption] = useState("bot_sql");
  const [modelName, setModelName] = useState("gpt-4o-mini");

  const { toast, Toaster } = useToast();

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
    <main>
      <Toaster />
      <button
        onClick={() => {
          toast("error", "Test toast");
        }}
      >
        Test toast
      </button>
      <header className="fixed w-full h-12 flex flex-rows items-center justify-between bg-slate-200 px-4 z-10">
        <Header
          chatOption={chatOption}
          setChatOption={setChatOption}
          modelName={modelName}
          setModelName={setModelName}
        />
      </header>
      <ChatContainer
        messages={messages}
        currentMessage={currentMessage}
        waitingForResponse={waitingForResponse}
      />
      <footer className="user-input-area-container absolute inset-0 top-auto p-2 bg-white">
        <UserInputArea
          userInput={userInput}
          setUserInput={setUserInput}
          callChatEndpoint={callChatEndpoint}
        />
      </footer>
    </main>
  );
};

export default Home;
