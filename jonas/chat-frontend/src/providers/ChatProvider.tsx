"use client";

import { createContext, Dispatch, SetStateAction, useState } from "react";

interface ChatContextValues {
  model: string;
  setModel: Dispatch<SetStateAction<string>>;
  bot: string;
  setBot: Dispatch<SetStateAction<string>>;
}

// @ts-expect-error
export const ChatContext = createContext<ChatContextValues>({});

const ChatProvider = ({ children }: { children: React.ReactNode }) => {
  const [model, setModel] = useState("gpt-4o-mini");
  const [bot, setBot] = useState("bot_sql");

  const value = {
    model,
    setModel,
    bot,
    setBot,
  };

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>;
};

export default ChatProvider;
