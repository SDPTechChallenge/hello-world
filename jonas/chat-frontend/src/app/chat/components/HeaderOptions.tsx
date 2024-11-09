"use client";

import Dropdown from "@/components/custom/Dropdown";
import { ChatContext } from "@/providers/ChatProvider";
import { Dispatch, SetStateAction, useContext } from "react";

interface HeaderOptionsProps {
  chatOption: string;
  setChatOption: Dispatch<SetStateAction<string>>;
  modelName: string;
  setModelName: Dispatch<SetStateAction<string>>;
}

const chatOptions = [
  { value: "bot_document", label: "Document Bot" },
  { value: "bot_internet", label: "Internet Bot" },
  { value: "bot_sql", label: "SQL Bot" },
];

const modelOptions = [
  { value: "gpt-4o-mini", label: "gpt-4o-mini" },
  { value: "gpt-4o", label: "gpt-4o" },
  { value: "meta/llama-3.2-3b-instruct", label: "llama-3.2-3b-instruct" },
  { value: "meta/llama-3.1-70b-instruct", label: "llama-3.1-70b-instruct" },
];

const HeaderOptions = () => {
  const { bot, setBot, model, setModel } = useContext(ChatContext);

  return (
    <>
      <Dropdown
        placeholder="Assistente"
        handleChange={setBot}
        value={bot}
        items={chatOptions}
      />
      <Dropdown
        placeholder="Modelo"
        handleChange={setModel}
        value={model}
        items={modelOptions}
      />
    </>
  );
};

export default HeaderOptions;
