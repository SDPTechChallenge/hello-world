"use client";

import Dropdown from "@/components/custom/Dropdown";
import { DOCUMENT_UPLOAD_ENDPOINT, getChatEndpoint } from "@/utils/api";
import { getWritable } from "@/utils/chat-helpers";
import { ChangeEvent, useState } from "react";
import exampleChat from "@/utils/exampleChat.json";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { FiLoader as Loader } from "react-icons/fi";

const Home = () => {
  const [userInput, setUserInput] = useState("");
  const [messages, setMessages] =
    useState<{ role: string; content: string; isVisibleToUser: boolean }[]>(
      exampleChat
    );
  const [waitingForResponse, setWaitingForResponse] = useState(false);
  const [currentMessage, setCurrentMessage] = useState<string | null>(null);
  const [files, setFiles] = useState<FileList | null>(null);
  const [chatOption, setChatOption] = useState<
    "bot_sql" | "bot_document" | "bot_internet"
  >("bot_sql");

  async function callChatEndpoint(message: string) {
    setMessages((msgs) => [
      ...msgs,
      { role: "user", content: userInput, isVisibleToUser: true },
    ]);
    setUserInput("");
    setWaitingForResponse(true);

    const endpoint = getChatEndpoint(chatOption, "abcd1234");
    const response = await fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content: message }),
    });

    if (response && response.ok) {
      setWaitingForResponse(false);
      if (response.headers.get("Content-Type")?.includes("application/json")) {
        const data: { response: string } = await response.json();
        setMessages((prev) => [
          ...prev,
          { role: "assistant", content: data.response, isVisibleToUser: true },
        ]);
      } else {
        const newSessionId = response.headers.get("X-Session-Id");
        if (newSessionId) {
          window.history.replaceState(null, "", `/chat/id/${newSessionId}`);
        }
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

  async function handleFileInput(e: ChangeEvent<HTMLInputElement>) {
    const files = e.target.files;
    if (files) {
      // We will upload the files to the server (assume the endpoint as a variable named endpoint)
      const formData = new FormData();

      for (let i = 0; i < files.length; i++) {
        formData.append("files", files[i], files[i].name);
      }

      const response = await fetch(DOCUMENT_UPLOAD_ENDPOINT, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        // Handle response ok
        console.log("Files uploaded successfully.");
      } else {
        // Handle response error
        console.log(
          "Error uploading files. Status code:" + response.status.toString()
        );
      }
    }
  }

  function submitInputIfEnter(e: any) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      callChatEndpoint(userInput);
    }
  }

  const chatOptions = [
    { value: "bot_document", label: "Document Bot" },
    { value: "bot_internet", label: "Internet Bot" },
    { value: "bot_sql", label: "SQL Bot" },
  ];

  // Chat options dropdown state management

  return (
    <main>
      <header className="fixed w-full h-12 flex flex-rows items-center justify-between bg-slate-200 px-4 z-10">
        <h1 className="text-center text-lg font-bold">Chat</h1>
        <div>
          <Dropdown
            handleChange={setChatOption}
            value={chatOption}
            placeholder="Select chat"
            items={chatOptions}
          />
        </div>
      </header>
      <div className="chat-outer-container relative pt-14 h-screen overflow-hidden">
        <div className="chat-messages-container overflow-y-scroll h-full pb-28">
          <div className="chat-messages-inner-container max-w-[650px] mx-auto">
            {messages.map((message, index) => {
              if (!message.isVisibleToUser) {
                return null;
              }
              let classString = "";
              classString =
                message.role === "user"
                  ? "user-message w-fit max-w-[300px] lg:max-w-[650px] ml-auto rounded-lg bg-zinc-300 p-1 px-2"
                  : "assistant-message";
              return (
                <div
                  className={`chat-message mb-[1rem] ${classString}`}
                  key={index}
                >
                  <Markdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </Markdown>
                </div>
              );
            })}
            {currentMessage && (
              <div className="chat-message mb-[.625rem] assistant-message">
                {currentMessage}
              </div>
            )}
            {waitingForResponse && (
              <div className="pb-8 grid place-items-center">
                <Loader className="animate-spin h-8 w-8 mx-auto" />
              </div>
            )}
          </div>
        </div>
        <form className="user-input-area-container absolute inset-0 top-auto p-2">
          <div className="user-input-area max-w-[800px] mx-auto">
            <textarea
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={submitInputIfEnter}
              placeholder="Escreva sua mensagem aqui"
              className="user-input rounded-lg bg-[#f4f4f4] p-1 px-2 w-full resize-none outline-none"
            ></textarea>
            <div className="flex flex-row justify-start items-center gap-3">
              <button
                className="send-button bg-zinc-300 rounded-lg p-1 px-3"
                onClick={() => callChatEndpoint(userInput)}
              >
                Send
              </button>
              <input type="file" onChange={handleFileInput} />
            </div>
          </div>
        </form>
      </div>
    </main>
  );
};

export default Home;
